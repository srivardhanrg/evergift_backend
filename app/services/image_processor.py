"""
Premium Image Processor for MagicTales text overlays.

This service handles:
- Fetching filler images from R2
- Rendering premium text overlays with PIL
- Applying drop caps, shadows, and theme-specific styling
- Uploading processed images back to R2

Designed for $40 premium storybook quality.
"""

import structlog
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from typing import Optional, Tuple, List, Dict
import os

from app.config.text_styling import (
    get_text_config,
    get_dedication_text,
    get_page_specific_colors,
    get_font_path,
    TextConfig,
    TextAlignment,
    BubbleConfig,
    FONT_PATHS,
)
from app.services.storage import StorageService

logger = structlog.get_logger()

# Default page dimensions (8.5x8.5 inch at 300 DPI for Lulu print)
DEFAULT_PAGE_WIDTH = 2550
DEFAULT_PAGE_HEIGHT = 2550


class ImageProcessor:
    """
    Premium text overlay processor for filler pages.

    Uses PIL/Pillow for high-quality text rendering with:
    - Custom Google Fonts (Dancing Script, Playfair Display, Cormorant Garamond)
    - Theme-specific color palettes
    - Page-specific color adaptations
    - Drop caps for story pages
    - Soft shadows for depth
    - Centered text positioning
    """

    def __init__(self):
        self.storage = StorageService()
        self._fonts_cache: Dict[str, ImageFont.FreeTypeFont] = {}
        self._fonts_loaded = False

    def _load_font(self, font_family: str, font_size: int) -> ImageFont.FreeTypeFont:
        """
        Load a font with caching.

        Attempts to load from /app/fonts/, falls back to system fonts.

        Args:
            font_family: Font family name
            font_size: Font size in pixels

        Returns:
            PIL ImageFont object
        """
        cache_key = f"{font_family}_{font_size}"

        if cache_key in self._fonts_cache:
            return self._fonts_cache[cache_key]

        font_path = get_font_path(font_family)

        # Try custom font path
        if font_path and os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                self._fonts_cache[cache_key] = font
                logger.debug("Loaded custom font", font=font_family, size=font_size)
                return font
            except OSError as e:
                logger.warning("Failed to load custom font", font=font_family, error=str(e))

        # Try system font paths (for local development)
        system_font_paths = [
            f"/usr/share/fonts/truetype/google/{font_family.replace(' ', '')}-Regular.ttf",
            f"/System/Library/Fonts/{font_family.replace(' ', '')}.ttf",
            f"C:/Windows/Fonts/{font_family.replace(' ', '')}.ttf",
            f"C:/Windows/Fonts/{font_family.replace(' ', '').lower()}.ttf",
        ]

        for path in system_font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, font_size)
                    self._fonts_cache[cache_key] = font
                    logger.debug("Loaded system font", font=font_family, path=path)
                    return font
                except OSError:
                    continue

        # Fallback to default font
        logger.warning("Using default font as fallback", requested_font=font_family)
        try:
            # Try to load a decent fallback
            fallback_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "/System/Library/Fonts/Times.ttc",
                "C:/Windows/Fonts/times.ttf",
            ]
            for path in fallback_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, font_size)
                    self._fonts_cache[cache_key] = font
                    return font
        except OSError:
            pass

        # Ultimate fallback - try to use a basic TrueType font
        logger.error(
            "CRITICAL: Failed to load custom fonts - using system fallback",
            requested_font=font_family,
            requested_size=font_size,
            warning="Text may not render as expected. Check font files at /app/fonts/"
        )

        # Try common system fonts as last resort
        system_fallbacks = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            "/System/Library/Fonts/Times.ttc",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/georgia.ttf",
        ]

        for fallback_path in system_fallbacks:
            if os.path.exists(fallback_path):
                try:
                    font = ImageFont.truetype(fallback_path, font_size)
                    self._fonts_cache[cache_key] = font
                    logger.warning(
                        "Using system fallback font",
                        fallback_path=fallback_path,
                        requested_font=font_family
                    )
                    return font
                except OSError:
                    continue

        # Absolute last resort - PIL default (but log critical error)
        logger.critical(
            "NO FONTS AVAILABLE - using PIL default (will look bad)",
            requested_font=font_family,
            requested_size=font_size
        )
        font = ImageFont.load_default()
        self._fonts_cache[cache_key] = font
        return font

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _hex_to_rgba(self, hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
        """Convert hex color to RGBA tuple."""
        rgb = self._hex_to_rgb(hex_color)
        return (*rgb, alpha)

    def _wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int
    ) -> List[str]:
        """
        Wrap text to fit within max width.

        Handles paragraphs (newlines) and word wrapping.

        Args:
            text: Text to wrap
            font: Font to measure with
            max_width: Maximum width in pixels

        Returns:
            List of wrapped lines
        """
        lines = []
        paragraphs = text.split('\n')

        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")
                continue

            words = paragraph.split()
            if not words:
                lines.append("")
                continue

            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]

                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

        return lines

    def _calculate_text_height(
        self,
        lines: List[str],
        font: ImageFont.FreeTypeFont,
        line_height_multiplier: float
    ) -> int:
        """Calculate total height of text block."""
        if not lines:
            return 0

        # Get font metrics
        bbox = font.getbbox("Ay")  # Use chars with ascenders and descenders
        single_line_height = bbox[3] - bbox[1]
        line_height = int(single_line_height * line_height_multiplier)

        return line_height * len(lines)

    def _draw_shadow_text(
        self,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        text_color: Tuple[int, int, int, int],
        shadow_config: Optional[dict]
    ) -> None:
        """
        Draw text with optional shadow effect.

        Args:
            draw: PIL ImageDraw object
            position: (x, y) position for text
            text: Text to draw
            font: Font to use
            text_color: RGBA text color
            shadow_config: Shadow configuration dict or None
        """
        x, y = position

        # Draw shadow first (behind text)
        if shadow_config:
            shadow_color = self._hex_to_rgba(
                shadow_config.get("color", "#000000"),
                int(255 * shadow_config.get("opacity", 0.15))
            )
            shadow_x = x + shadow_config.get("offset_x", 1)
            shadow_y = y + shadow_config.get("offset_y", 2)

            # For blur effect, draw multiple times with offset
            blur = shadow_config.get("blur", 2)
            if blur > 0:
                for dx in range(-blur, blur + 1):
                    for dy in range(-blur, blur + 1):
                        # Fade based on distance from center
                        distance = (dx * dx + dy * dy) ** 0.5
                        if distance <= blur:
                            alpha_mult = 1 - (distance / (blur + 1))
                            faded_alpha = int(shadow_color[3] * alpha_mult * 0.3)
                            faded_color = (*shadow_color[:3], faded_alpha)
                            draw.text(
                                (shadow_x + dx, shadow_y + dy),
                                text,
                                font=font,
                                fill=faded_color
                            )
            else:
                draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)

        # Draw main text
        draw.text(position, text, font=font, fill=text_color)

    def _draw_text_bubble(
        self,
        page_size: Tuple[int, int],
        text_bounds: Tuple[int, int, int, int],
        bubble_config: dict,
    ) -> Image.Image:
        """
        Draw a soft, kid-friendly bubble behind the text area.

        Creates a rounded rectangle with blurred edges that looks like
        a pillowy cloud/thought bubble — fun and readable.

        Args:
            page_size: (width, height) of the page
            text_bounds: (x1, y1, x2, y2) bounding box of the text block
            bubble_config: BubbleConfig dict with color, opacity, radius, etc.

        Returns:
            RGBA Image layer with the bubble drawn on it
        """
        width, height = page_size
        x1, y1, x2, y2 = text_bounds

        # Expand bounds by padding
        pad_x = bubble_config.get("padding_x", 100)
        pad_y = bubble_config.get("padding_y", 60)

        bx1 = max(0, x1 - pad_x)
        by1 = max(0, y1 - pad_y)
        bx2 = min(width, x2 + pad_x)
        by2 = min(height, y2 + pad_y)

        # Parse color and opacity
        hex_color = bubble_config.get("color", "#FFFFFF")
        opacity = bubble_config.get("opacity", 0.65)
        corner_radius = bubble_config.get("corner_radius", 100)
        blur_edge = bubble_config.get("blur_edge", 10)

        rgb = self._hex_to_rgb(hex_color)
        alpha = int(255 * opacity)
        fill_color = (*rgb, alpha)

        # Create bubble on a separate RGBA layer
        bubble_layer = Image.new("RGBA", page_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(bubble_layer)

        # Draw the rounded rectangle (pillow shape)
        draw.rounded_rectangle(
            [(bx1, by1), (bx2, by2)],
            radius=corner_radius,
            fill=fill_color,
        )

        # Soften edges with Gaussian blur for that dreamy pillow feel
        if blur_edge > 0:
            bubble_layer = bubble_layer.filter(
                ImageFilter.GaussianBlur(radius=blur_edge)
            )

        logger.debug(
            "Drew text bubble",
            bounds=(bx1, by1, bx2, by2),
            color=hex_color,
            opacity=opacity,
            corner_radius=corner_radius,
        )

        return bubble_layer

    async def overlay_text(
        self,
        background_url: str,
        text: str,
        theme: str,
        page_type: str,  # 'dedication' or 'story'
        text_page_number: Optional[int] = None,
        child_name: Optional[str] = None
    ) -> bytes:
        """
        Overlay text on a filler image with premium styling.

        Args:
            background_url: R2 URL of the filler image
            text: Text content to overlay (ignored for dedication if child_name provided)
            theme: Theme identifier (e.g., 'storygift_enchanted_forest')
            page_type: 'dedication' or 'story'
            text_page_number: For story pages, which text page (1-10)
            child_name: For dedication page, child's name for personalization

        Returns:
            PNG image bytes with text overlay
        """
        logger.info(
            "Processing text overlay",
            theme=theme,
            page_type=page_type,
            text_page_number=text_page_number,
            background_url=background_url[:80] if background_url else None
        )

        # Fetch background image
        try:
            image_bytes = await self.storage.download_image(background_url)
            background = Image.open(BytesIO(image_bytes)).convert("RGBA")
        except Exception as e:
            logger.error("Failed to fetch background image", url=background_url, error=str(e))
            raise

        width, height = background.size

        # Normalize image dimensions for consistent text rendering
        # This fixes the inconsistent text issue caused by varying filler image sizes
        if width != DEFAULT_PAGE_WIDTH or height != DEFAULT_PAGE_HEIGHT:
            logger.info(
                "Normalizing filler image dimensions for consistent text rendering",
                original_size=f"{width}×{height}",
                normalized_size=f"{DEFAULT_PAGE_WIDTH}×{DEFAULT_PAGE_HEIGHT}",
                background_url=background_url[:100],
                page_type=page_type,
                text_page_number=text_page_number
            )

            # Resize to standard dimensions using high-quality Lanczos resampling
            resized_background = background.resize(
                (DEFAULT_PAGE_WIDTH, DEFAULT_PAGE_HEIGHT),
                Image.Resampling.LANCZOS
            )
            background.close()
            background = resized_background
            width, height = DEFAULT_PAGE_WIDTH, DEFAULT_PAGE_HEIGHT

        # Get text styling configuration
        text_config = get_text_config(theme, page_type)

        # Handle dedication page text generation
        if page_type == "dedication" and child_name:
            text = get_dedication_text(child_name)

        if not text or not text.strip():
            logger.warning("No text to overlay, returning original image")
            output = BytesIO()
            rgb_bg = background.convert("RGB")
            rgb_bg.save(output, format="PNG", quality=95)
            rgb_bg.close()
            output.seek(0)
            background.close()
            return output.getvalue()

        # Get colors (page-specific for story pages)
        color = text_config.get("color", "#000000")
        shadow_config = text_config.get("shadow")

        if page_type == "story" and text_page_number:
            page_colors = get_page_specific_colors(theme, text_page_number)
            if page_colors:
                color = page_colors.get("color", color)
                if shadow_config and "shadow_color" in page_colors:
                    shadow_config = shadow_config.copy()
                    shadow_config["color"] = page_colors["shadow_color"]

        # Create text layer
        text_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        # Load font
        font = self._load_font(
            text_config.get("font_family", "Playfair Display"),
            text_config.get("font_size", 32)
        )

        # Calculate text area
        max_width_percent = text_config.get("max_width_percent", 75)
        max_text_width = int(width * max_width_percent / 100)

        # Wrap text
        lines = self._wrap_text(text, font, max_text_width)

        # Calculate line height
        line_height_multiplier = text_config.get("line_height", 1.8)
        bbox = font.getbbox("Ay")
        single_line_height = bbox[3] - bbox[1]
        line_height = int(single_line_height * line_height_multiplier)

        # Calculate total text height
        total_height = line_height * len(lines)

        # Calculate starting Y position (center by default)
        vertical_position = text_config.get("vertical_position", "center")
        if vertical_position == "center":
            start_y = (height - total_height) // 2
        elif vertical_position == "top":
            start_y = int(height * 0.15)
        else:  # bottom
            start_y = height - total_height - int(height * 0.15)

        # Get alignment
        alignment = text_config.get("alignment", TextAlignment.CENTER)
        if isinstance(alignment, str):
            alignment = TextAlignment(alignment)

        # Convert color
        text_color = self._hex_to_rgba(color)

        # Handle drop cap for story pages
        drop_cap_config = text_config.get("drop_cap")
        has_drop_cap = (
            page_type == "story" and
            drop_cap_config and
            drop_cap_config.get("enabled", False) and
            lines and
            lines[0] and
            lines[0][0].isalpha()
        )

        # Draw fun bubble behind text for readability
        bubble_config = text_config.get("bubble")
        if bubble_config and bubble_config.get("enabled"):
            # Calculate text bounding box for bubble sizing
            # Account for drop cap overshoot on the left/top
            margin = (width - max_text_width) // 2
            text_x1 = margin
            text_x2 = width - margin
            text_y1 = start_y
            text_y2 = start_y + total_height

            # If drop cap exists, extend the top a bit for the large letter
            if has_drop_cap:
                drop_cap_font_size = drop_cap_config.get("font_size", 240)
                text_y1 = min(text_y1, start_y - int(drop_cap_font_size * 0.1))

            bubble_layer = self._draw_text_bubble(
                page_size=(width, height),
                text_bounds=(text_x1, text_y1, text_x2, text_y2),
                bubble_config=bubble_config,
            )
            background = Image.alpha_composite(background, bubble_layer)
            bubble_layer.close()

        # Draw each line
        current_y = start_y

        for i, line in enumerate(lines):
            if not line:
                current_y += line_height
                continue

            # Calculate line width for alignment
            line_bbox = font.getbbox(line)
            line_width = line_bbox[2] - line_bbox[0]

            # Calculate X position
            margin = (width - max_text_width) // 2
            if alignment == TextAlignment.CENTER:
                x = (width - line_width) // 2
            elif alignment == TextAlignment.RIGHT:
                x = width - line_width - margin
            else:  # LEFT or JUSTIFY
                x = margin

            # Handle drop cap for first line
            if i == 0 and has_drop_cap:
                first_char = line[0].upper()
                remaining_text = line[1:] if len(line) > 1 else ""

                # Load drop cap font
                drop_cap_font = self._load_font(
                    drop_cap_config.get("font_family", "Cormorant Garamond Bold"),
                    drop_cap_config.get("font_size", 96)
                )

                # Get drop cap dimensions
                cap_bbox = drop_cap_font.getbbox(first_char)
                cap_width = cap_bbox[2] - cap_bbox[0]
                cap_height = cap_bbox[3] - cap_bbox[1]

                # Position drop cap
                cap_color = self._hex_to_rgba(drop_cap_config.get("color", color))

                # Draw drop cap (slightly lower to align with text baseline)
                cap_y = current_y - int(cap_height * 0.1)
                self._draw_shadow_text(
                    draw,
                    (x, cap_y),
                    first_char,
                    drop_cap_font,
                    cap_color,
                    shadow_config
                )

                # Draw remaining text on first line (offset by drop cap width)
                if remaining_text.strip():
                    remaining_x = x + cap_width + 10
                    self._draw_shadow_text(
                        draw,
                        (remaining_x, current_y),
                        remaining_text.lstrip(),
                        font,
                        text_color,
                        shadow_config
                    )
            else:
                # Draw regular line
                self._draw_shadow_text(
                    draw,
                    (x, current_y),
                    line,
                    font,
                    text_color,
                    shadow_config
                )

            current_y += line_height

        # Composite text layer onto background
        result = Image.alpha_composite(background, text_layer)

        # Convert to bytes
        output = BytesIO()
        rgb_result = result.convert("RGB")
        rgb_result.save(output, format="PNG", quality=95)
        rgb_result.close()
        
        output.seek(0)
        
        # Free memory explicitly
        background.close()
        text_layer.close()
        result.close()
        
        import gc
        gc.collect()

        logger.info(
            "Text overlay complete",
            theme=theme,
            page_type=page_type,
            output_size=len(output.getvalue())
        )

        return output.getvalue()

    async def process_dedication_page(
        self,
        background_url: str,
        child_name: str,
        theme: str
    ) -> bytes:
        """
        Process dedication page with personalized text.

        Args:
            background_url: R2 URL of dedication.png filler
            child_name: Child's name for personalization
            theme: Theme identifier

        Returns:
            PNG image bytes with dedication text overlay
        """
        return await self.overlay_text(
            background_url=background_url,
            text="",  # Will be generated from template
            theme=theme,
            page_type="dedication",
            child_name=child_name
        )

    async def process_story_text_page(
        self,
        background_url: str,
        story_text: str,
        theme: str,
        text_page_number: int
    ) -> bytes:
        """
        Process a story text page with text overlay.

        Args:
            background_url: R2 URL of textN.png filler
            story_text: Story text content for this page
            theme: Theme identifier
            text_page_number: Which text page (1-10)

        Returns:
            PNG image bytes with story text overlay
        """
        return await self.overlay_text(
            background_url=background_url,
            text=story_text,
            theme=theme,
            page_type="story",
            text_page_number=text_page_number
        )

    def _get_adaptive_cover_font(
        self,
        text: str,
        base_font_size: int,
        font_family: str,
        letter_spacing: int,
        max_allowed_width: int,
        draw: ImageDraw.Draw
    ) -> Tuple[ImageFont.FreeTypeFont, int]:
        """Dynamically scale down font if it exceeds max width to prevent overflow."""
        font_size = base_font_size
        while font_size > 20:
            font = self._load_font(font_family, font_size)
            total_width = 0
            for char in text:
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_width = int(char_bbox[2] - char_bbox[0])
                total_width += char_width + letter_spacing
            if text:
                total_width -= letter_spacing
            
            if total_width <= max_allowed_width:
                return font, total_width
            
            # Reduce size to fit
            font_size -= 5
            
        # Fallback
        font = self._load_font(font_family, font_size)
        return font, max_allowed_width

    async def process_cover_page(
        self,
        cover_image_url: str,
        story_title: str,
        child_name: str
    ) -> bytes:
        """
        Process cover page with title and starring text overlay.

        Adds:
        - Top gradient (33% height): Theme title with gold gradient effect
        - Bottom gradient (25% height): "STARRING" label + child name

        Args:
            cover_image_url: URL of AI-generated cover image
            story_title: Theme title (e.g., "Enchanted Forest")
            child_name: Child's name for "Starring" credit

        Returns:
            PNG image bytes with text overlays
        """
        logger.info(
            "Processing cover page with text overlay",
            story_title=story_title,
            child_name=child_name,
            cover_url=cover_image_url[:80] if cover_image_url else None
        )

        # Fetch cover image
        try:
            image_bytes = await self.storage.download_image(cover_image_url)
            cover_image = Image.open(BytesIO(image_bytes)).convert("RGBA")
        except Exception as e:
            logger.error("Failed to fetch cover image", url=cover_image_url, error=str(e))
            raise

        width, height = cover_image.size

        # Normalize cover image dimensions for consistency
        if width != DEFAULT_PAGE_WIDTH or height != DEFAULT_PAGE_HEIGHT:
            logger.info(
                "Normalizing cover image dimensions",
                original_size=f"{width}×{height}",
                normalized_size=f"{DEFAULT_PAGE_WIDTH}×{DEFAULT_PAGE_HEIGHT}",
                cover_url=cover_image_url[:100]
            )

            resized_cover = cover_image.resize(
                (DEFAULT_PAGE_WIDTH, DEFAULT_PAGE_HEIGHT),
                Image.Resampling.LANCZOS
            )
            cover_image.close()
            cover_image = resized_cover
            width, height = DEFAULT_PAGE_WIDTH, DEFAULT_PAGE_HEIGHT

        # Create overlay layer for gradients and text
        overlay = Image.new("RGBA", cover_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # ============================================
        # TOP GRADIENT (33% height) with title
        # ============================================
        top_gradient_height = int(height * 0.33)

        # Create gradient from black (top) to transparent (bottom)
        for y in range(top_gradient_height):
            # Opacity decreases from top to bottom
            alpha = int(180 * (1 - y / top_gradient_height))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        # Maximum width constraint (90% of page) to guarantee NO overflow
        max_cover_text_width = int(width * 0.90)

        # Load adaptive premium title font (Cormorant Garamond Bold for luxury feel)
        story_title_upper = story_title.upper()
        title_letter_spacing = int(16)  # Premium letter-spacing in pixels appropriate for 300DPI
        
        title_font, total_title_width = self._get_adaptive_cover_font(
            text=story_title_upper,
            base_font_size=240,
            font_family="Cormorant Garamond Bold",
            letter_spacing=title_letter_spacing,
            max_allowed_width=max_cover_text_width,
            draw=draw
        )

        # Center horizontally, position higher to prevent overflow (10% from top)
        title_x = (width - total_title_width) // 2
        title_y = int(height * 0.10)

        # Premium antique gold color (more sophisticated than bright yellow)
        gold_color = (212, 175, 55, 255)  # #D4AF37 - antique gold

        # Draw title with letter-spacing and stroke for premium depth
        current_x = title_x
        for char in story_title_upper:
            char_bbox = draw.textbbox((0, 0), char, font=title_font)
            char_width = int(char_bbox[2] - char_bbox[0])

            # Draw text stroke (white outline for depth, adjusted for huge sizes)
            stroke_width = int(4)
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx*dx + dy*dy <= stroke_width*stroke_width:
                        draw.text(
                            (current_x + dx, title_y + dy),
                            char,
                            font=title_font,
                            fill=(255, 255, 255, 80)  # Semi-transparent white stroke
                        )

            # Draw bold drop shadow
            shadow_offset = int(8)
            draw.text(
                (current_x + shadow_offset, title_y + shadow_offset),
                char,
                font=title_font,
                fill=(0, 0, 0, 180)
            )

            # Draw main character in antique gold
            draw.text(
                (current_x, title_y),
                char,
                font=title_font,
                fill=gold_color
            )

            current_x += char_width + title_letter_spacing

        # ============================================
        # BOTTOM GRADIENT (25% height) with starring
        # ============================================
        bottom_gradient_height = int(height * 0.25)
        bottom_start = height - bottom_gradient_height

        # Create gradient from transparent (top) to black (bottom)
        for y in range(bottom_gradient_height):
            # Opacity increases from top to bottom
            alpha = int(220 * (y / bottom_gradient_height))
            actual_y = bottom_start + y
            draw.line([(0, actual_y), (width, actual_y)], fill=(0, 0, 0, alpha))

        # "STARRING" label with letter-spacing and adaptive scaling
        starring_text = "STARRING"
        starring_letter_spacing = int(12)
        starring_label_font, total_starring_width = self._get_adaptive_cover_font(
            text=starring_text,
            base_font_size=80,
            font_family="Cormorant Garamond Bold",
            letter_spacing=starring_letter_spacing,
            max_allowed_width=max_cover_text_width,
            draw=draw
        )

        starring_x = (width - total_starring_width) // 2
        starring_y = height - int(height * 0.16)  # 16% from bottom

        # Draw starring label
        current_x = starring_x
        for char in starring_text:
            char_bbox = draw.textbbox((0, 0), char, font=starring_label_font)
            char_width = int(char_bbox[2] - char_bbox[0])

            draw.text(
                (current_x, starring_y),
                char,
                font=starring_label_font,
                fill=(255, 255, 255, 180)  # Semi-transparent white
            )

            current_x += char_width + starring_letter_spacing

        # Child name (bold, uppercase) with luxury letter spacing & adaptive scaling
        child_name_upper = child_name.upper()
        name_letter_spacing = int(16)
        
        child_name_font, total_name_width = self._get_adaptive_cover_font(
            text=child_name_upper,
            base_font_size=140,
            font_family="Cormorant Garamond Bold",
            letter_spacing=name_letter_spacing,
            max_allowed_width=max_cover_text_width,
            draw=draw
        )

        name_x = (width - total_name_width) // 2
        name_y = height - int(height * 0.09)  # 9% from bottom

        # Draw name with letter-spacing and stroke for depth
        current_x = name_x
        for char in child_name_upper:
            char_bbox = draw.textbbox((0, 0), char, font=child_name_font)
            char_width = int(char_bbox[2] - char_bbox[0])

            # Draw bold text stroke (subtle outline)
            stroke_width = int(4)
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx*dx + dy*dy <= stroke_width*stroke_width:
                        draw.text(
                            (current_x + dx, name_y + dy),
                            char,
                            font=child_name_font,
                            fill=(200, 200, 200, 60)  # Subtle gray stroke
                        )

            # Draw bold shadow
            draw.text(
                (current_x + 4, name_y + 4),
                char,
                font=child_name_font,
                fill=(0, 0, 0, 200)
            )

            # Draw main text in bright white
            draw.text(
                (current_x, name_y),
                char,
                font=child_name_font,
                fill=(255, 255, 255, 255)  # Brilliant white
            )

            current_x += char_width + name_letter_spacing

        # Composite overlay onto cover
        result = Image.alpha_composite(cover_image, overlay)

        # Convert to bytes
        output = BytesIO()
        rgb_result = result.convert("RGB")
        rgb_result.save(output, format="PNG", quality=95)
        rgb_result.close()
        
        output.seek(0)

        # Free memory explicitly
        cover_image.close()
        overlay.close()
        result.close()
        
        import gc
        gc.collect()

        logger.info(
            "Cover text overlay complete",
            story_title=story_title,
            child_name=child_name,
            output_size=len(output.getvalue())
        )

        return output.getvalue()


# Module-level singleton instance
_image_processor: Optional[ImageProcessor] = None


def get_image_processor() -> ImageProcessor:
    """Get or create the ImageProcessor singleton."""
    global _image_processor
    if _image_processor is None:
        _image_processor = ImageProcessor()
    return _image_processor
