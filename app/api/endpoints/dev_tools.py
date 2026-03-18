"""
Development Tools API - For testing V2 26-page generation flow.

SECURITY: Only accessible when TESTING_MODE_ENABLED=true
Provides endpoints to test post-payment generation without creating real orders.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
import structlog
from typing import Optional
from pydantic import BaseModel

from app.models.database import get_db
from app.models.enums import PreviewStatus
from app.background.storygift_tasks import generate_remaining_pages_and_pdf

logger = structlog.get_logger()
router = APIRouter(prefix="/dev")


class TestPostPaymentRequest(BaseModel):
    """Request model for testing post-payment generation."""
    preview_id: str
    order_type: str = "digital"  # "digital" or "physical"


class TestPostPaymentResponse(BaseModel):
    """Response model for test post-payment endpoint."""
    success: bool
    message: str
    preview_id: str
    generation_started: bool
    order_type: str


@router.post("/test-post-payment", response_model=TestPostPaymentResponse)
async def test_post_payment_generation(
    request: TestPostPaymentRequest,
    background_tasks: BackgroundTasks
):
    """
    Test endpoint to trigger post-payment generation (pages 13-25 + PDF).

    This bypasses Shopify order creation and directly tests:
    - Locked AI page generation (indices 14, 16, 18, 20, 22)
    - Locked filler page processing (indices 13-25)
    - V2 26-page PDF generation
    - Email delivery (if configured)

    Prerequisites:
    - Preview must exist and have status "active"
    - Preview must have completed preview generation (pages 0-12)
    - Preview must have story_texts populated
    - Preview must have book_structure with at least preview pages

    Args:
        request: Contains preview_id and order_type

    Returns:
        Success response with generation status

    Raises:
        HTTPException: If preview not found or not ready for post-payment
    """
    try:
        db = get_db()
        preview_id = request.preview_id
        order_type = request.order_type

        # Fetch preview
        preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Preview {preview_id} not found"
            )

        preview = preview_result.data[0]

        # Validate preview is ready for post-payment generation
        status = preview.get("status")
        if status != PreviewStatus.ACTIVE.value:
            raise HTTPException(
                status_code=400,
                detail=f"Preview status is '{status}', must be 'active' to test post-payment"
            )

        generation_phase = preview.get("generation_phase", "")
        if generation_phase != "complete":
            raise HTTPException(
                status_code=400,
                detail=f"Preview generation phase is '{generation_phase}', must be 'complete'. Preview generation not finished yet."
            )

        # Check critical data exists
        book_structure = preview.get("book_structure")
        if not book_structure or not isinstance(book_structure, dict):
            raise HTTPException(
                status_code=400,
                detail="Preview has no book_structure. Preview generation may have failed."
            )

        story_texts = preview.get("story_texts")
        if not story_texts or len(story_texts) < 10:
            raise HTTPException(
                status_code=400,
                detail=f"Preview has incomplete story_texts (found {len(story_texts or {})}, need 10)"
            )

        # Get child name for generation
        child_name = preview.get("child_name", "Child")

        # Create a test order ID for tracking
        test_order_id = f"TEST_{preview_id[:8]}"

        # Trigger post-payment generation in background
        background_tasks.add_task(
            generate_remaining_pages_and_pdf,
            order_id=test_order_id,
            preview_id=preview_id,
            child_name=child_name,
            max_retries=3,
            order_type=order_type
        )

        logger.info(
            "Test post-payment generation triggered",
            preview_id=preview_id,
            test_order_id=test_order_id,
            order_type=order_type,
            child_name=child_name
        )

        return TestPostPaymentResponse(
            success=True,
            message=f"Post-payment generation started for preview {preview_id}. This will take 3-5 minutes. Monitor logs for progress.",
            preview_id=preview_id,
            generation_started=True,
            order_type=order_type
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to trigger test post-payment generation",
            preview_id=request.preview_id,
            error=str(e),
            error_type=type(e).__name__
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/preview/{preview_id}/status")
async def get_preview_status(preview_id: str):
    """
    Get detailed status of a preview for debugging.

    Returns comprehensive preview data including:
    - Generation status and phase
    - Page counts and structure
    - Story texts availability
    - PDF status

    Args:
        preview_id: Preview UUID

    Returns:
        Detailed preview status information
    """
    try:
        db = get_db()

        preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Preview {preview_id} not found"
            )

        preview = preview_result.data[0]
        book_structure = preview.get("book_structure") or {}
        story_texts = preview.get("story_texts") or {}
        filler_pages_processed = preview.get("filler_pages_processed") or {}

        # Count pages by type
        generated_pages = [int(k) for k, v in book_structure.items() if v.get("is_generated")]
        filler_pages = [int(k) for k, v in book_structure.items() if v.get("type") == "filler"]

        return {
            "success": True,
            "data": {
                "preview_id": preview_id,
                "status": preview.get("status"),
                "generation_phase": preview.get("generation_phase"),
                "child_name": preview.get("child_name"),
                "theme": preview.get("theme"),
                "total_pages": preview.get("total_pages", 0),
                "preview_page_count": preview.get("preview_page_count", 0),
                "book_structure": {
                    "total_indices": len(book_structure),
                    "generated_pages_count": len(generated_pages),
                    "filler_pages_count": len(filler_pages),
                    "generated_pages": sorted(generated_pages),
                    "filler_pages": sorted(filler_pages),
                },
                "story_texts": {
                    "count": len(story_texts),
                    "indices": sorted([int(k) for k in story_texts.keys()]),
                    "all_10_present": len(story_texts) == 10
                },
                "filler_processed": {
                    "count": len(filler_pages_processed),
                    "indices": sorted([int(k) for k in filler_pages_processed.keys()])
                },
                "pdf_url": preview.get("pdf_url"),
                "cover_url": preview.get("cover_url"),
                "created_at": preview.get("created_at"),
                "updated_at": preview.get("updated_at")
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to get preview status",
            preview_id=preview_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve preview status: {str(e)}"
        )
