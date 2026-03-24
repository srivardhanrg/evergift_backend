"""
Book structure configuration for MagicTales 26-page storybook.

This module defines the complete book layout:
- 26 total pages (indices 0-25)
- Cover at index 0 (AI-generated)
- Dedication at index 1 (filler + text overlay)
- Intro pages at indices 2-3 (filler, no text)
- Alternating generated/text pages for the story
- End page and back cover at indices 24-25

Preview shows pages 0-13 (14 pages)
Locked pages are 14-25 (12 pages)
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class PageType(str, Enum):
    """Types of pages in the storybook."""
    COVER = "cover"
    DEDICATION = "dedication"
    INTRO = "intro"
    GENERATED = "generated"
    TEXT = "text"
    END_PAGE = "end_page"
    BACK_COVER = "back_cover"


class PageConfig(BaseModel):
    """Configuration for a single page in the book."""
    index: int
    page_type: PageType
    filler_filename: Optional[str] = None
    requires_text_overlay: bool = False
    text_page_number: Optional[int] = None  # For text1-text10 mapping (1-10)
    is_preview: bool = True  # False for locked pages (index >= 13)

    class Config:
        frozen = True  # Make immutable


# Complete 26-page book structure (UPDATED: Text on LEFT, AI on RIGHT)
# AI-generated pages: 0 (cover), 5, 7, 9, 11, 13, 15, 17, 19, 21, 23
# Filler pages: 1 (dedication), 2-3 (intros), 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 (text), 24 (end), 25 (back)
BOOK_STRUCTURE: List[PageConfig] = [
    # === PREVIEW PAGES (0-13) ===
    # Page 0: Cover - AI generated with child's face
    PageConfig(
        index=0,
        page_type=PageType.COVER,
        is_preview=True
    ),
    # Page 1: Dedication - filler with personalized text
    PageConfig(
        index=1,
        page_type=PageType.DEDICATION,
        filler_filename="dedication.png",
        requires_text_overlay=True,
        is_preview=True
    ),
    # Page 2: Intro 1 - filler, no text overlay
    PageConfig(
        index=2,
        page_type=PageType.INTRO,
        filler_filename="intro1.png",
        requires_text_overlay=False,
        is_preview=True
    ),
    # Page 3: Intro 2 - filler, no text overlay
    PageConfig(
        index=3,
        page_type=PageType.INTRO,
        filler_filename="intro2.png",
        requires_text_overlay=False,
        is_preview=True
    ),
    # Page 4: Text page 1 - filler with story text (LEFT page)
    PageConfig(
        index=4,
        page_type=PageType.TEXT,
        filler_filename="text1.png",
        requires_text_overlay=True,
        text_page_number=1,
        is_preview=True
    ),
    # Page 5: Generated story page 1 (RIGHT page)
    PageConfig(
        index=5,
        page_type=PageType.GENERATED,
        is_preview=True
    ),
    # Page 6: Text page 2 (LEFT page)
    PageConfig(
        index=6,
        page_type=PageType.TEXT,
        filler_filename="text2.png",
        requires_text_overlay=True,
        text_page_number=2,
        is_preview=True
    ),
    # Page 7: Generated story page 2 (RIGHT page)
    PageConfig(
        index=7,
        page_type=PageType.GENERATED,
        is_preview=True
    ),
    # Page 8: Text page 3 (LEFT page)
    PageConfig(
        index=8,
        page_type=PageType.TEXT,
        filler_filename="text3.png",
        requires_text_overlay=True,
        text_page_number=3,
        is_preview=True
    ),
    # Page 9: Generated story page 3 (RIGHT page)
    PageConfig(
        index=9,
        page_type=PageType.GENERATED,
        is_preview=True
    ),
    # Page 10: Text page 4 (LEFT page)
    PageConfig(
        index=10,
        page_type=PageType.TEXT,
        filler_filename="text4.png",
        requires_text_overlay=True,
        text_page_number=4,
        is_preview=True
    ),
    # Page 11: Generated story page 4 (RIGHT page)
    PageConfig(
        index=11,
        page_type=PageType.GENERATED,
        is_preview=True
    ),
    # Page 12: Text page 5 (LEFT page)
    PageConfig(
        index=12,
        page_type=PageType.TEXT,
        filler_filename="text5.png",
        requires_text_overlay=True,
        text_page_number=5,
        is_preview=True
    ),
    # Page 13: Generated story page 5 (RIGHT page - last preview page)
    PageConfig(
        index=13,
        page_type=PageType.GENERATED,
        is_preview=True
    ),

    # === LOCKED PAGES (14-25) ===
    # Page 14: Text page 6 (LEFT page)
    PageConfig(
        index=14,
        page_type=PageType.TEXT,
        filler_filename="text6.png",
        requires_text_overlay=True,
        text_page_number=6,
        is_preview=False
    ),
    # Page 15: Generated story page 6 (RIGHT page)
    PageConfig(
        index=15,
        page_type=PageType.GENERATED,
        is_preview=False
    ),
    # Page 16: Text page 7 (LEFT page)
    PageConfig(
        index=16,
        page_type=PageType.TEXT,
        filler_filename="text7.png",
        requires_text_overlay=True,
        text_page_number=7,
        is_preview=False
    ),
    # Page 17: Generated story page 7 (RIGHT page)
    PageConfig(
        index=17,
        page_type=PageType.GENERATED,
        is_preview=False
    ),
    # Page 18: Text page 8 (LEFT page)
    PageConfig(
        index=18,
        page_type=PageType.TEXT,
        filler_filename="text8.png",
        requires_text_overlay=True,
        text_page_number=8,
        is_preview=False
    ),
    # Page 19: Generated story page 8 (RIGHT page)
    PageConfig(
        index=19,
        page_type=PageType.GENERATED,
        is_preview=False
    ),
    # Page 20: Text page 9 (LEFT page)
    PageConfig(
        index=20,
        page_type=PageType.TEXT,
        filler_filename="text9.png",
        requires_text_overlay=True,
        text_page_number=9,
        is_preview=False
    ),
    # Page 21: Generated story page 9 (RIGHT page)
    PageConfig(
        index=21,
        page_type=PageType.GENERATED,
        is_preview=False
    ),
    # Page 22: Text page 10 (LEFT page - final story text)
    PageConfig(
        index=22,
        page_type=PageType.TEXT,
        filler_filename="text10.png",
        requires_text_overlay=True,
        text_page_number=10,
        is_preview=False
    ),
    # Page 23: Generated story page 10 (RIGHT page - last AI page)
    PageConfig(
        index=23,
        page_type=PageType.GENERATED,
        is_preview=False
    ),
    # Page 24: End page
    PageConfig(
        index=24,
        page_type=PageType.END_PAGE,
        filler_filename="endpage.png",
        requires_text_overlay=False,
        is_preview=False
    ),
    # Page 25: Back cover
    PageConfig(
        index=25,
        page_type=PageType.BACK_COVER,
        filler_filename="backcover.png",
        requires_text_overlay=False,
        is_preview=False
    ),
]

# Page count constants
PREVIEW_PAGE_COUNT = 14   # Pages 0-13
LOCKED_PAGE_COUNT = 12    # Pages 14-25
TOTAL_PAGE_COUNT = 26     # All pages

# AI-generated page indices (UPDATED: Text on LEFT, AI on RIGHT)
# Cover (0) + 10 story pages (5, 7, 9, 11, 13, 15, 17, 19, 21, 23) = 11 total
AI_GENERATED_INDICES = [0, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

# Preview phase generates: cover + 5 story pages
PREVIEW_AI_INDICES = [0, 5, 7, 9, 11, 13]  # 6 AI pages in preview

# Post-payment generates remaining 5 story pages
LOCKED_AI_INDICES = [15, 17, 19, 21, 23]   # 5 AI pages locked

# Theme folder mapping (strips 'storygift_' prefix for R2 paths)
THEME_FOLDER_MAP = {
    "storygift_enchanted_forest": "enchanted_forest",
    "storygift_magic_castle": "magic_castle",
    "storygift_cosmic_dreamer": "cosmic_dreamer",
    "storygift_mighty_guardian": "mighty_guardian",
    "storygift_ocean_explorer": "ocean_explorer",
    "storygift_birthday_magic": "birthday_magic",
    "storygift_safari_adventure": "safari_adventure",
    "storygift_secret_agent": "secret_agent",
    # Legacy themes
    "magic_castle": "magic_castle",
    "space_adventure": "space_adventure",
    "underwater": "underwater",
    "forest_friends": "forest_friends",
}


def get_filler_url(theme: str, style: str, filename: str) -> str:
    """
    Generate R2 public URL for filler image.

    Args:
        theme: Theme identifier (e.g., 'storygift_enchanted_forest')
        style: Book style ('photorealistic' or 'cartoon_3d')
        filename: Filler image filename (e.g., 'dedication.png')

    Returns:
        Full R2 public URL for the filler image
    """
    from app.config import get_settings
    settings = get_settings()

    # Get theme folder name
    theme_folder = THEME_FOLDER_MAP.get(theme, theme.replace("storygift_", ""))

    return f"{settings.r2_public_url}/filler_images/{theme_folder}/{style}/{filename}"


def get_page_config(index: int) -> Optional[PageConfig]:
    """
    Get page configuration by index.

    Args:
        index: Page index (0-25)

    Returns:
        PageConfig for the index, or None if invalid
    """
    if 0 <= index < len(BOOK_STRUCTURE):
        return BOOK_STRUCTURE[index]
    return None


def get_preview_pages() -> List[PageConfig]:
    """Get all pages visible in preview (indices 0-13)."""
    return [p for p in BOOK_STRUCTURE if p.is_preview]


def get_locked_pages() -> List[PageConfig]:
    """Get all locked pages (indices 14-25)."""
    return [p for p in BOOK_STRUCTURE if not p.is_preview]


def get_filler_pages(preview_only: bool = False) -> List[PageConfig]:
    """
    Get all filler pages (pages with filler_filename set).

    Args:
        preview_only: If True, only return preview filler pages

    Returns:
        List of PageConfig for filler pages
    """
    pages = [p for p in BOOK_STRUCTURE if p.filler_filename is not None]
    if preview_only:
        pages = [p for p in pages if p.is_preview]
    return pages


def get_text_pages(preview_only: bool = False) -> List[PageConfig]:
    """
    Get all text pages (pages that require text overlay).

    Args:
        preview_only: If True, only return preview text pages

    Returns:
        List of PageConfig for text pages
    """
    pages = [p for p in BOOK_STRUCTURE if p.requires_text_overlay]
    if preview_only:
        pages = [p for p in pages if p.is_preview]
    return pages


def get_ai_pages(preview_only: bool = False) -> List[PageConfig]:
    """
    Get all AI-generated pages.

    Args:
        preview_only: If True, only return preview AI pages

    Returns:
        List of PageConfig for AI-generated pages
    """
    indices = PREVIEW_AI_INDICES if preview_only else AI_GENERATED_INDICES
    return [BOOK_STRUCTURE[i] for i in indices]
