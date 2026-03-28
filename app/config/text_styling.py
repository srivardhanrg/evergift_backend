"""
Premium text styling configuration for MagicTales storybook text overlays.

This module defines:
- Font choices for premium $40 book quality
- Theme-specific color palettes
- Page-specific color adaptations
- Text layout and effects (shadows, drop caps)

Fonts used (Google Fonts - commercial safe):
- Dancing Script: Warm, personal handwritten feel for dedication
- Playfair Display: Elegant serif with literary feel for story text
- Cormorant Garamond: Classic book typography for drop caps
"""

from enum import Enum
from typing import TypedDict, Optional, Dict


class TextAlignment(str, Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class ShadowConfig(TypedDict):
    """Text shadow configuration."""
    color: str          # Hex color for shadow
    opacity: float      # 0.0 - 1.0
    offset_x: int       # Horizontal offset in pixels
    offset_y: int       # Vertical offset in pixels
    blur: int           # Blur radius in pixels


class DropCapConfig(TypedDict):
    """Drop cap (large first letter) configuration."""
    enabled: bool
    font_size: int      # Size of drop cap in pixels
    font_family: str
    color: str          # Hex color
    lines_to_span: int  # How many lines the drop cap spans


class PageTextStyle(TypedDict):
    """Page-specific text color overrides."""
    color: str          # Primary text color (hex)
    shadow_color: str   # Shadow color (hex)


class BubbleConfig(TypedDict):
    """Fun semi-transparent bubble behind text for kid-friendly readability."""
    enabled: bool
    color: str              # Hex color (theme-specific)
    opacity: float          # 0.0 - 1.0 (recommend 0.55-0.70)
    corner_radius: int      # Pixels — large values = pillow/cloud feel (80-120 at 300 DPI)
    padding_x: int          # Horizontal padding beyond text bounds
    padding_y: int          # Vertical padding beyond text bounds
    blur_edge: int          # Gaussian blur on bubble edge (0=sharp, 8-15=soft pillow feel)


class TextConfig(TypedDict):
    """Complete text styling configuration."""
    font_family: str
    font_size: int
    line_height: float
    color: str
    shadow: Optional[ShadowConfig]
    alignment: TextAlignment
    max_width_percent: int
    vertical_position: str  # 'center', 'top', 'bottom'
    drop_cap: Optional[DropCapConfig]
    page_colors: Optional[Dict[str, PageTextStyle]]
    letter_spacing: Optional[float]  # Extra letter spacing
    bubble: Optional[BubbleConfig]   # Semi-transparent fun bubble behind text


# ============================================================================
# DEDICATION PAGE TEXT TEMPLATE
# ============================================================================
# This template creates an emotional, personalized dedication page.
# The {child_name} placeholder is replaced with the actual child's name.

DEDICATION_TEXT_TEMPLATE = """Dear {child_name},

This magical story was made just for you. May it fill your heart with wonder and joy."""


# ============================================================================
# FONT PATHS (relative to /app/fonts/ in Docker)
# ============================================================================
# These fonts are downloaded during Docker build from Google Fonts

FONT_PATHS = {
    # Primary fonts (playful + kid-friendly)
    "Bubblegum Sans": "/app/fonts/BubblegumSans-Regular.ttf",
    "Caveat": "/app/fonts/Caveat-Regular.ttf",
    "Pacifico": "/app/fonts/Pacifico-Regular.ttf",
    # Cover fonts
    "Magical Neverland": "/app/fonts/MagicalNeverland-Regular.ttf",
    "Luckiest Guy": "/app/fonts/LuckiestGuy-Regular.ttf",
    # Legacy fonts (kept for backward compatibility)
    "Dancing Script": "/app/fonts/DancingScript-Regular.ttf",
    "Playfair Display": "/app/fonts/PlayfairDisplay-Regular.ttf",
    "Cormorant Garamond": "/app/fonts/CormorantGaramond-Regular.ttf",
    "Cormorant Garamond Bold": "/app/fonts/CormorantGaramond-Bold.ttf",
    # Fallback fonts (system fonts)
    "Georgia": None,  # System font
    "Times New Roman": None,  # System font
}


# ============================================================================
# THEME-SPECIFIC TEXT CONFIGURATIONS
# ============================================================================
# Fonts: Bubblegum Sans (story) + Caveat (dedication) — playful & kid-friendly
# Text fills ~75% of page width for maximum impact
# Cloud bubble behind text for readability against any background

# Shared bubble defaults (theme color overrides below)
_STORY_BUBBLE_DEFAULTS = {
    "enabled": True,
    "opacity": 0.72,
    "corner_radius": 120,
    "padding_x": 100,
    "padding_y": 70,
    "blur_edge": 12,
    "shape": "cloud",       # "cloud" = bumpy edges, "rounded" = plain rounded rect
    "cloud_bump_size": 60,  # radius of each bump circle (at 2550px)
}

_DEDICATION_BUBBLE_DEFAULTS = {
    "enabled": True,
    "opacity": 0.75,
    "corner_radius": 120,
    "padding_x": 130,
    "padding_y": 90,
    "blur_edge": 14,
    "shape": "cloud",
    "cloud_bump_size": 60,
}

# Shared story text config (overridden per-theme for colors only)
_STORY_BASE = {
    "font_family": "Bubblegum Sans",
    "font_size": 100,
    "line_height": 1.8,
    "shadow": {
        "color": "#000000",
        "opacity": 0.12,
        "offset_x": 3,
        "offset_y": 4,
        "blur": 5
    },
    "alignment": TextAlignment.CENTER,
    "max_width_percent": 75,
    "vertical_position": "center",
    "drop_cap": {
        "enabled": True,
        "font_size": 260,
        "font_family": "Bubblegum Sans",
        "color": None,  # overridden per theme
        "lines_to_span": 3
    },
    "letter_spacing": 0.5,
}

_DEDICATION_BASE = {
    "font_family": "Caveat",
    "font_size": 130,
    "line_height": 1.6,
    "shadow": {
        "color": "#000000",
        "opacity": 0.10,
        "offset_x": 3,
        "offset_y": 4,
        "blur": 6
    },
    "alignment": TextAlignment.CENTER,
    "max_width_percent": 75,
    "vertical_position": "center",
    "drop_cap": None,
    "page_colors": None,
    "letter_spacing": 0.8,
}


def _make_theme(
    dedication_color: str,
    story_color: str,
    drop_cap_color: str,
    bubble_color: str,
    page_colors: dict,
    shadow_color: str = "#000000",
) -> Dict[str, TextConfig]:
    """Build a complete theme config from just the colors."""
    return {
        "dedication": {
            **_DEDICATION_BASE,
            "color": dedication_color,
            "bubble": {**_DEDICATION_BUBBLE_DEFAULTS, "color": bubble_color},
        },
        "story": {
            **_STORY_BASE,
            "color": story_color,
            "shadow": {**_STORY_BASE["shadow"], "color": shadow_color},
            "drop_cap": {**_STORY_BASE["drop_cap"], "color": drop_cap_color},
            "page_colors": page_colors,
            "bubble": {**_STORY_BUBBLE_DEFAULTS, "color": bubble_color},
        },
    }


THEME_TEXT_CONFIGS: Dict[str, Dict[str, TextConfig]] = {
    # ========================================================================
    # ENCHANTED FOREST — warm parchment bubble, forest greens
    # ========================================================================
    "storygift_enchanted_forest": _make_theme(
        dedication_color="#2D5016",
        story_color="#2D5016",
        drop_cap_color="#1B4D3E",
        bubble_color="#F5F0E1",
        shadow_color="#1A3009",
        page_colors={
            "text1": {"color": "#2D5016", "shadow_color": "#1A3009"},
            "text2": {"color": "#5D4037", "shadow_color": "#3E2723"},
            "text3": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text4": {"color": "#2D5016", "shadow_color": "#1A3009"},
            "text5": {"color": "#4A148C", "shadow_color": "#311B92"},
            "text6": {"color": "#5D4037", "shadow_color": "#3E2723"},
            "text7": {"color": "#388E3C", "shadow_color": "#1B5E20"},
            "text8": {"color": "#1976D2", "shadow_color": "#0D47A1"},
            "text9": {"color": "#6D4C41", "shadow_color": "#4E342E"},
            "text10": {"color": "#F57F17", "shadow_color": "#E65100"},
        },
    ),

    # ========================================================================
    # MAGIC CASTLE — soft lavender bubble, royal purples
    # ========================================================================
    "storygift_magic_castle": _make_theme(
        dedication_color="#4A148C",
        story_color="#4A148C",
        drop_cap_color="#6A1B9A",
        bubble_color="#EDE7F6",
        shadow_color="#311B92",
        page_colors={
            "text1": {"color": "#4A148C", "shadow_color": "#311B92"},
            "text2": {"color": "#1A237E", "shadow_color": "#0D1642"},
            "text3": {"color": "#6A1B9A", "shadow_color": "#4A148C"},
            "text4": {"color": "#4527A0", "shadow_color": "#311B92"},
            "text5": {"color": "#283593", "shadow_color": "#1A237E"},
            "text6": {"color": "#6A1B9A", "shadow_color": "#4A148C"},
            "text7": {"color": "#4A148C", "shadow_color": "#311B92"},
            "text8": {"color": "#1A237E", "shadow_color": "#0D1642"},
            "text9": {"color": "#4527A0", "shadow_color": "#311B92"},
            "text10": {"color": "#F57F17", "shadow_color": "#E65100"},
        },
    ),

    # ========================================================================
    # COSMIC DREAMER — pale indigo bubble, space blues
    # ========================================================================
    "storygift_cosmic_dreamer": _make_theme(
        dedication_color="#1A237E",
        story_color="#1A237E",
        drop_cap_color="#283593",
        bubble_color="#E8EAF6",
        shadow_color="#0D1642",
        page_colors={
            "text1": {"color": "#1A237E", "shadow_color": "#0D1642"},
            "text2": {"color": "#4A148C", "shadow_color": "#311B92"},
            "text3": {"color": "#0D47A1", "shadow_color": "#01579B"},
            "text4": {"color": "#283593", "shadow_color": "#1A237E"},
            "text5": {"color": "#4A148C", "shadow_color": "#311B92"},
            "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text7": {"color": "#1A237E", "shadow_color": "#0D1642"},
            "text8": {"color": "#4527A0", "shadow_color": "#311B92"},
            "text9": {"color": "#0D47A1", "shadow_color": "#01579B"},
            "text10": {"color": "#1A237E", "shadow_color": "#0D1642"},
        },
    ),

    # ========================================================================
    # OCEAN EXPLORER — light cyan bubble, ocean blues
    # ========================================================================
    "storygift_ocean_explorer": _make_theme(
        dedication_color="#01579B",
        story_color="#01579B",
        drop_cap_color="#0277BD",
        bubble_color="#E0F7FA",
        shadow_color="#002F6C",
        page_colors={
            "text1": {"color": "#01579B", "shadow_color": "#002F6C"},
            "text2": {"color": "#00695C", "shadow_color": "#004D40"},
            "text3": {"color": "#0277BD", "shadow_color": "#01579B"},
            "text4": {"color": "#00838F", "shadow_color": "#006064"},
            "text5": {"color": "#01579B", "shadow_color": "#002F6C"},
            "text6": {"color": "#00695C", "shadow_color": "#004D40"},
            "text7": {"color": "#0277BD", "shadow_color": "#01579B"},
            "text8": {"color": "#00838F", "shadow_color": "#006064"},
            "text9": {"color": "#01579B", "shadow_color": "#002F6C"},
            "text10": {"color": "#00695C", "shadow_color": "#004D40"},
        },
    ),

    # ========================================================================
    # SAFARI ADVENTURE — warm cream bubble, earth browns
    # ========================================================================
    "storygift_safari_adventure": _make_theme(
        dedication_color="#5D4037",
        story_color="#5D4037",
        drop_cap_color="#6D4C41",
        bubble_color="#FFF8E1",
        shadow_color="#3E2723",
        page_colors={
            "text1": {"color": "#5D4037", "shadow_color": "#3E2723"},
            "text2": {"color": "#EF6C00", "shadow_color": "#E65100"},
            "text3": {"color": "#6D4C41", "shadow_color": "#4E342E"},
            "text4": {"color": "#F57F17", "shadow_color": "#E65100"},
            "text5": {"color": "#5D4037", "shadow_color": "#3E2723"},
            "text6": {"color": "#EF6C00", "shadow_color": "#E65100"},
            "text7": {"color": "#6D4C41", "shadow_color": "#4E342E"},
            "text8": {"color": "#F57F17", "shadow_color": "#E65100"},
            "text9": {"color": "#5D4037", "shadow_color": "#3E2723"},
            "text10": {"color": "#5D4037", "shadow_color": "#3E2723"},
        },
    ),

    # ========================================================================
    # MIGHTY GUARDIAN — soft red bubble, hero reds & blues
    # ========================================================================
    "storygift_mighty_guardian": _make_theme(
        dedication_color="#B71C1C",
        story_color="#B71C1C",
        drop_cap_color="#C62828",
        bubble_color="#FFEBEE",
        shadow_color="#7F0000",
        page_colors={
            "text1": {"color": "#B71C1C", "shadow_color": "#7F0000"},
            "text2": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text3": {"color": "#C62828", "shadow_color": "#B71C1C"},
            "text4": {"color": "#1976D2", "shadow_color": "#1565C0"},
            "text5": {"color": "#B71C1C", "shadow_color": "#7F0000"},
            "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text7": {"color": "#C62828", "shadow_color": "#B71C1C"},
            "text8": {"color": "#1976D2", "shadow_color": "#1565C0"},
            "text9": {"color": "#B71C1C", "shadow_color": "#7F0000"},
            "text10": {"color": "#1A237E", "shadow_color": "#0D47A1"},
        },
    ),

    # ========================================================================
    # BIRTHDAY MAGIC — pink bubble, party pinks & purples
    # ========================================================================
    "storygift_birthday_magic": _make_theme(
        dedication_color="#AD1457",
        story_color="#AD1457",
        drop_cap_color="#C2185B",
        bubble_color="#FCE4EC",
        shadow_color="#880E4F",
        page_colors={
            "text1": {"color": "#AD1457", "shadow_color": "#880E4F"},
            "text2": {"color": "#7B1FA2", "shadow_color": "#6A1B9A"},
            "text3": {"color": "#C2185B", "shadow_color": "#AD1457"},
            "text4": {"color": "#8E24AA", "shadow_color": "#7B1FA2"},
            "text5": {"color": "#AD1457", "shadow_color": "#880E4F"},
            "text6": {"color": "#7B1FA2", "shadow_color": "#6A1B9A"},
            "text7": {"color": "#C2185B", "shadow_color": "#AD1457"},
            "text8": {"color": "#8E24AA", "shadow_color": "#7B1FA2"},
            "text9": {"color": "#AD1457", "shadow_color": "#880E4F"},
            "text10": {"color": "#7B1FA2", "shadow_color": "#6A1B9A"},
        },
    ),

    # ========================================================================
    # SECRET AGENT — cool gray bubble, sleek grays & blues
    # ========================================================================
    "storygift_secret_agent": _make_theme(
        dedication_color="#37474F",
        story_color="#37474F",
        drop_cap_color="#455A64",
        bubble_color="#ECEFF1",
        shadow_color="#263238",
        page_colors={
            "text1": {"color": "#37474F", "shadow_color": "#263238"},
            "text2": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text3": {"color": "#455A64", "shadow_color": "#37474F"},
            "text4": {"color": "#1976D2", "shadow_color": "#1565C0"},
            "text5": {"color": "#37474F", "shadow_color": "#263238"},
            "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
            "text7": {"color": "#455A64", "shadow_color": "#37474F"},
            "text8": {"color": "#1976D2", "shadow_color": "#1565C0"},
            "text9": {"color": "#37474F", "shadow_color": "#263238"},
            "text10": {"color": "#37474F", "shadow_color": "#263238"},
        },
    ),
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_text_config(theme: str, page_type: str) -> TextConfig:
    """
    Get text styling configuration for a theme and page type.

    Args:
        theme: Theme identifier (e.g., 'storygift_enchanted_forest')
        page_type: 'dedication' or 'story'

    Returns:
        TextConfig for the specified theme and page type
    """
    # Get theme config, fall back to enchanted_forest as default
    theme_config = THEME_TEXT_CONFIGS.get(
        theme,
        THEME_TEXT_CONFIGS.get("storygift_enchanted_forest")
    )

    if theme_config is None:
        # Ultimate fallback
        theme_config = THEME_TEXT_CONFIGS["storygift_enchanted_forest"]

    return theme_config.get(page_type, theme_config["story"])


def get_dedication_text(child_name: str) -> str:
    """
    Generate dedication page text with child's name.

    Args:
        child_name: The child's name to personalize the dedication

    Returns:
        Formatted dedication text with the child's name
    """
    return DEDICATION_TEXT_TEMPLATE.format(child_name=child_name)


def get_page_specific_colors(
    theme: str,
    text_page_number: int
) -> Optional[PageTextStyle]:
    """
    Get page-specific colors for a text page.

    Args:
        theme: Theme identifier
        text_page_number: Text page number (1-10)

    Returns:
        PageTextStyle with color and shadow_color, or None if not defined
    """
    story_config = get_text_config(theme, "story")
    page_colors = story_config.get("page_colors")

    if page_colors is None:
        return None

    page_key = f"text{text_page_number}"
    return page_colors.get(page_key)


def get_font_path(font_family: str) -> Optional[str]:
    """
    Get the file path for a font family.

    Args:
        font_family: Font family name

    Returns:
        Path to font file, or None for system fonts
    """
    return FONT_PATHS.get(font_family)
