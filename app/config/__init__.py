"""
Book configuration package for MagicTales 26-page structure.

This package contains:
- book_structure: Page layout configuration (26 pages, filler mappings)
- text_styling: Premium text overlay styling per theme
"""

from app.config.book_structure import (
    PageType,
    PageConfig,
    BOOK_STRUCTURE,
    PREVIEW_PAGE_COUNT,
    LOCKED_PAGE_COUNT,
    TOTAL_PAGE_COUNT,
    AI_GENERATED_INDICES,
    PREVIEW_AI_INDICES,
    LOCKED_AI_INDICES,
    get_filler_url,
    get_page_config,
    get_preview_pages,
    get_locked_pages,
)

from app.config.text_styling import (
    TextAlignment,
    DEDICATION_TEXT_TEMPLATE,
    THEME_TEXT_CONFIGS,
    get_text_config,
    get_dedication_text,
    get_page_specific_colors,
)

__all__ = [
    # Book structure
    "PageType",
    "PageConfig",
    "BOOK_STRUCTURE",
    "PREVIEW_PAGE_COUNT",
    "LOCKED_PAGE_COUNT",
    "TOTAL_PAGE_COUNT",
    "AI_GENERATED_INDICES",
    "PREVIEW_AI_INDICES",
    "LOCKED_AI_INDICES",
    "get_filler_url",
    "get_page_config",
    "get_preview_pages",
    "get_locked_pages",
    # Text styling
    "TextAlignment",
    "DEDICATION_TEXT_TEMPLATE",
    "THEME_TEXT_CONFIGS",
    "get_text_config",
    "get_dedication_text",
    "get_page_specific_colors",
]
