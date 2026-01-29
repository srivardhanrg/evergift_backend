"""
StoryGift-style PDF Generator Service.

Pure ReportLab approach for production-ready PDF generation:
- Direct image + text → PDF (no browser needed)
- 10x10 inch square pages matching frontend preview
- 80% image area / 20% text area layout
- Fast (~2-5 seconds for 10 pages)
"""

import asyncio
import os
import tempfile
from io import BytesIO
from typing import List, Dict, Optional, Any
import structlog
import httpx
from PIL import Image

from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import Color, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from app.config import get_settings
from app.core.exceptions import StorageError
from app.services.storage import StorageService

logger = structlog.get_logger()

# Page dimensions: 10x10 inch square
PAGE_WIDTH = 10 * inch
PAGE_HEIGHT = 10 * inch

# Layout: 80% image, 20% text
IMAGE_HEIGHT = 8 * inch  # 80% of page
TEXT_HEIGHT = 2 * inch   # 20% of page


class StoryGiftPDFGeneratorService:
    """
    PDF Generator using pure ReportLab approach.

    Flow:
    1. Download images from R2 storage
    2. Create PDF with ReportLab
    3. For each page: draw image (80%) + text (20%)
    4. Upload to R2 and return URL
    """

    def __init__(self):
        self.settings = get_settings()
        self.storage = StorageService()
        logger.info("StoryGift PDF generator initialized (ReportLab-only)")

    async def generate_storygift_pdf(
        self,
        preview_id: str,
        child_name: str,
        story_pages: List[Dict[str, Any]],
        story_title: str,
        cover_image_url: Optional[str] = None
    ) -> str:
        """
        Generate StoryGift-style PDF from story pages.

        Args:
            preview_id: Preview ID for storage paths
            child_name: Child's name for personalization
            story_pages: List of page data with image_url, story_text
            story_title: Story title for cover page
            cover_image_url: Optional cover image URL

        Returns:
            PDF file URL in storage
        """
        try:
            logger.info(
                "Starting ReportLab PDF generation",
                preview_id=preview_id,
                child_name=child_name,
                page_count=len(story_pages)
            )

            # Download all images first
            page_images = await self._download_all_images(story_pages, cover_image_url)

            # Generate PDF
            pdf_bytes = self._create_pdf(
                story_pages=story_pages,
                page_images=page_images,
                child_name=child_name,
                story_title=story_title,
                cover_image=page_images.get('cover')
            )

            # Upload to storage
            storage_path = f"final/{preview_id}/storygift_book.pdf"
            pdf_url = await self.storage.upload_pdf(pdf_bytes, storage_path)

            logger.info(
                "PDF generated successfully",
                preview_id=preview_id,
                pdf_url=pdf_url,
                page_count=len(story_pages),
                size_bytes=len(pdf_bytes)
            )

            return pdf_url

        except Exception as e:
            logger.error(
                "PDF generation failed",
                preview_id=preview_id,
                error=str(e)
            )
            raise StorageError(f"PDF generation failed: {str(e)}")

    async def _download_all_images(
        self,
        story_pages: List[Dict[str, Any]],
        cover_image_url: Optional[str]
    ) -> Dict[str, bytes]:
        """Download all images concurrently for faster processing."""
        images = {}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Download cover image
            if cover_image_url:
                try:
                    response = await client.get(cover_image_url)
                    response.raise_for_status()
                    images['cover'] = response.content
                    logger.info("Cover image downloaded")
                except Exception as e:
                    logger.warning(f"Failed to download cover image: {e}")

            # Download page images
            for i, page in enumerate(story_pages):
                page_num = page.get('page', i + 1)
                image_url = page.get('image_url', '')
                
                if image_url:
                    try:
                        response = await client.get(image_url)
                        response.raise_for_status()
                        images[f'page_{page_num}'] = response.content
                    except Exception as e:
                        logger.warning(f"Failed to download page {page_num} image: {e}")

        logger.info(f"Downloaded {len(images)} images for PDF")
        return images

    def _create_pdf(
        self,
        story_pages: List[Dict[str, Any]],
        page_images: Dict[str, bytes],
        child_name: str,
        story_title: str,
        cover_image: Optional[bytes] = None
    ) -> bytes:
        """Create the PDF using ReportLab canvas for precise control."""
        
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Create canvas
            c = canvas.Canvas(tmp_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
            
            # Generate cover page if we have a cover image
            if cover_image:
                self._draw_cover_page(c, cover_image, story_title, child_name)
                c.showPage()

            # Generate story pages
            for i, page_data in enumerate(story_pages):
                page_num = page_data.get('page', i + 1)
                story_text = page_data.get('story_text', page_data.get('text', ''))
                image_bytes = page_images.get(f'page_{page_num}')
                
                self._draw_story_page(c, image_bytes, story_text, page_num)
                
                # Add page break (except for last page)
                if i < len(story_pages) - 1:
                    c.showPage()

            c.save()

            # Read the generated PDF
            with open(tmp_path, 'rb') as f:
                pdf_bytes = f.read()

            return pdf_bytes

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def _draw_cover_page(
        self,
        c: canvas.Canvas,
        cover_image: bytes,
        story_title: str,
        child_name: str
    ):
        """Draw premium cover page matching the Enchanted Forest sample style.
        
        Premium features:
        - Elegant serif font (Times-Roman) for title with letter spacing
        - Subtle gradient overlays (no harsh black bars)
        - Thin gold decorative line separator
        - Letter-spaced "STARRING" label
        - Clean, premium typography
        """
        try:
            # Load and draw cover image to fill entire page
            img = Image.open(BytesIO(cover_image))
            img_reader = ImageReader(img)
            
            # Draw image edge-to-edge (1:1 image on 10x10" page = perfect fit)
            c.drawImage(
                img_reader,
                0, 0,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                preserveAspectRatio=False
            )

            # Extract display title (remove child name prefix)
            display_title = story_title
            if child_name.lower() in story_title.lower():
                import re
                patterns = [
                    rf"{re.escape(child_name)}'?s?\s*",
                    rf"{re.escape(child_name)}\s+and\s+the\s+",
                    r"^and\s+the\s+",
                ]
                for pattern in patterns:
                    display_title = re.sub(pattern, '', display_title, flags=re.IGNORECASE)
                display_title = display_title.strip()

            # =========================================================
            # TOP GRADIENT OVERLAY - Subtle and smooth (no harsh bars)
            # Much lighter than before to avoid "black bar" appearance
            # =========================================================
            c.saveState()
            
            # Subtle gradient: only 25% of page height, lighter opacity
            top_gradient_height = PAGE_HEIGHT * 0.25
            num_layers = 15
            stripe_height = top_gradient_height / num_layers
            
            for i in range(num_layers):
                # Start at 50% opacity and fade to transparent (gentler than before)
                progress = i / num_layers
                alpha = 0.50 * (1 - progress) ** 1.5  # Exponential falloff for smoother fade
                
                y_pos = PAGE_HEIGHT - (i + 1) * stripe_height
                c.setFillColor(Color(0, 0, 0, alpha=alpha))
                c.rect(0, y_pos, PAGE_WIDTH, stripe_height + 1, fill=1, stroke=0)
            
            c.restoreState()

            # =========================================================
            # TITLE TEXT - Premium serif font with letter spacing
            # Matching the Enchanted Forest elegant style
            # =========================================================
            c.saveState()
            
            # Use Times-Bold for elegant serif look (built-in ReportLab font)
            title_upper = display_title.upper()
            title_y = PAGE_HEIGHT - 0.85 * inch
            
            # Calculate base font size
            base_font_size = 52
            c.setFont("Times-Bold", base_font_size)
            
            # Measure and adjust for long titles
            title_width = c.stringWidth(title_upper, "Times-Bold", base_font_size)
            if title_width > PAGE_WIDTH - 80:
                base_font_size = 44
            title_width = c.stringWidth(title_upper, "Times-Bold", base_font_size)
            if title_width > PAGE_WIDTH - 80:
                base_font_size = 36
            
            # Letter spacing effect (draw each character individually)
            letter_spacing = 4  # pixels between letters
            total_width = 0
            
            for char in title_upper:
                total_width += c.stringWidth(char, "Times-Bold", base_font_size) + letter_spacing
            total_width -= letter_spacing  # Remove last spacing
            
            # Check if we need to split into two lines
            if total_width > PAGE_WIDTH - 60:
                # Split title into two lines at natural break point
                words = title_upper.split()
                if len(words) >= 2:
                    mid = len(words) // 2
                    line1 = " ".join(words[:mid])
                    line2 = " ".join(words[mid:])
                    
                    # Draw line 1

                    self._draw_letter_spaced_text(c, line1, "Times-Bold", base_font_size, 
                                                  title_y + 35, letter_spacing,
                                                  Color(218/255, 165/255, 32/255))  # Golden color
                    # Draw line 2
                    self._draw_letter_spaced_text(c, line2, "Times-Bold", base_font_size,
                                                  title_y - 10, letter_spacing,
                                                  Color(218/255, 165/255, 32/255))
                else:
                    # Single word, just draw it
                    self._draw_letter_spaced_text(c, title_upper, "Times-Bold", base_font_size,
                                                  title_y, letter_spacing,
                                                  Color(218/255, 165/255, 32/255))
            else:
                # Single line title
                self._draw_letter_spaced_text(c, title_upper, "Times-Bold", base_font_size,
                                              title_y, letter_spacing,
                                              Color(218/255, 165/255, 32/255))
            
            c.restoreState()

            # =========================================================
            # BOTTOM GRADIENT OVERLAY - Subtle fade for text readability
            # =========================================================
            c.saveState()
            
            bottom_gradient_height = PAGE_HEIGHT * 0.20
            num_layers = 12
            stripe_height = bottom_gradient_height / num_layers
            
            for i in range(num_layers):
                # Fade from bottom (0.6 opacity) to transparent
                progress = i / num_layers
                alpha = 0.60 * (1 - progress) ** 1.5
                
                y_pos = i * stripe_height
                c.setFillColor(Color(0, 0, 0, alpha=alpha))
                c.rect(0, y_pos, PAGE_WIDTH, stripe_height + 1, fill=1, stroke=0)
            
            c.restoreState()

            # =========================================================
            # THIN GOLD DECORATIVE LINE - Premium separator
            # =========================================================
            c.saveState()
            c.setStrokeColor(Color(218/255, 165/255, 32/255, alpha=0.7))  # Golden, slightly transparent
            c.setLineWidth(1)
            line_y = 1.0 * inch
            line_width = 2.5 * inch
            c.line((PAGE_WIDTH - line_width) / 2, line_y, (PAGE_WIDTH + line_width) / 2, line_y)
            c.restoreState()

            # =========================================================
            # "STARRING" LABEL - Letter-spaced, elegant
            # =========================================================
            c.saveState()
            starring_text = "STARRING"
            starring_size = 11
            starring_spacing = 6  # Wide letter spacing for premium feel
            starring_y = 0.75 * inch
            
            self._draw_letter_spaced_text(c, starring_text, "Helvetica", starring_size,
                                          starring_y, starring_spacing,
                                          Color(0.75, 0.75, 0.75))  # Light gray
            c.restoreState()

            # =========================================================
            # CHILD NAME - Premium serif, white with subtle shadow
            # =========================================================
            c.saveState()
            name_upper = child_name.upper()
            name_font_size = 30
            name_y = 0.35 * inch
            name_spacing = 3
            
            # Calculate width for centering
            c.setFont("Times-Bold", name_font_size)
            
            # Draw subtle shadow first
            self._draw_letter_spaced_text(c, name_upper, "Times-Bold", name_font_size,
                                          name_y - 1, name_spacing,
                                          Color(0, 0, 0, alpha=0.4), shadow_offset=1.5)
            
            # Draw main name in white
            self._draw_letter_spaced_text(c, name_upper, "Times-Bold", name_font_size,
                                          name_y, name_spacing,
                                          white)
            c.restoreState()

        except Exception as e:
            logger.error(f"Failed to draw cover page: {e}")
            # Draw a fallback cover
            c.setFillColor(Color(0.4, 0.2, 0.6))
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
            c.setFillColor(white)
            c.setFont("Times-Bold", 48)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2, story_title)

    def _draw_letter_spaced_text(
        self,
        c: canvas.Canvas,
        text: str,
        font_name: str,
        font_size: float,
        y_pos: float,
        letter_spacing: float,
        color: Color,
        shadow_offset: float = 0
    ):
        """Draw text with letter spacing, centered on page."""
        c.setFont(font_name, font_size)
        
        # Calculate total width with spacing
        total_width = 0
        for char in text:
            total_width += c.stringWidth(char, font_name, font_size) + letter_spacing
        total_width -= letter_spacing  # Remove last spacing
        
        # Start position for centering
        x_pos = (PAGE_WIDTH - total_width) / 2 + shadow_offset
        
        c.setFillColor(color)
        
        # Draw each character
        for char in text:
            char_width = c.stringWidth(char, font_name, font_size)
            c.drawString(x_pos, y_pos, char)
            x_pos += char_width + letter_spacing

    def _draw_story_page(
        self,
        c: canvas.Canvas,
        image_bytes: Optional[bytes],
        story_text: str,
        page_num: int
    ):
        """Draw a story page with image (top 80%) and text (bottom 20%)."""
        
        # Background
        c.setFillColor(white)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        # Draw image in top 80%
        if image_bytes:
            try:
                img = Image.open(BytesIO(image_bytes))
                img_reader = ImageReader(img)
                
                # Image area: top 80% of page
                img_y = TEXT_HEIGHT  # Start above text area
                
                c.drawImage(
                    img_reader,
                    0, img_y,  # x, y (bottom-left of image area)
                    width=PAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    preserveAspectRatio=True,
                    anchor='c'  # Center the image
                )
            except Exception as e:
                logger.error(f"Failed to draw image for page {page_num}: {e}")
                # Draw placeholder
                c.setFillColor(Color(0.95, 0.95, 0.95))
                c.rect(0, TEXT_HEIGHT, PAGE_WIDTH, IMAGE_HEIGHT, fill=1, stroke=0)
                c.setFillColor(Color(0.7, 0.7, 0.7))
                c.setFont("Helvetica", 24)
                c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 + inch, f"Page {page_num}")
        else:
            # No image - draw placeholder
            c.setFillColor(Color(0.95, 0.95, 0.95))
            c.rect(0, TEXT_HEIGHT, PAGE_WIDTH, IMAGE_HEIGHT, fill=1, stroke=0)

        # Draw border line between image and text
        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        c.setLineWidth(1)
        c.line(0, TEXT_HEIGHT, PAGE_WIDTH, TEXT_HEIGHT)

        # Draw text in bottom 20%
        self._draw_story_text(c, story_text, page_num)

    def _draw_story_text(self, c: canvas.Canvas, story_text: str, page_num: int):
        """Draw the story text in the bottom 20% of the page."""
        if not story_text:
            # No text - draw decorative dots
            c.setFillColor(Color(0.6, 0.65, 0.7))
            c.setFont("Helvetica", 14)
            c.drawCentredString(PAGE_WIDTH/2, TEXT_HEIGHT/2, "• • •")
            return

        # Text area padding
        padding_x = 0.5 * inch
        padding_y = 0.3 * inch
        text_area_width = PAGE_WIDTH - (2 * padding_x)
        
        # Set up text styling
        c.setFillColor(Color(0.22, 0.25, 0.32))  # Dark gray (#374151)
        
        # Calculate font size based on text length (responsive sizing)
        text_length = len(story_text)
        if text_length > 250:
            font_size = 14
        elif text_length > 150:
            font_size = 16
        elif text_length > 80:
            font_size = 18
        else:
            font_size = 20

        c.setFont("Helvetica", font_size)
        
        # Simple text wrapping
        words = story_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if c.stringWidth(test_line, "Helvetica", font_size) <= text_area_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)

        # Calculate vertical centering
        line_height = font_size * 1.4
        total_text_height = len(lines) * line_height
        start_y = (TEXT_HEIGHT + total_text_height) / 2

        # Draw lines centered
        for i, line in enumerate(lines):
            y_pos = start_y - (i * line_height)
            if y_pos > padding_y:  # Don't draw below padding
                c.drawCentredString(PAGE_WIDTH/2, y_pos, line)

    # Legacy compatibility methods
    async def generate_storybook_pdf(
        self,
        pages: List[Dict],
        title: str,
        child_name: str,
        theme: str,
        story_template: Optional[object] = None
    ) -> bytes:
        """Legacy compatibility method for existing API."""
        logger.info("Legacy PDF generation called, using ReportLab approach")

        pdf_url = await self.generate_storygift_pdf(
            preview_id=f"legacy_{child_name}_{theme}",
            child_name=child_name,
            story_pages=pages,
            story_title=title
        )

        # Download PDF bytes for legacy return format
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(pdf_url)
            response.raise_for_status()
            return response.content


# Legacy class alias for backward compatibility
class PDFGeneratorService(StoryGiftPDFGeneratorService):
    """Backward compatibility alias."""
    pass