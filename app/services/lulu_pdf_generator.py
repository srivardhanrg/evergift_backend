"""
Lulu Print-Spec PDF Generator

Generates two PDFs required by Lulu for print production:

1. INTERIOR PDF
   - Page size: 8.5 x 8.5 inches + 0.125" bleed = 8.75 x 8.75 inches per page
   - 24 pages total (indices 1-24 from V2 book structure, divisible by 4 for saddle stitch)
   - Layout: ~80% image / ~20% story text, matching StoryGift screen preview
   - No crop marks required by Lulu (bleed only)
   - TODO: Back cover (index 25) not yet included in cover wrap

2. COVER WRAP PDF
   - Single landscape spread: back + spine + front, all in one PDF page
   - Spine width calculated by Lulu's cover-dimensions API (or ~0.12" for 24 pages / 80# coated)
   - Safety zone: 0.125" bleed on all outer edges, 0.0625" inside spine
   - We generate a simple full-bleed colour cover with child name + title

Both PDFs are uploaded to R2 and their public URLs are returned for submission to Lulu.
"""

import asyncio
import hashlib
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
import os as _os

from app.config import get_settings
from app.services.storage import StorageService

# ---------------------------------------------------------------------------
# Register embeddable TTF fonts (Bitstream Vera — bundled with ReportLab)
# Lulu requires ALL fonts to be embedded in the PDF.
# Standard Type1 fonts (Helvetica etc.) are NOT embedded by ReportLab by default.
# ---------------------------------------------------------------------------
_RL_FONTS_DIR = _os.path.join(_os.path.dirname(reportlab.__file__), "fonts")
pdfmetrics.registerFont(TTFont("Vera",      _os.path.join(_RL_FONTS_DIR, "Vera.ttf")))
pdfmetrics.registerFont(TTFont("Vera-Bold", _os.path.join(_RL_FONTS_DIR, "VeraBd.ttf")))

# Aliases so the rest of the code reads naturally
FONT_REGULAR = "Vera"
FONT_BOLD    = "Vera-Bold"

logger = structlog.get_logger()

# ---------------------------------------------------------------------------
# Lulu 8.5 x 8.5" print spec
# ---------------------------------------------------------------------------
BLEED = 0.125 * inch                        # 0.125 inch bleed on all sides
SAFETY_MARGIN = 0.50 * inch                 # Interior: 0.50" from trim edge (Lulu spec)
PAGE_W = (8.5 + 2 * 0.125) * inch          # 8.75" trimmed + bleed (both sides)
PAGE_H = (8.5 + 2 * 0.125) * inch          # 8.75"

# ---------------------------------------------------------------------------
# Spine widths per cover type (Lulu official spec)
# Hardcover casewrap (24-84 pages): 0.25"
# Saddle stitch / softcover:        no spine (0.0")
# ---------------------------------------------------------------------------
HARDCOVER_SPINE_W = 0.25 * inch            # Lulu spec: hardcover 24+ pages = 0.25"
SOFTCOVER_SPINE_W = 0.0  * inch            # Saddle stitch has NO spine

# ---------------------------------------------------------------------------
# Cover safety zones per cover type (Lulu official spec)
# Hardcover casewrap:  0.75" from trim edge
# Softcover / saddle:  0.50" from trim edge
# ---------------------------------------------------------------------------
HARDCOVER_COVER_SAFETY = 0.75 * inch
SOFTCOVER_COVER_SAFETY = 0.50 * inch

# Legacy alias kept for interior pages (unchanged — interior is always 0.50")
SPINE_W = HARDCOVER_SPINE_W                # kept for backward compat

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

# ----------------------------------------------------------------
# CRITICAL: Page count must meet Lulu requirements
# ----------------------------------------------------------------
# Lulu Print API requirements:
# - Saddle Stitch (softcover): 4-48 pages, MUST BE EVEN
# - Hardcover (casewrap): 24-800 pages, MUST BE EVEN
# - Page count MUST be divisible by 4 for proper binding (multiples of 4)
#
# Our choice: 24 pages (meets both softcover and hardcover minimums)
# This value is validated in lulu_tasks.py before Lulu API submission
# ----------------------------------------------------------------
TOTAL_PAGES = 24                            # 24 pages: even, divisible by 4, meets all requirements

# Gutter margin: minimum 0.20" from the inner (binding) edge — using 0.25" for safety
GUTTER = 0.25 * inch


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
        # Gutter: Lulu requires min 0.20" from binding edge. We use 0.25" for safety.
        # Odd pages (1,3,5...) are on the RIGHT side of the spread → gutter is on the LEFT.
        # Even pages (2,4,6...) are on the LEFT side of the spread → gutter is on the RIGHT.
        is_right_page = (page_number % 2 != 0)  # odd → right side
        outer_pad = BLEED + SAFETY_MARGIN                   # outer edge (always 0.50" from trim)
        inner_pad = BLEED + SAFETY_MARGIN + GUTTER           # binding edge (0.75" from trim)

        left_pad  = inner_pad if not is_right_page else outer_pad
        right_pad = inner_pad if is_right_page     else outer_pad

        text_width = PAGE_W - left_pad - right_pad
        text_center_x = left_pad + text_width / 2            # shift center toward outer edge

        c.setFillColor(TEXT_COLOR)
        c.setFont(FONT_REGULAR, BODY_FONT_SIZE)

        # Simple word-wrap
        words = story_text.split()
        lines: List[str] = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, FONT_REGULAR, BODY_FONT_SIZE) <= text_width:
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
            c.drawCentredString(text_center_x, y_start, line)
            y_start -= line_height

    # ---- Page number (subtle, inside trim on outer edge) ----
    if not is_cover and page_number > 0:
        is_right_page = (page_number % 2 != 0)
        c.setFont(FONT_REGULAR, 8)
        c.setFillColor(HexColor("#AAAAAA"))
        if is_right_page:
            # Right page: page number at bottom-right (outer edge)
            c.drawRightString(PAGE_W - BLEED - SAFETY_MARGIN, BLEED + 0.25 * inch, str(page_number))
        else:
            # Left page: page number at bottom-left (outer edge)
            c.drawString(BLEED + SAFETY_MARGIN, BLEED + 0.25 * inch, str(page_number))


def _draw_blank_page(c: canvas.Canvas) -> None:
    """Draw a blank (padding) page."""
    c.setFillColor(TEXT_BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


async def generate_interior_pdf(
    pages: List[Dict],
    preview_id: str,
    child_name: str,
) -> Tuple[str, str]:
    """
    Generate a Lulu-spec interior PDF for a 24-page story (indices 1-24).

    Args:
        pages: list of dicts with keys: page_number, image_url, story_text
        preview_id: used to name the uploaded file
        child_name: for logging

    Returns:
        Tuple of (R2 public URL, MD5 hash) for the uploaded PDF
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

    # Calculate MD5 hash for Lulu API integrity verification
    pdf_md5 = hashlib.md5(pdf_bytes).hexdigest()

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
        pdf_md5=pdf_md5,
        duration_ms=duration_ms,
    )
    return pdf_url, pdf_md5


# ---------------------------------------------------------------------------
# Cover Wrap PDF
# ---------------------------------------------------------------------------

async def generate_cover_pdf(
    cover_image_url: Optional[str],
    child_name: str,
    story_title: str,
    preview_id: str,
    cover_type: str = "hardcover",
    spine_width_inches: Optional[float] = None,  # If None, derived from cover_type
) -> Tuple[str, str]:
    """
    Generate a Lulu-spec cover wrap PDF.

    Per Lulu official specifications (8.5" × 8.5" square, 24 pages):
    - Softcover (Saddle Stitch): 17.25" × 8.75" (no spine)
    - Hardcover (Case Wrap):     19.00" × 10.25" (0.25" spine, includes board turn-in)

    The cover is a single landscape page: [back] [spine] [front]

    Args:
        cover_image_url: optional URL of the generated cover image
        child_name: printed on cover
        story_title: printed on cover
        preview_id: for naming the R2 file
        cover_type: "softcover" (saddle stitch) or "hardcover" (case wrap)
        spine_width_inches: manual spine override (default: 0.0 softcover, 0.25 hardcover)

    Returns:
        Tuple of (R2 public URL, MD5 hash) for the uploaded cover PDF
    """
    import time as _time
    start_time = _time.monotonic()

    storage = StorageService()

    # Lulu official cover dimensions (per spec, not calculated)
    # These are EXACT specifications from Lulu for 8.5" × 8.5" square books with 24 pages
    if cover_type == "softcover":
        # Saddle stitch: 17.25" × 8.75" (no spine)
        wrap_w = 17.25 * inch
        wrap_h = 8.75 * inch
        _spine_inches = 0.0  # Saddle stitch has no spine
        _cover_safety = SOFTCOVER_COVER_SAFETY  # 0.50" from trim
    else:
        # Hardcover casewrap: 19.00" × 10.25" (includes 0.25" spine + board turn-in)
        wrap_w = 19.0 * inch
        wrap_h = 10.25 * inch
        _spine_inches = 0.25  # Hardcover spine width for 24 pages
        _cover_safety = HARDCOVER_COVER_SAFETY  # 0.75" from trim

    # Allow manual override of spine width if provided (rare, for custom page counts)
    if spine_width_inches is not None:
        _spine_inches = spine_width_inches

    spine = _spine_inches * inch

    logger.info(
        "Generating Lulu cover PDF - starting",
        preview_id=preview_id,
        child_name=child_name,
        story_title=story_title[:30] + "..." if len(story_title) > 30 else story_title,
        has_cover_image=bool(cover_image_url),
        cover_type=cover_type,
        spine_width_inches=_spine_inches,
        cover_safety_inches=_cover_safety / inch,
        wrap_width_inches=wrap_w / inch,
        wrap_height_inches=wrap_h / inch,
    )

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

    # ---- Calculate panel dimensions ----
    # Layout: [back panel] [spine] [front panel]
    # For symmetry, center the spine and divide remaining width equally
    if _spine_inches > 0:
        # Hardcover: total 19", spine 0.25" centered
        # Spine center: wrap_w / 2
        # Back panel: 0 to (spine_center - spine/2)
        # Front panel: (spine_center + spine/2) to wrap_w
        spine_center_x = wrap_w / 2
        spine_left_x = spine_center_x - spine / 2
        spine_right_x = spine_center_x + spine / 2

        back_w = spine_left_x
        front_x = spine_right_x
        front_w = wrap_w - spine_right_x
    else:
        # Softcover: total 17.25", no spine
        # Split equally: back = left half, front = right half
        back_w = wrap_w / 2
        front_x = wrap_w / 2
        front_w = wrap_w / 2

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
    # Title must be inside safety zone: bleed + cover_safety from top edge
    # e.g. hardcover: bleed (0.125") + safety (0.75") = 0.875" from page top
    c.setFillColor(COVER_BG_COLOR)
    overlay_h = _cover_safety + BLEED + 0.5 * inch   # Safety zone + some visual breathing room
    c.rect(front_x, wrap_h - overlay_h, front_w, overlay_h, fill=1, stroke=0)

    # Title y position: inside safety zone from the TOP trim
    # Top of text should be at least (bleed + _cover_safety) from top page edge
    title_y = wrap_h - BLEED - _cover_safety - 0.05 * inch
    subtitle_y = title_y - 0.45 * inch

    c.setFillColor(white)
    c.setFont(FONT_BOLD, 20)
    c.drawCentredString(front_x + front_w / 2, title_y, story_title[:40])
    c.setFont(FONT_REGULAR, 14)
    c.drawCentredString(front_x + front_w / 2, subtitle_y, f"Starring {child_name}")

    # ---- Back cover (left panel) ----
    c.setFillColor(COVER_BG_COLOR)
    c.rect(0, 0, back_w, wrap_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont(FONT_REGULAR, 10)
    c.drawCentredString(
        back_w / 2,  # Center of back panel
        BLEED + _cover_safety,  # Safety zone from bottom trim (hardcover: 0.75", softcover: 0.50")
        "A personalised storybook by StoryGift · storygift.in",
    )

    # ---- Spine (only for hardcover) ----
    if _spine_inches > 0:
        c.setFillColor(COVER_BG_COLOR)
        c.rect(spine_left_x, 0, spine, wrap_h, fill=1, stroke=0)

        # Spine text (rotated) — only if spine is wide enough
        if _spine_inches >= 0.18:
            c.saveState()
            c.translate(spine_center_x, wrap_h / 2)
            c.rotate(90)
            c.setFillColor(white)
            c.setFont(FONT_BOLD, 8)
            c.drawCentredString(0, 0, f"{story_title} · {child_name}")
            c.restoreState()

    c.save()
    pdf_bytes = pdf_buffer.getvalue()

    # Calculate MD5 hash for Lulu API integrity verification
    pdf_md5 = hashlib.md5(pdf_bytes).hexdigest()

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
        pdf_md5=pdf_md5,
        duration_ms=duration_ms,
        has_cover_image=bool(cover_img_bytes),
    )
    return cover_url, pdf_md5
