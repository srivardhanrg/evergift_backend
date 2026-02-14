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


def _build_download_response(
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

    pdf_path = f"final/{preview['preview_id']}/storygift_book.pdf"
    pdf_url = f"{storage.settings.r2_public_url}/{pdf_path}"

    # Individual image downloads
    image_downloads = []
    if preview.get("hires_images"):
        for img_data in preview["hires_images"]:
            image_path = f"final/{preview['preview_id']}/page_{img_data['page']:02d}.jpg"
            image_signed_url = storage.generate_signed_url(image_path, expires_in=3600)
            image_downloads.append({
                "page": img_data["page"],
                "url": image_signed_url,
                "filename": f"page_{img_data['page']:02d}.jpg",
            })

    days_remaining = max(
        0, (expires_at - datetime.utcnow().replace(tzinfo=expires_at.tzinfo)).days
    )

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
        preview_ready = bool(preview_pdf_url) and generation_phase == "complete"

        # Also check if all pages exist (pages_complete phase or 10+ story pages)
        story_pages = preview.get("story_pages", [])
        all_pages_generated = len(story_pages) >= 10

        # =============================================
        # Step 4: Determine download availability
        # =============================================

        # FAST PATH: Preview says complete — verify PDF on R2 and serve
        if preview_ready:
            pdf_path = f"final/{preview_id}/storygift_book.pdf"
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
                        logger.info("Auto-healed stuck order status", order_id=order.get("order_id"))
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

                return _build_download_response(preview, storage, pdf_exists, pdf_size_mb, expires_at)
            else:
                # Preview says complete but PDF is missing from R2
                logger.warning(
                    "Preview marked complete but PDF not found on R2",
                    preview_id=preview_id,
                    pdf_url=preview_pdf_url,
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

        # Check if pages are complete but PDF hasn't been generated yet
        if generation_phase in ("pages_complete", "pdf_failed"):
            return DownloadResponse(
                status="pdf_missing",
                progress=90,
                message="Your story pages are ready but the PDF needs to be created. Please click 'Retry' to generate it.",
            )

        # Still generating
        if generation_phase == "generating_full" or (preview_status == "purchased" and not preview_ready):
            # Calculate approximate progress
            pages_done = len(story_pages)
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


def _get_expiry(order: dict | None, preview: dict) -> datetime:
    """Calculate expiry datetime from order or preview creation time."""
    if order and order.get("expires_at"):
        return datetime.fromisoformat(order["expires_at"].replace("Z", "+00:00"))

    # Default: 30 days from creation
    created_str = (
        (order.get("created_at") if order else None)
        or preview.get("created_at")
        or datetime.utcnow().isoformat()
    )
    created_at = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
    return created_at + timedelta(days=30)