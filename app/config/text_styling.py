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

THEME_TEXT_CONFIGS: Dict[str, Dict[str, TextConfig]] = {
    # ========================================================================
    # ENCHANTED FOREST THEME
    # ========================================================================
    # Color palette inspired by magical forest imagery:
    # - Forest greens (#2D5016, #1B4D3E)
    # - Earth browns (#5D4037)
    # - Waterfall blues (#1565C0)
    # - Mystical purples (#4A148C)
    # - Golden endings (#FFB300)
    "storygift_enchanted_forest": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#2D5016",  # Deep forest green
            "shadow": {
                "color": "#000000",
                "opacity": 0.12,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#2D5016",  # Default forest green
            "shadow": {
                "color": "#1A3009",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#1B4D3E",  # Darker forest accent
                "lines_to_span": 3
            },
            # Page-specific colors based on filler image aesthetics
            "page_colors": {
                # Text page 1 - Opening forest scene (green tones)
                "text1": {"color": "#2D5016", "shadow_color": "#1A3009"},
                # Text page 2 - Earth/woodland scene (warm brown)
                "text2": {"color": "#5D4037", "shadow_color": "#3E2723"},
                # Text page 3 - Waterfall/stream scene (water blue)
                "text3": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                # Text page 4 - Deep forest (forest green)
                "text4": {"color": "#2D5016", "shadow_color": "#1A3009"},
                # Text page 5 - Mystical encounter (mystical purple)
                "text5": {"color": "#4A148C", "shadow_color": "#311B92"},
                # Text page 6 - Tree/bark scene (earth brown)
                "text6": {"color": "#5D4037", "shadow_color": "#3E2723"},
                # Text page 7 - Meadow scene (fresh green)
                "text7": {"color": "#388E3C", "shadow_color": "#1B5E20"},
                # Text page 8 - Twilight scene (soft blue)
                "text8": {"color": "#1976D2", "shadow_color": "#0D47A1"},
                # Text page 9 - Dawn scene (warm brown)
                "text9": {"color": "#6D4C41", "shadow_color": "#4E342E"},
                # Text page 10 - Triumphant ending (golden)
                "text10": {"color": "#F57F17", "shadow_color": "#E65100"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # MAGIC CASTLE THEME
    # ========================================================================
    # Color palette inspired by magical academy:
    # - Royal purples (#6A1B9A, #4A148C)
    # - Midnight blues (#1A237E)
    # - Gold accents (#FFD600)
    "storygift_magic_castle": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#4A148C",
            "shadow": {
                "color": "#000000",
                "opacity": 0.12,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#4A148C",
            "shadow": {
                "color": "#311B92",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#6A1B9A",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#4A148C", "shadow_color": "#311B92"},
                "text2": {"color": "#1A237E", "shadow_color": "#0D1642"},
                "text3": {"color": "#6A1B9A", "shadow_color": "#4A148C"},
                "text4": {"color": "#4527A0", "shadow_color": "#311B92"},
                "text5": {"color": "#283593", "shadow_color": "#1A237E"},
                "text6": {"color": "#6A1B9A", "shadow_color": "#4A148C"},
                "text7": {"color": "#4A148C", "shadow_color": "#311B92"},
                "text8": {"color": "#1A237E", "shadow_color": "#0D1642"},
                "text9": {"color": "#4527A0", "shadow_color": "#311B92"},
                "text10": {"color": "#F57F17", "shadow_color": "#E65100"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # COSMIC ADVENTURE THEME
    # ========================================================================
    # Color palette inspired by space exploration:
    # - Deep space blues (#1A237E, #0D47A1)
    # - Nebula purples (#4A148C)
    # - Starlight silver (#546E7A)
    "storygift_cosmic_dreamer": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#1A237E",
            "shadow": {
                "color": "#000000",
                "opacity": 0.15,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 5
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#1A237E",
            "shadow": {
                "color": "#0D1642",
                "opacity": 0.18,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#283593",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#1A237E", "shadow_color": "#0D1642"},
                "text2": {"color": "#4A148C", "shadow_color": "#311B92"},
                "text3": {"color": "#0D47A1", "shadow_color": "#01579B"},
                "text4": {"color": "#283593", "shadow_color": "#1A237E"},
                "text5": {"color": "#4A148C", "shadow_color": "#311B92"},
                "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                "text7": {"color": "#1A237E", "shadow_color": "#0D1642"},
                "text8": {"color": "#4527A0", "shadow_color": "#311B92"},
                "text9": {"color": "#0D47A1", "shadow_color": "#01579B"},
                "text10": {"color": "#FFD600", "shadow_color": "#F57F17"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # OCEAN EXPLORER THEME
    # ========================================================================
    # Color palette inspired by underwater world:
    # - Ocean blues (#0277BD, #01579B)
    # - Coral (#E65100)
    # - Sea green (#00695C)
    "storygift_ocean_explorer": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#01579B",
            "shadow": {
                "color": "#000000",
                "opacity": 0.12,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#01579B",
            "shadow": {
                "color": "#002F6C",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#0277BD",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#01579B", "shadow_color": "#002F6C"},
                "text2": {"color": "#00695C", "shadow_color": "#004D40"},
                "text3": {"color": "#0277BD", "shadow_color": "#01579B"},
                "text4": {"color": "#00838F", "shadow_color": "#006064"},
                "text5": {"color": "#01579B", "shadow_color": "#002F6C"},
                "text6": {"color": "#00695C", "shadow_color": "#004D40"},
                "text7": {"color": "#0277BD", "shadow_color": "#01579B"},
                "text8": {"color": "#00838F", "shadow_color": "#006064"},
                "text9": {"color": "#01579B", "shadow_color": "#002F6C"},
                "text10": {"color": "#FFB300", "shadow_color": "#FF8F00"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # SAFARI ADVENTURE THEME
    # ========================================================================
    # Color palette inspired by African savanna:
    # - Savanna gold (#F57F17, #E65100)
    # - Earth brown (#5D4037)
    # - Sunset orange (#EF6C00)
    "storygift_safari_adventure": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#5D4037",
            "shadow": {
                "color": "#000000",
                "opacity": 0.12,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#5D4037",
            "shadow": {
                "color": "#3E2723",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#6D4C41",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#5D4037", "shadow_color": "#3E2723"},
                "text2": {"color": "#EF6C00", "shadow_color": "#E65100"},
                "text3": {"color": "#6D4C41", "shadow_color": "#4E342E"},
                "text4": {"color": "#F57F17", "shadow_color": "#E65100"},
                "text5": {"color": "#5D4037", "shadow_color": "#3E2723"},
                "text6": {"color": "#EF6C00", "shadow_color": "#E65100"},
                "text7": {"color": "#6D4C41", "shadow_color": "#4E342E"},
                "text8": {"color": "#F57F17", "shadow_color": "#E65100"},
                "text9": {"color": "#5D4037", "shadow_color": "#3E2723"},
                "text10": {"color": "#FFB300", "shadow_color": "#FF8F00"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # MIGHTY GUARDIAN (SUPERHERO) THEME
    # ========================================================================
    "storygift_mighty_guardian": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#B71C1C",
            "shadow": {
                "color": "#000000",
                "opacity": 0.15,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#B71C1C",
            "shadow": {
                "color": "#7F0000",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#C62828",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#B71C1C", "shadow_color": "#7F0000"},
                "text2": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                "text3": {"color": "#C62828", "shadow_color": "#B71C1C"},
                "text4": {"color": "#1976D2", "shadow_color": "#1565C0"},
                "text5": {"color": "#B71C1C", "shadow_color": "#7F0000"},
                "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                "text7": {"color": "#C62828", "shadow_color": "#B71C1C"},
                "text8": {"color": "#1976D2", "shadow_color": "#1565C0"},
                "text9": {"color": "#B71C1C", "shadow_color": "#7F0000"},
                "text10": {"color": "#FFD600", "shadow_color": "#F57F17"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # BIRTHDAY MAGIC THEME
    # ========================================================================
    "storygift_birthday_magic": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#AD1457",
            "shadow": {
                "color": "#000000",
                "opacity": 0.12,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#AD1457",
            "shadow": {
                "color": "#880E4F",
                "opacity": 0.15,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#C2185B",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#AD1457", "shadow_color": "#880E4F"},
                "text2": {"color": "#7B1FA2", "shadow_color": "#6A1B9A"},
                "text3": {"color": "#C2185B", "shadow_color": "#AD1457"},
                "text4": {"color": "#8E24AA", "shadow_color": "#7B1FA2"},
                "text5": {"color": "#AD1457", "shadow_color": "#880E4F"},
                "text6": {"color": "#7B1FA2", "shadow_color": "#6A1B9A"},
                "text7": {"color": "#C2185B", "shadow_color": "#AD1457"},
                "text8": {"color": "#8E24AA", "shadow_color": "#7B1FA2"},
                "text9": {"color": "#AD1457", "shadow_color": "#880E4F"},
                "text10": {"color": "#FFD600", "shadow_color": "#F57F17"}
            },
            "letter_spacing": 0.3
        }
    },

    # ========================================================================
    # SECRET AGENT THEME
    # ========================================================================
    "storygift_secret_agent": {
        "dedication": {
            "font_family": "Dancing Script",
            "font_size": 48,
            "line_height": 1.7,
            "color": "#37474F",
            "shadow": {
                "color": "#000000",
                "opacity": 0.15,
                "offset_x": 2,
                "offset_y": 2,
                "blur": 4
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 70,
            "vertical_position": "center",
            "drop_cap": None,
            "page_colors": None,
            "letter_spacing": 0.5
        },
        "story": {
            "font_family": "Playfair Display",
            "font_size": 32,
            "line_height": 1.9,
            "color": "#37474F",
            "shadow": {
                "color": "#263238",
                "opacity": 0.18,
                "offset_x": 1,
                "offset_y": 2,
                "blur": 3
            },
            "alignment": TextAlignment.CENTER,
            "max_width_percent": 75,
            "vertical_position": "center",
            "drop_cap": {
                "enabled": True,
                "font_size": 72,
                "font_family": "Cormorant Garamond Bold",
                "color": "#455A64",
                "lines_to_span": 3
            },
            "page_colors": {
                "text1": {"color": "#37474F", "shadow_color": "#263238"},
                "text2": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                "text3": {"color": "#455A64", "shadow_color": "#37474F"},
                "text4": {"color": "#1976D2", "shadow_color": "#1565C0"},
                "text5": {"color": "#37474F", "shadow_color": "#263238"},
                "text6": {"color": "#1565C0", "shadow_color": "#0D47A1"},
                "text7": {"color": "#455A64", "shadow_color": "#37474F"},
                "text8": {"color": "#1976D2", "shadow_color": "#1565C0"},
                "text9": {"color": "#37474F", "shadow_color": "#263238"},
                "text10": {"color": "#FFD600", "shadow_color": "#F57F17"}
            },
            "letter_spacing": 0.3
        }
    },
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
