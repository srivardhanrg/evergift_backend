"""
PDF regeneration endpoint.

Allows re-creating the PDF for a preview that has all 10 pages
but whose PDF file is missing or failed to upload.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
import structlog

from app.models.database import get_db
from app.models.enums import OrderStatus
from app.services.storage import StorageService
from app.services.storygift_pdf_generator import StoryGiftPDFGeneratorService

logger = structlog.get_logger()
router = APIRouter()


async def _regenerate_pdf_task(preview_id: str):
    """Background task to regenerate PDF from existing pages."""
    try:
        db = get_db()
        preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_result.data:
            logger.error("Preview not found for PDF regeneration", preview_id=preview_id)
            return

        preview = preview_result.data[0]
        story_pages = preview.get("story_pages", [])
        child_name = preview.get("child_name", "Child")
        theme = preview.get("theme", "storygift_enchanted_forest")

        if len(story_pages) < 10:
            logger.error(
                "Not enough pages for PDF regeneration",
                preview_id=preview_id,
                page_count=len(story_pages),
            )
            db.table("previews").update({
                "generation_phase": "pdf_failed",
            }).eq("preview_id", preview_id).execute()
            return

        # Mark as regenerating
        db.table("previews").update({
            "generation_phase": "generating_pdf",
        }).eq("preview_id", preview_id).execute()

        # Get story title
        from app.background.storygift_tasks import get_theme, sanitize_child_name
        safe_child_name = sanitize_child_name(child_name)
        template = get_theme(theme)
        story_title = (
            template.get_title(safe_child_name)
            if hasattr(template, "get_title")
            else f"{safe_child_name}'s Adventure"
        )

        # Cover URL
        cover_url = preview.get("cover_url")
        hires_images = preview.get("hires_images", [])
        if not cover_url and hires_images and isinstance(hires_images[0], dict):
            cover_url = hires_images[0]["url"]

        # Generate PDF
        pdf_generator = StoryGiftPDFGeneratorService()
        pdf_url = await pdf_generator.generate_storygift_pdf(
            preview_id=preview_id,
            child_name=safe_child_name,
            story_pages=story_pages,
            story_title=story_title,
            cover_image_url=cover_url,
        )

        # Update preview
        db.table("previews").update({
            "pdf_url": pdf_url,
            "generation_phase": "complete",
        }).eq("preview_id", preview_id).execute()

        # Update associated order if exists
        order_response = (
            db.table("orders").select("order_id").eq("preview_id", preview_id).execute()
        )
        if order_response.data:
            order_id = order_response.data[0]["order_id"]
            db.table("orders").update({
                "pdf_url": pdf_url,
                "status": OrderStatus.COMPLETED.value,
            }).eq("order_id", order_id).execute()

        logger.info("PDF regeneration completed", preview_id=preview_id, pdf_url=pdf_url)

    except Exception as e:
        logger.error("PDF regeneration failed", preview_id=preview_id, error=str(e))
        try:
            db = get_db()
            db.table("previews").update({
                "generation_phase": "pdf_failed",
            }).eq("preview_id", preview_id).execute()
        except Exception:
            pass


@router.post("/preview/{preview_id}/regenerate-pdf")
async def regenerate_pdf(preview_id: str, background_tasks: BackgroundTasks):
    """
    Regenerate PDF for a preview that has all pages but a missing/failed PDF.

    Only works for purchased previews with 10+ story pages.
    Triggers PDF generation as a background task and returns immediately.
    """
    try:
        db = get_db()
        preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_result.data:
            raise HTTPException(status_code=404, detail="Preview not found")

        preview = preview_result.data[0]

        # Verify this is a paid preview
        if preview.get("status") != "purchased":
            raise HTTPException(
                status_code=403,
                detail="Only purchased previews can have their PDF regenerated.",
            )

        # Verify we have enough pages
        story_pages = preview.get("story_pages", [])
        if len(story_pages) < 10:
            raise HTTPException(
                status_code=400,
                detail=f"Preview only has {len(story_pages)} pages. Need 10 to generate PDF.",
            )

        # Don't regenerate if already in progress
        phase = preview.get("generation_phase", "")
        if phase == "generating_pdf":
            return {
                "status": "already_generating",
                "message": "PDF is already being regenerated. Please wait.",
            }

        # Check if PDF already exists on R2
        storage = StorageService()
        pdf_path = f"final/{preview_id}/storygift_book.pdf"
        if await storage.file_exists(pdf_path) and phase == "complete":
            return {
                "status": "already_ready",
                "message": "PDF already exists and is ready for download.",
            }

        # Trigger regeneration in background
        background_tasks.add_task(_regenerate_pdf_task, preview_id)

        logger.info("PDF regeneration triggered", preview_id=preview_id)

        return {
            "status": "regenerating",
            "message": "PDF regeneration started. This usually takes 30-60 seconds.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to trigger PDF regeneration", preview_id=preview_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to start PDF regeneration. Please try again.",
        )
