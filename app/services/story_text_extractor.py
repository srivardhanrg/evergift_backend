"""
Story Text Extractor - Extracts story text from theme templates for V2 26-page structure.

Maps theme pages (1-10) to book structure text page indices (5,7,9,11,13,15,17,19,21,23).
Handles child name substitution and returns formatted text ready for overlay rendering.
"""

import structlog
from typing import Dict, Optional
from app.stories.themes import get_theme
from app.core.sanitization import sanitize_for_prompt

logger = structlog.get_logger()

# Mapping: theme page number → book structure text page index
# Theme has 10 pages with story_text, which map to 10 text pages in the book
THEME_PAGE_TO_TEXT_INDEX = {
    1: 5,   # Theme page 1 → Book index 5 (first text page after AI page 4)
    2: 7,   # Theme page 2 → Book index 7 (text page after AI page 6)
    3: 9,   # Theme page 3 → Book index 9 (text page after AI page 8)
    4: 11,  # Theme page 4 → Book index 11 (text page after AI page 10)
    5: 13,  # Theme page 5 → Book index 13 (first locked text page after AI page 12)
    6: 15,  # Theme page 6 → Book index 15 (text page after AI page 14)
    7: 17,  # Theme page 7 → Book index 17 (text page after AI page 16)
    8: 19,  # Theme page 8 → Book index 19 (text page after AI page 18)
    9: 21,  # Theme page 9 → Book index 21 (text page after AI page 20)
    10: 23, # Theme page 10 → Book index 23 (last text page after AI page 22)
}


def extract_story_texts(theme: str, child_name: str) -> Dict[int, str]:
    """
    Extract story texts from theme template and map to book structure indices.

    This function:
    1. Loads the theme template
    2. Extracts story_text from each page
    3. Substitutes {name} placeholder with actual child name
    4. Maps theme page numbers to book structure indices
    5. Returns dict ready for filler page text overlay processing

    Args:
        theme: Theme identifier (e.g., 'storygift_enchanted_forest')
        child_name: Child's name to substitute in story text

    Returns:
        Dict mapping book index (5,7,9,11,13,15,17,19,21,23) to story text string

    Example:
        >>> extract_story_texts('storygift_enchanted_forest', 'Alice')
        {
            5: "The morning sunshine danced through the bedroom window as Alice discovered...",
            7: "The map was unlike anything Alice had ever seen before...",
            ...
            23: "As the golden sun painted the sky in magical colors, Alice knew..."
        }
    """
    try:
        template = get_theme(theme)
        story_texts = {}

        # Extract story_text from each page in template
        for page in template.pages:
            page_num = page.page_number  # 1-10

            if page_num not in THEME_PAGE_TO_TEXT_INDEX:
                logger.warning(
                    "Theme page not in mapping",
                    page_num=page_num,
                    theme=theme
                )
                continue

            # Get story text from page template
            story_text = page.story_text

            if not story_text:
                logger.warning(
                    "No story_text found for page",
                    page_num=page_num,
                    theme=theme
                )
                continue

            # Substitute {name} with actual child name
            # Use sanitize_for_prompt to prevent any potential issues
            safe_name = sanitize_for_prompt(child_name)
            story_text = story_text.replace("{name}", safe_name)

            # Map to book structure index
            book_index = THEME_PAGE_TO_TEXT_INDEX[page_num]
            story_texts[book_index] = story_text

            logger.debug(
                "Extracted story text",
                theme_page=page_num,
                book_index=book_index,
                text_length=len(story_text),
                text_preview=story_text[:50] + "..."
            )

        if len(story_texts) != 10:
            logger.warning(
                "Expected 10 story texts, got different count",
                theme=theme,
                expected=10,
                actual=len(story_texts)
            )

        logger.info(
            "Story texts extracted successfully",
            theme=theme,
            count=len(story_texts),
            indices=sorted(story_texts.keys())
        )

        return story_texts

    except Exception as e:
        logger.error(
            "Failed to extract story texts",
            theme=theme,
            child_name=child_name,
            error=str(e),
            error_type=type(e).__name__
        )
        # Return empty dict - generation will fail with clear error
        # This is safer than returning partial data
        return {}


def get_story_text_for_index(
    story_texts: Dict[int, str],
    index: int
) -> Optional[str]:
    """
    Get story text for a specific book structure index.

    Args:
        story_texts: Dict from extract_story_texts()
        index: Book structure index (5,7,9,11,13,15,17,19,21,23)

    Returns:
        Story text string or None if not found

    Example:
        >>> texts = extract_story_texts('storygift_enchanted_forest', 'Bob')
        >>> get_story_text_for_index(texts, 5)
        "The morning sunshine danced through the bedroom window as Bob discovered..."
    """
    text = story_texts.get(index)

    if text is None:
        logger.warning(
            "No story text found for index",
            index=index,
            available_indices=sorted(story_texts.keys())
        )

    return text


def get_text_page_number_from_index(index: int) -> Optional[int]:
    """
    Convert book structure index to text page number (1-10).

    Reverse mapping from THEME_PAGE_TO_TEXT_INDEX.

    Args:
        index: Book structure index (5,7,9,11,13,15,17,19,21,23)

    Returns:
        Text page number (1-10) or None if invalid

    Example:
        >>> get_text_page_number_from_index(5)
        1
        >>> get_text_page_number_from_index(23)
        10
    """
    # Reverse lookup
    for page_num, book_index in THEME_PAGE_TO_TEXT_INDEX.items():
        if book_index == index:
            return page_num

    logger.warning("Invalid text page index", index=index)
    return None
