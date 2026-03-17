"""
Filler Pages Service for MagicTales 26-page storybook.

This service orchestrates the processing of filler pages:
- Fetches base filler images from R2
- Applies text overlays for dedication and story text pages
- Uploads processed images back to R2
- Tracks which pages have been processed

Filler Page Types:
- Dedication (index 1): Personalized with child's name
- Intro pages (indices 2-3): No text overlay
- Text pages (indices 5, 7, 9, 11, 13, 15, 17, 19, 21, 23): Story text overlay
- End page (index 24): No text overlay (or optional closing text)
- Back cover (index 25): No text overlay
"""

import structlog
from typing import Optional, Dict, List

from app.config.book_structure import (
    BOOK_STRUCTURE,
    PageType,
    PageConfig,
    get_filler_url,
    get_filler_pages,
)
from app.services.image_processor import get_image_processor
from app.services.storage import StorageService

logger = structlog.get_logger()


class FillerPagesService:
    """
    Service for processing filler pages with text overlays.

    Handles:
    - Fetching base filler images from R2
    - Processing text overlays via ImageProcessor
    - Uploading processed images to preview-specific paths
    - Returning URLs for processed pages
    """

    def __init__(self):
        self.storage = StorageService()
        self.image_processor = get_image_processor()

    def get_filler_image_url(
        self,
        theme: str,
        style: str,
        filename: str
    ) -> str:
        """
        Get the R2 URL for a base filler image.

        Args:
            theme: Theme identifier (e.g., 'storygift_enchanted_forest')
            style: Book style ('photorealistic' or 'cartoon_3d')
            filename: Filler image filename (e.g., 'dedication.png')

        Returns:
            Full R2 public URL for the filler image
        """
        return get_filler_url(theme, style, filename)

    async def process_single_page(
        self,
        preview_id: str,
        page_config: PageConfig,
        theme: str,
        style: str,
        child_name: str,
        story_texts: Dict[int, str]
    ) -> Optional[str]:
        """
        Process a single filler page and return the processed URL.

        Args:
            preview_id: Preview identifier for storage path
            page_config: Page configuration from BOOK_STRUCTURE
            theme: Theme identifier
            style: Book style
            child_name: Child's name for dedication page
            story_texts: Dict mapping text page number (1-10) to story text

        Returns:
            R2 URL of processed image, or base filler URL if no processing needed
        """
        if not page_config.filler_filename:
            logger.warning(
                "Page has no filler filename",
                page_index=page_config.index,
                page_type=page_config.page_type
            )
            return None

        # Get base filler image URL
        base_url = self.get_filler_image_url(theme, style, page_config.filler_filename)

        # Pages without text overlay return base URL directly
        if not page_config.requires_text_overlay:
            logger.debug(
                "Page does not require text overlay",
                page_index=page_config.index,
                base_url=base_url[:80]
            )
            return base_url

        try:
            # Process based on page type
            if page_config.page_type == PageType.DEDICATION:
                # Dedication page with personalized text
                processed_bytes = await self.image_processor.process_dedication_page(
                    background_url=base_url,
                    child_name=child_name,
                    theme=theme
                )
            elif page_config.page_type == PageType.TEXT:
                # Story text page
                text_page_num = page_config.text_page_number
                if text_page_num is None:
                    logger.error(
                        "Text page missing text_page_number",
                        page_index=page_config.index
                    )
                    return base_url

                story_text = story_texts.get(text_page_num, "")
                if not story_text:
                    logger.warning(
                        "No story text found for page",
                        page_index=page_config.index,
                        text_page_number=text_page_num
                    )
                    return base_url

                processed_bytes = await self.image_processor.process_story_text_page(
                    background_url=base_url,
                    story_text=story_text,
                    theme=theme,
                    text_page_number=text_page_num
                )
            else:
                # Unknown page type requiring text overlay
                logger.warning(
                    "Unexpected page type requiring text overlay",
                    page_index=page_config.index,
                    page_type=page_config.page_type
                )
                return base_url

            # Upload processed image to R2
            r2_path = f"previews/{preview_id}/pages/page_{page_config.index:02d}.png"
            processed_url = await self.storage.upload_image(
                image_bytes=processed_bytes,
                path=r2_path,
                content_type="image/png"
            )

            logger.info(
                "Processed filler page uploaded",
                preview_id=preview_id,
                page_index=page_config.index,
                page_type=page_config.page_type.value,
                r2_url=processed_url[:80]
            )

            return processed_url

        except Exception as e:
            logger.error(
                "Failed to process filler page",
                preview_id=preview_id,
                page_index=page_config.index,
                error=str(e)
            )
            # Return base URL as fallback
            return base_url

    async def process_preview_filler_pages(
        self,
        preview_id: str,
        theme: str,
        style: str,
        child_name: str,
        story_texts: Dict[int, str]
    ) -> Dict[int, str]:
        """
        Process all filler pages for the preview (pages 0-12).

        Args:
            preview_id: Preview identifier
            theme: Theme identifier
            style: Book style
            child_name: Child's name for dedication
            story_texts: Dict mapping text page number (1-10) to story text

        Returns:
            Dict mapping page index to processed/base image URL
        """
        logger.info(
            "Processing preview filler pages",
            preview_id=preview_id,
            theme=theme,
            style=style
        )

        results: Dict[int, str] = {}
        filler_pages = get_filler_pages(preview_only=True)

        for page_config in filler_pages:
            url = await self.process_single_page(
                preview_id=preview_id,
                page_config=page_config,
                theme=theme,
                style=style,
                child_name=child_name,
                story_texts=story_texts
            )

            if url:
                results[page_config.index] = url

        logger.info(
            "Preview filler pages processed",
            preview_id=preview_id,
            pages_count=len(results)
        )

        return results

    async def process_locked_filler_pages(
        self,
        preview_id: str,
        theme: str,
        style: str,
        child_name: str,
        story_texts: Dict[int, str]
    ) -> Dict[int, str]:
        """
        Process all locked filler pages (pages 13-25) for post-payment.

        Args:
            preview_id: Preview identifier
            theme: Theme identifier
            style: Book style
            child_name: Child's name
            story_texts: Dict mapping text page number (1-10) to story text

        Returns:
            Dict mapping page index to processed/base image URL
        """
        logger.info(
            "Processing locked filler pages",
            preview_id=preview_id,
            theme=theme,
            style=style
        )

        results: Dict[int, str] = {}

        # Get all filler pages, filter to locked only
        all_filler_pages = get_filler_pages(preview_only=False)
        locked_filler_pages = [p for p in all_filler_pages if not p.is_preview]

        for page_config in locked_filler_pages:
            url = await self.process_single_page(
                preview_id=preview_id,
                page_config=page_config,
                theme=theme,
                style=style,
                child_name=child_name,
                story_texts=story_texts
            )

            if url:
                results[page_config.index] = url

        logger.info(
            "Locked filler pages processed",
            preview_id=preview_id,
            pages_count=len(results)
        )

        return results

    async def process_all_filler_pages(
        self,
        preview_id: str,
        theme: str,
        style: str,
        child_name: str,
        story_texts: Dict[int, str]
    ) -> Dict[int, str]:
        """
        Process ALL filler pages (both preview and locked).

        Use this for full book generation after payment.

        Args:
            preview_id: Preview identifier
            theme: Theme identifier
            style: Book style
            child_name: Child's name
            story_texts: Dict mapping text page number (1-10) to story text

        Returns:
            Dict mapping page index to processed/base image URL
        """
        logger.info(
            "Processing all filler pages",
            preview_id=preview_id,
            theme=theme,
            style=style
        )

        results: Dict[int, str] = {}
        all_filler_pages = get_filler_pages(preview_only=False)

        for page_config in all_filler_pages:
            url = await self.process_single_page(
                preview_id=preview_id,
                page_config=page_config,
                theme=theme,
                style=style,
                child_name=child_name,
                story_texts=story_texts
            )

            if url:
                results[page_config.index] = url

        logger.info(
            "All filler pages processed",
            preview_id=preview_id,
            pages_count=len(results)
        )

        return results

    def get_filler_page_indices(self, preview_only: bool = False) -> List[int]:
        """
        Get list of filler page indices.

        Args:
            preview_only: If True, only return preview page indices

        Returns:
            List of page indices that are filler pages
        """
        filler_pages = get_filler_pages(preview_only=preview_only)
        return [p.index for p in filler_pages]


# Module-level singleton
_filler_pages_service: Optional[FillerPagesService] = None


def get_filler_pages_service() -> FillerPagesService:
    """Get or create the FillerPagesService singleton."""
    global _filler_pages_service
    if _filler_pages_service is None:
        _filler_pages_service = FillerPagesService()
    return _filler_pages_service
