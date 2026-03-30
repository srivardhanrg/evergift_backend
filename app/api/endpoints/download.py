"""
Download endpoint for completed orders.

Resilient design:
1. Preview-first lookup (bypasses orders table if preview is complete)
2. R2 file existence verification before returning URLs
3. Auto-heals stuck order statuses
4. Handles missing orders gracefully for paid previews
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
import structlog

from app.models.schemas import DownloadResponse
from app.models.database import get_db
from app.models.enums import OrderStatus
from app.services.storage import StorageService

logger = structlog.get_logger()
router = APIRouter()


async def _build_download_response(
    preview: dict,
    storage: StorageService,
    pdf_exists: bool,
    pdf_size_mb: float | None,
    expires_at: datetime,
) -> DownloadResponse:
    """Build the final download response with PDF and image URLs."""
    theme_name = (
        preview.get("theme", "Story")
        .replace("storygift_", "")
        .replace("_", " ")
        .title()
        .replace(" ", "_")
    )
    child_name_clean = preview["child_name"].strip().replace(" ", "_")
    pdf_filename = f"{child_name_clean}_{theme_name}_Book.pdf"

    # Use actual PDF filename from database if available, fallback to default
    preview_pdf_url = preview.get("pdf_url", "")
    if preview_pdf_url:
        # Extract filename from stored URL (e.g., "storybook_v2.pdf" or "storygift_book.pdf")
        pdf_filename_on_r2 = preview_pdf_url.rstrip("/").split("/")[-1]
    else:
        pdf_filename_on_r2 = "storygift_book.pdf"
    pdf_path = f"final/{preview['preview_id']}/{pdf_filename_on_r2}"
    pdf_url = f"{storage.settings.r2_public_url}/{pdf_path}"

    # Individual image downloads
    image_downloads = []
    if preview.get("hires_images"):
        for img_data in preview["hires_images"]:
            image_path = f"final/{preview['preview_id']}/page_{img_data['page']:02d}.jpg"
            image_signed_url = await storage.generate_signed_url(image_path, expires_in=3600)
            image_downloads.append({
                "page": img_data["page"],
                "url": image_signed_url,
                "filename": f"page_{img_data['page']:02d}.jpg",
            })
    elif preview.get("book_structure"):
        # V2 fallback: build image downloads from book_structure
        book_structure = preview["book_structure"]
        for idx_str, page_data in sorted(book_structure.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            if page_data.get("url"):
                try:
                    page_num = int(idx_str)
                except (ValueError, TypeError):
                    continue
                image_downloads.append({
                    "page": page_num,
                    "url": page_data["url"],
                    "filename": f"page_{page_num:02d}.jpg",
                })

    now = datetime.utcnow()
    # Make both naive or both aware for subtraction
    if expires_at.tzinfo is not None:
        now = now.replace(tzinfo=expires_at.tzinfo)
    days_remaining = max(0, (expires_at - now).days)

    return DownloadResponse(
        status="ready",
        downloads={
            "pdf": {
                "url": pdf_url,
                "filename": pdf_filename,
                "size_mb": pdf_size_mb,
                "expires_in_seconds": 3600,
            },
            "images": image_downloads,
        },
        expires_at=expires_at,
        days_remaining=days_remaining,
    )


@router.get("/download/{identifier}", response_model=DownloadResponse)
async def get_download(identifier: str):
    """
    Get download links for completed order.

    Returns signed URLs for PDF and individual images.
    Links are time-limited for security.

    Accepts either order_id or preview_id - will look up the order accordingly.

    Resilient lookup order:
    1. Try orders table (by order_id, then by preview_id)
    2. If no order found, fall back to preview-only lookup
    3. Verify PDF exists on R2 before returning "ready"
    """

    try:
        logger.info("Getting download links", identifier=identifier)

        db = get_db()
        storage = StorageService()

        # =============================================
        # Step 1: Find order (optional — may not exist)
        # =============================================
        order = None
        order_response = db.table("orders").select("*").eq("order_id", identifier).execute()

        if not order_response.data:
            order_response = db.table("orders").select("*").eq("preview_id", identifier).execute()

        if order_response.data:
            order = order_response.data[0]

        # =============================================
        # Step 2: Find preview (required)
        # =============================================
        preview_id = order["preview_id"] if order else identifier
        if not order:
            logger.info(
                "No order found for identifier — treating as preview_id directly",
                identifier=identifier,
            )
        preview_response = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_response.data:
            raise HTTPException(status_code=404, detail="Preview not found")

        preview = preview_response.data[0]
        preview_pdf_url = preview.get("pdf_url")
        generation_phase = preview.get("generation_phase", "preview")
        preview_status = preview.get("status", "")

        # =============================================
        # Step 3: Check preview completeness
        # =============================================
        ready_phases = {"complete", "preparing_print", "submitting_print", "print_submitted"}
        preview_ready = bool(preview_pdf_url) and generation_phase in ready_phases

        # Also check if all pages exist (pages_complete phase or 10+ story pages)
        story_pages = preview.get("story_pages", [])
        book_structure = preview.get("book_structure")
        # V2 stores pages in book_structure (26 entries for full book); legacy uses story_pages
        all_pages_generated = len(story_pages) >= 10 or (bool(book_structure) and len(book_structure) >= 10)

        # =============================================
        # Step 4: Determine download availability
        # =============================================

        # FAST PATH: Preview says complete — verify PDF on R2 and serve
        if preview_ready:
            # Use actual filename from pdf_url, not hardcoded name
            if preview_pdf_url:
                pdf_filename_on_r2 = preview_pdf_url.rstrip("/").split("/")[-1]
            else:
                pdf_filename_on_r2 = "storygift_book.pdf"
            pdf_path = f"final/{preview_id}/{pdf_filename_on_r2}"
            pdf_exists = await storage.file_exists(pdf_path)

            if pdf_exists:
                # PDF is on R2 — serve the download
                logger.info("PDF verified on R2", preview_id=preview_id)

                # Auto-heal stuck order status if needed
                if order and order["status"] != OrderStatus.COMPLETED.value:
                    try:
                        db.table("orders").update({
                            "status": OrderStatus.COMPLETED.value,
                            "pdf_url": preview_pdf_url,
                        }).eq("order_id", order.get("order_id")).execute()
                        logger.info(
                            "Auto-healed stuck order status to COMPLETED",
                            order_id=order.get("order_id"),
                            old_status=order["status"],
                            pdf_url=preview_pdf_url,
                        )
                    except Exception as fix_err:
                        logger.warning("Failed to auto-heal order status", error=str(fix_err))

                # Build expiry
                expires_at = _get_expiry(order, preview)

                # Get PDF size (optional)
                pdf_size_mb = None
                try:
                    pdf_size_bytes = await storage.get_file_size(pdf_path)
                    pdf_size_mb = round(pdf_size_bytes / 1024 / 1024, 1)
                except Exception:
                    pass

                return await _build_download_response(preview, storage, pdf_exists, pdf_size_mb, expires_at)
            else:
                # Preview says complete but PDF is missing from R2
                logger.warning(
                    "Preview marked complete but PDF not found on R2",
                    preview_id=preview_id,
                    pdf_url=preview_pdf_url,
                )
                logger.warning(
                    "Returning pdf_missing: PDF not found on R2",
                    identifier=identifier,
                    preview_id=preview_id,
                    expected_r2_path=pdf_path,
                    generation_phase=generation_phase,
                    all_pages_generated=all_pages_generated,
                )

                if all_pages_generated:
                    return DownloadResponse(
                        status="pdf_missing",
                        progress=90,
                        message="Your story pages are ready but the PDF file needs to be recreated. Please click 'Retry' to regenerate it.",
                    )
                else:
                    return DownloadResponse(
                        status="generating",
                        progress=50,
                        message="Your book is still being created. Please check back in a few minutes.",
                    )

        # Pages done, PDF is auto-generating in background — keep polling
        if generation_phase == "pages_complete":
            pages_done = len(story_pages) or (len(book_structure) if book_structure else 0)
            progress = min(90, int((pages_done / 10) * 80) + 10)
            return DownloadResponse(
                status="generating",
                progress=progress,
                message="Your pages are ready! Creating your PDF now, this takes about 1 minute.",
            )

        # PDF specifically failed — user needs to manually retry
        if generation_phase == "pdf_failed":
            return DownloadResponse(
                status="pdf_missing",
                progress=90,
                message="Your story pages are ready but the PDF needs to be created. Please click 'Retry' to generate it.",
            )

        # Still generating
        if generation_phase == "generating_full" or (preview_status == "purchased" and not preview_ready):
            # Calculate approximate progress
            pages_done = len(story_pages) or (len(book_structure) if book_structure else 0)
            progress = min(85, int((pages_done / 10) * 80) + 10) if pages_done > 5 else 25

            return DownloadResponse(
                status="generating",
                progress=progress,
                message="Your book is being created with beautiful illustrations. Please check back in a few minutes.",
            )

        # Preview phase (not purchased yet)
        if generation_phase == "preview":
            return DownloadResponse(
                status="not_purchased",
                progress=0,
                message="Please purchase your book to unlock the full PDF download.",
            )

        # Failed generation
        if generation_phase == "failed":
            return DownloadResponse(
                status="failed",
                progress=0,
                message="Book generation failed. Please contact support for assistance.",
            )

        # Fallback: use order status if we have an order
        if order:
            if order["status"] == OrderStatus.FAILED.value:
                raise HTTPException(
                    status_code=500,
                    detail="Order generation failed. Please contact support.",
                )
            elif order["status"] in (OrderStatus.PAID.value, OrderStatus.GENERATING_PDF.value):
                return DownloadResponse(
                    status="generating",
                    progress=50,
                    message="Your book is being created. Please check back in a few minutes.",
                )

        # Last fallback
        raise HTTPException(
            status_code=400,
            detail=f"Unable to determine download status. Generation phase: {generation_phase}",
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Failed to get download links", identifier=identifier, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve download links. Please try again.",
        )


def _parse_datetime(dt_str: str) -> datetime:
    """Parse a datetime string, handling Python 3.10 fromisoformat limitations.

    Python 3.10 only accepts 0, 3, or 6 fractional digits. Supabase/Postgres
    can return 5 digits (e.g. '2026-03-21T04:28:36.03677+00:00'), so we
    normalize fractional seconds to 6 digits before parsing.
    """
    import re

    clean = dt_str.strip()
    if clean.endswith("Z"):
        clean = clean[:-1]

    # Strip timezone offset, parse as naive
    tz_match = re.search(r'[+-]\d{2}:\d{2}$', clean)
    if tz_match:
        clean = clean[:tz_match.start()]

    # Normalize fractional seconds to exactly 6 digits
    frac_match = re.search(r'\.(\d+)$', clean)
    if frac_match:
        frac = frac_match.group(1).ljust(6, '0')[:6]
        clean = clean[:frac_match.start()] + '.' + frac

    return datetime.fromisoformat(clean)


def _get_expiry(order: dict | None, preview: dict) -> datetime:
    """Calculate expiry datetime from order or preview creation time."""
    if order and order.get("expires_at"):
        return _parse_datetime(order["expires_at"])

    # Default: 30 days from creation
    created_str = (
        (order.get("created_at") if order else None)
        or preview.get("created_at")
        or datetime.utcnow().isoformat()
    )
    created_at = _parse_datetime(created_str)
    return created_at + timedelta(days=30)