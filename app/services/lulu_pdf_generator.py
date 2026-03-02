"""
Lulu Print-Spec PDF Generator

Generates two PDFs required by Lulu for print production:

1. INTERIOR PDF
   - Page size: 8.5 x 8.5 inches + 0.125" bleed = 8.75 x 8.75 inches per page
   - 12 pages total (10 story pages padded to next multiple of 4 for saddle stitch)
   - Layout: ~80% image / ~20% story text, matching StoryGift screen preview
   - No crop marks required by Lulu (bleed only)

2. COVER WRAP PDF
   - Single landscape spread: back + spine + front, all in one PDF page
   - Spine width calculated by Lulu's cover-dimensions API (or ~0.06" for 12 pages / 80# coated)
   - Safety zone: 0.125" bleed on all outer edges, 0.0625" inside spine
   - We generate a simple full-bleed colour cover with child name + title

Both PDFs are uploaded to R2 and their public URLs are returned for submission to Lulu.
"""

import asyncio
import io
import tempfile
from typing import List, Dict, Optional, Tuple
import httpx
import structlog
from PIL import Image, ImageDraw, ImageFont

from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from app.config import get_settings
from app.services.storage import StorageService

logger = structlog.get_logger()

# ---------------------------------------------------------------------------
# Lulu 8.5 x 8.5" saddle stitch print spec
# ---------------------------------------------------------------------------
BLEED = 0.125 * inch                        # 0.125 inch bleed on all sides
SAFETY_MARGIN = 0.50 * inch                 # Lulu requires 0.50" from trim edge for all content
PAGE_W = (8.5 + 2 * 0.125) * inch          # 8.75" trimmed + bleed (both sides)
PAGE_H = (8.5 + 2 * 0.125) * inch          # 8.75"

# Spine width for 12 pages of 80# coated paper ≈ 0.06 inches
SPINE_W = 0.06 * inch

# Image / text split (matching StoryGift preview: 80 / 20)
IMAGE_AREA_H = 0.80 * PAGE_H
TEXT_AREA_H = 0.20 * PAGE_H

# Font sizes
TITLE_FONT_SIZE = 18
BODY_FONT_SIZE = 13

# Brand colours
COVER_BG_COLOR = HexColor("#FF6B9D")        # StoryGift pink
COVER_TEXT_COLOR = white
TEXT_BG_COLOR = HexColor("#FFF0F5")         # Soft pink
TEXT_COLOR = HexColor("#2D2D2D")

TOTAL_PAGES = 12                            # Must be multiple of 4 for saddle stitch


# ---------------------------------------------------------------------------
# Helper: download image bytes
# ---------------------------------------------------------------------------

async def _download_image(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url)
    resp.raise_for_status()
    return resp.content


# ---------------------------------------------------------------------------
# Interior PDF
# ---------------------------------------------------------------------------

def _draw_story_page(
    c: canvas.Canvas,
    image_bytes: Optional[bytes],
    story_text: str,
    page_number: int,
    is_cover: bool = False,
) -> None:
    """Draw a single story page onto the ReportLab canvas."""

    # ---- Background ----
    c.setFillColor(TEXT_BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # ---- Image area ----
    if image_bytes:
        try:
            img_reader = ImageReader(io.BytesIO(image_bytes))
            # Draw image filling the top 80%, respecting bleed margin on sides
            c.drawImage(
                img_reader,
                x=0,
                y=TEXT_AREA_H,
                width=PAGE_W,
                height=IMAGE_AREA_H,
                preserveAspectRatio=False,
            )
        except Exception as e:
            logger.warning("Could not draw image on page", page=page_number, error=str(e))

    # ---- Text area background ----
    c.setFillColor(TEXT_BG_COLOR)
    c.rect(0, 0, PAGE_W, TEXT_AREA_H, fill=1, stroke=0)

    # ---- Story text ----
    if story_text:
        text_padding = BLEED + SAFETY_MARGIN   # 0.50" from trim edge (Lulu requirement)
        text_width = PAGE_W - 2 * text_padding
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", BODY_FONT_SIZE)

        # Simple word-wrap
        words = story_text.split()
        lines: List[str] = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, "Helvetica", BODY_FONT_SIZE) <= text_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        line_height = BODY_FONT_SIZE * 1.4
        total_text_h = len(lines) * line_height
        y_start = TEXT_AREA_H / 2 + total_text_h / 2 - line_height / 2

        for line in lines[:4]:   # max 4 lines to stay in zone
            c.drawCentredString(PAGE_W / 2, y_start, line)
            y_start -= line_height

    # ---- Page number (subtle, bottom right, inside trim) ----
    if not is_cover and page_number > 0:
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor("#AAAAAA"))
        c.drawRightString(PAGE_W - BLEED - SAFETY_MARGIN, BLEED + 0.25 * inch, str(page_number))


def _draw_blank_page(c: canvas.Canvas) -> None:
    """Draw a blank (padding) page."""
    c.setFillColor(TEXT_BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


async def generate_interior_pdf(
    pages: List[Dict],
    preview_id: str,
    child_name: str,
) -> str:
    """
    Generate a Lulu-spec interior PDF for a 10-page story.

    Args:
        pages: list of dicts with keys: page_number, image_url, story_text
        preview_id: used to name the uploaded file
        child_name: for logging

    Returns:
        R2 public URL of the uploaded PDF
    """
    import time as _time
    start_time = _time.monotonic()

    settings = get_settings()
    storage = StorageService()

    logger.info(
        "Generating Lulu interior PDF - starting",
        preview_id=preview_id,
        child_name=child_name,
        input_pages_count=len(pages),
        target_pages=TOTAL_PAGES,
    )

    # Download all images concurrently
    image_tasks = {}
    for page in pages:
        url = page.get("image_url") or page.get("url", "")
        if url:
            image_tasks[page["page_number"]] = _download_image(url)

    image_bytes_map: Dict[int, bytes] = {}
    if image_tasks:
        results = await asyncio.gather(*image_tasks.values(), return_exceptions=True)
        for page_num, result in zip(image_tasks.keys(), results):
            if isinstance(result, bytes):
                image_bytes_map[page_num] = result
            else:
                logger.warning("Failed to download page image", page=page_num, error=str(result))

    # Build PDF in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(PAGE_W, PAGE_H))

    # Sort pages by page_number; page 0 = cover, 1-10 = story
    sorted_pages = sorted(pages, key=lambda p: p.get("page_number", 0))

    drawn = 0
    for page in sorted_pages:
        page_num = page.get("page_number", 0)
        story_text = page.get("story_text") or page.get("text", "")
        is_cover = page_num == 0
        img = image_bytes_map.get(page_num)

        _draw_story_page(c, img, story_text, page_num, is_cover=is_cover)
        c.showPage()
        drawn += 1

    # Pad to TOTAL_PAGES (12) with blank pages
    while drawn < TOTAL_PAGES:
        _draw_blank_page(c)
        c.showPage()
        drawn += 1

    c.save()
    pdf_bytes = pdf_buffer.getvalue()

    # Upload to R2
    r2_key = f"lulu/{preview_id}/interior.pdf"
    pdf_url = await storage.upload_pdf(
        pdf_bytes=pdf_bytes,
        path=r2_key,
    )

    duration_ms = round((_time.monotonic() - start_time) * 1000)
    pdf_size_kb = round(len(pdf_bytes) / 1024, 1)

    logger.info(
        "Interior PDF generated and uploaded",
        preview_id=preview_id,
        url=pdf_url[:80] + "..." if pdf_url else None,
        pages_drawn=drawn,
        images_downloaded=len(image_bytes_map),
        pdf_size_kb=pdf_size_kb,
        duration_ms=duration_ms,
    )
    return pdf_url


# ---------------------------------------------------------------------------
# Cover Wrap PDF
# ---------------------------------------------------------------------------

async def generate_cover_pdf(
    cover_image_url: Optional[str],
    child_name: str,
    story_title: str,
    preview_id: str,
    spine_width_inches: float = 0.06,
) -> str:
    """
    Generate a Lulu-spec cover wrap PDF.

    The cover is a single landscape page:
      width  = 2 * (trim_width + bleed) + spine
      height = trim_height + 2 * bleed

    Args:
        cover_image_url: optional URL of the generated cover image
        child_name: printed on cover
        story_title: printed on cover
        preview_id: for naming the R2 file
        spine_width_inches: calculated spine width (default 0.06" for 12 pages 80# coated)

    Returns:
        R2 public URL of the uploaded cover PDF
    """
    import time as _time
    start_time = _time.monotonic()

    storage = StorageService()

    logger.info(
        "Generating Lulu cover PDF - starting",
        preview_id=preview_id,
        child_name=child_name,
        story_title=story_title[:30] + "..." if len(story_title) > 30 else story_title,
        has_cover_image=bool(cover_image_url),
        spine_width_inches=spine_width_inches,
    )

    trim_w = 8.5 * inch
    trim_h = 8.5 * inch
    bleed = BLEED
    spine = spine_width_inches * inch

    # Total wrap dimensions
    wrap_w = 2 * (trim_w + bleed) + spine
    wrap_h = trim_h + 2 * bleed

    # Download cover image if provided
    cover_img_bytes: Optional[bytes] = None
    if cover_image_url:
        try:
            cover_img_bytes = await _download_image(cover_image_url)
        except Exception as e:
            logger.warning("Could not download cover image", error=str(e))

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(wrap_w, wrap_h))

    # ---- Full-bleed pink background ----
    c.setFillColor(COVER_BG_COLOR)
    c.rect(0, 0, wrap_w, wrap_h, fill=1, stroke=0)

    # ---- Front cover (right half) ----
    front_x = bleed + trim_w + spine  # x-start of front cover area
    front_w = trim_w + bleed          # extends to right bleed edge

    if cover_img_bytes:
        try:
            img_reader = ImageReader(io.BytesIO(cover_img_bytes))
            c.drawImage(
                img_reader,
                x=front_x,
                y=0,
                width=front_w,
                height=wrap_h,
                preserveAspectRatio=False,
            )
        except Exception as e:
            logger.warning("Could not draw cover image", error=str(e))

    # ---- Front cover: title overlay ----
    c.setFillColor(COVER_BG_COLOR)
    overlay_h = 1.6 * inch
    c.rect(front_x, wrap_h - overlay_h, front_w, overlay_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(front_x + front_w / 2, wrap_h - 0.7 * inch, story_title[:40])
    c.setFont("Helvetica", 14)
    c.drawCentredString(front_x + front_w / 2, wrap_h - 1.1 * inch, f"Starring {child_name}")

    # ---- Back cover (left half) ----
    c.setFillColor(COVER_BG_COLOR)
    c.rect(0, 0, bleed + trim_w, wrap_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica", 10)
    c.drawCentredString(
        (bleed + trim_w) / 2,
        bleed + SAFETY_MARGIN,  # 0.50" from trim edge (was 0.275" - too close)
        "A personalised storybook by StoryGift · storygift.in",
    )

    # ---- Spine ----
    spine_x = bleed + trim_w
    c.setFillColor(COVER_BG_COLOR)
    c.rect(spine_x, 0, spine, wrap_h, fill=1, stroke=0)

    # Spine text (rotated) — only if spine is wide enough
    if spine_width_inches >= 0.18:
        c.saveState()
        c.translate(spine_x + spine / 2, wrap_h / 2)
        c.rotate(90)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(0, 0, f"{story_title} · {child_name}")
        c.restoreState()

    c.save()
    pdf_bytes = pdf_buffer.getvalue()

    # Upload to R2
    r2_key = f"lulu/{preview_id}/cover.pdf"
    cover_url = await storage.upload_pdf(
        pdf_bytes=pdf_bytes,
        path=r2_key,
    )

    duration_ms = round((_time.monotonic() - start_time) * 1000)
    pdf_size_kb = round(len(pdf_bytes) / 1024, 1)

    logger.info(
        "Cover PDF generated and uploaded",
        preview_id=preview_id,
        url=cover_url[:80] + "..." if cover_url else None,
        pdf_size_kb=pdf_size_kb,
        duration_ms=duration_ms,
        has_cover_image=bool(cover_img_bytes),
    )
    return cover_url
