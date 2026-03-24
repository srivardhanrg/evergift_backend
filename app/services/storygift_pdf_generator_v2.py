"""
StoryGift-style PDF Generator V2 for 26-page book structure.

Generates premium PDFs from the complete 26-page book:
- Cover (index 0): AI-generated
- Dedication (index 1): Filler with text overlay
- Intros (indices 2-3): Filler pages
- Story pages: Alternating AI-generated and text overlays
- End page (index 24): Filler
- Back cover (index 25): Filler

All pages are pre-rendered (text overlays done by ImageProcessor),
so this generator simply assembles them into a PDF.
"""

import asyncio
import os
import tempfile
from io import BytesIO
from typing import Dict, Optional, List
import structlog
import httpx
from PIL import Image

from reportlab.lib.units import inch
from reportlab.lib.colors import Color, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from app.config import get_settings
from app.core.exceptions import StorageError
from app.services.storage import StorageService
from app.config.book_structure import BOOK_STRUCTURE, PageType, TOTAL_PAGE_COUNT

logger = structlog.get_logger()

# Page dimensions: 10x10 inch square (matching print specs)
PAGE_WIDTH = 10 * inch
PAGE_HEIGHT = 10 * inch


class StoryGiftPDFGeneratorV2:
    """
    PDF Generator V2 for 26-page book structure.

    All pages are pre-rendered with text overlays by ImageProcessor,
    so this generator focuses on:
    1. Downloading all page images
    2. Assembling them into a properly ordered PDF
    3. Handling missing pages gracefully
    """

    def __init__(self):
        self.settings = get_settings()
        self.storage = StorageService()
        logger.info("StoryGift PDF Generator V2 initialized")

    async def generate_pdf(
        self,
        preview_id: str,
        child_name: str,
        page_urls: Dict[int, str],
        story_title: str,
        add_blank_back_page: bool = False,
    ) -> str:
        """
        Generate PDF from 26-page book structure.

        Args:
            preview_id: Preview ID for storage paths
            child_name: Child's name (for logging/title)
            page_urls: Dict mapping page index (0-25) to image URL
            story_title: Story title for cover fallback
            add_blank_back_page: True for physical Lulu orders (adds blank page)

        Returns:
            PDF file URL in storage
        """
        try:
            logger.info(
                "Starting V2 PDF generation",
                preview_id=preview_id,
                page_count=len(page_urls),
                total_expected=TOTAL_PAGE_COUNT
            )

            # Download all page images in parallel
            page_images = await self._download_all_images(page_urls)

            # Generate PDF
            pdf_bytes = self._create_pdf(
                page_images=page_images,
                story_title=story_title,
                child_name=child_name,
                add_blank_back_page=add_blank_back_page,
            )

            # Upload to storage
            storage_path = f"final/{preview_id}/storybook_v2.pdf"
            pdf_url = await self.storage.upload_pdf(pdf_bytes, storage_path)

            page_count = len([p for p in page_images.values() if p is not None])
            total_pages = page_count + (1 if add_blank_back_page else 0)

            logger.info(
                "V2 PDF generated successfully",
                preview_id=preview_id,
                pdf_url=pdf_url[:80],
                pages_included=page_count,
                total_pdf_pages=total_pages,
                has_blank_back=add_blank_back_page,
                size_bytes=len(pdf_bytes)
            )

            return pdf_url

        except Exception as e:
            logger.error(
                "V2 PDF generation failed",
                preview_id=preview_id,
                error=str(e)
            )
            raise StorageError(f"PDF generation failed: {str(e)}")

    async def _download_all_images(
        self,
        page_urls: Dict[int, str]
    ) -> Dict[int, Optional[bytes]]:
        """Download all page images in parallel."""
        async with httpx.AsyncClient(timeout=60.0) as client:

            async def fetch(page_index: int, url: str):
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    return page_index, response.content
                except Exception as e:
                    logger.warning(
                        f"Failed to download page {page_index}: {e}",
                        page_index=page_index
                    )
                    return page_index, None

            # Build download tasks
            tasks = [
                fetch(idx, url)
                for idx, url in page_urls.items()
                if url  # Skip None URLs
            ]

            # Download all images concurrently
            results = await asyncio.gather(*tasks)

        images = {idx: data for idx, data in results}
        successful = sum(1 for data in images.values() if data is not None)
        logger.info(
            f"Downloaded {successful}/{len(tasks)} page images",
            successful=successful,
            total=len(tasks)
        )
        return images

    def _create_pdf(
        self,
        page_images: Dict[int, Optional[bytes]],
        story_title: str,
        child_name: str,
        add_blank_back_page: bool = False,
    ) -> bytes:
        """Create the PDF from page images."""

        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Create canvas
            c = canvas.Canvas(tmp_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

            # Process pages in order (0-25)
            for page_config in BOOK_STRUCTURE:
                idx = page_config.index
                image_bytes = page_images.get(idx)

                if image_bytes:
                    self._draw_page(c, image_bytes, idx, page_config.page_type)
                else:
                    # Draw placeholder for missing pages
                    self._draw_placeholder_page(
                        c, idx, page_config.page_type, story_title, child_name
                    )

                c.showPage()

            # Add blank back page for Lulu physical orders
            if add_blank_back_page:
                self._draw_blank_page(c)
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

    def _draw_page(
        self,
        c: canvas.Canvas,
        image_bytes: bytes,
        page_index: int,
        page_type: PageType
    ):
        """Draw a page with its pre-rendered image."""
        try:
            img = Image.open(BytesIO(image_bytes))

            # Ensure correct orientation and mode
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')

            img_reader = ImageReader(img)

            # Draw image to fill entire page (images are 1:1 ratio)
            c.drawImage(
                img_reader,
                0, 0,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                preserveAspectRatio=True,
                anchor='c'
            )

            logger.debug(
                f"Drew page {page_index} ({page_type.value})",
                page_index=page_index
            )

        except Exception as e:
            logger.error(
                f"Failed to draw page {page_index}: {e}",
                page_index=page_index,
                page_type=page_type.value
            )
            # Draw fallback
            c.setFillColor(white)
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
            c.setFillColor(Color(0.7, 0.7, 0.7))
            c.setFont("Helvetica", 24)
            c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2, f"Page {page_index + 1}")

    def _draw_placeholder_page(
        self,
        c: canvas.Canvas,
        page_index: int,
        page_type: PageType,
        story_title: str,
        child_name: str
    ):
        """Draw a placeholder for missing pages."""
        # Light gray background
        c.setFillColor(Color(0.95, 0.95, 0.95))
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        # Page info
        c.setFillColor(Color(0.6, 0.6, 0.6))
        c.setFont("Helvetica", 18)
        c.drawCentredString(
            PAGE_WIDTH/2,
            PAGE_HEIGHT/2 + 20,
            f"Page {page_index + 1}"
        )
        c.setFont("Helvetica", 14)
        c.drawCentredString(
            PAGE_WIDTH/2,
            PAGE_HEIGHT/2 - 10,
            page_type.value.replace('_', ' ').title()
        )

        logger.warning(
            f"Drew placeholder for missing page {page_index}",
            page_index=page_index,
            page_type=page_type.value
        )

    def _draw_blank_page(self, c: canvas.Canvas):
        """Draw a blank white page (for Lulu print jobs)."""
        c.setFillColor(white)
        c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        logger.debug("Drew blank page for Lulu")


# Module-level singleton
_pdf_generator_v2: Optional[StoryGiftPDFGeneratorV2] = None


def get_pdf_generator_v2() -> StoryGiftPDFGeneratorV2:
    """Get or create the PDF Generator V2 singleton."""
    global _pdf_generator_v2
    if _pdf_generator_v2 is None:
        _pdf_generator_v2 = StoryGiftPDFGeneratorV2()
    return _pdf_generator_v2
