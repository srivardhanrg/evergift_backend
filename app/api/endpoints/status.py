"""
Job status polling endpoint.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import structlog

from app.models.schemas import JobStatusResponse
from app.models.database import get_db
from app.models.enums import JobStatus, GenerationPhase

logger = structlog.get_logger()
router = APIRouter()


async def _get_job_status_internal(job_id: str):
    """Internal function to get job status (shared by both endpoints)."""
    logger.debug("Getting job status", job_id=job_id)

    db = get_db()

    # Get job record
    job_response = db.table("generation_jobs").select("*").eq("job_id", job_id).execute()

    if not job_response.data:
        raise HTTPException(status_code=404, detail="Job not found")

    job = job_response.data[0]

    # Get current step or default message
    current_step = None
    if job["status"] == JobStatus.QUEUED.value:
        current_step = "Queued for processing..."
    elif job["status"] == JobStatus.PROCESSING.value:
        current_step = job.get("current_step", "Generating images...")
    elif job["status"] == JobStatus.COMPLETED.value:
        current_step = "Generation completed!"
    elif job["status"] == JobStatus.FAILED.value:
        current_step = "Generation failed"

    # Build response based on status
    response_data = {
        "job_id": job_id,
        "status": JobStatus(job["status"]),
        "progress": job["progress"],
        "current_step": current_step,
        "preview_id": job["reference_id"],  # Always include preview_id
        "can_retry": False
    }

    # Add redirect for completed jobs
    if job["status"] == JobStatus.COMPLETED.value:
        response_data.update({
            "redirect_url": f"/preview/{job['reference_id']}"
        })

    # Add error info for failed jobs
    if job["status"] == JobStatus.FAILED.value:
        response_data.update({
            "error": job.get("error_message", "Generation failed"),
            "can_retry": job["attempts"] < job["max_attempts"]
        })

    return JobStatusResponse(**response_data)


@router.get("/preview-status/{job_id}", response_model=JobStatusResponse)
async def get_preview_status(job_id: str):
    """
    Get status of a preview generation job.

    Used for polling by frontend to track generation progress.
    Returns progress percentage and current step.
    """
    try:
        return await _get_job_status_internal(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get job status", job_id=job_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve job status. Please try again."
        )


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Alias for get_preview_status for frontend compatibility.
    Frontend expects /status/{job_id} endpoint.
    """
    try:
        return await _get_job_status_internal(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get job status", job_id=job_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve job status. Please try again."
        )


# ---------------------------------------------------------------------------
# Full Status Response Model
# ---------------------------------------------------------------------------

class PrintOrderStatus(BaseModel):
    """Print order status for physical orders."""
    print_order_id: Optional[str] = None
    lulu_status: Optional[str] = None
    lulu_print_job_id: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    carrier: Optional[str] = None
    estimated_delivery: Optional[str] = None
    shipped_at: Optional[str] = None
    delivered_at: Optional[str] = None


class FullStatusResponse(BaseModel):
    """
    Comprehensive status response for preview/order lifecycle.
    Used by frontend to determine what UI state to show.
    """
    preview_id: str
    generation_phase: str
    order_type: Optional[str] = None  # "digital" or "physical"

    # Preview info
    preview_status: str
    child_name: Optional[str] = None
    theme: Optional[str] = None
    pdf_url: Optional[str] = None

    # Order info (if exists)
    order_id: Optional[str] = None
    order_status: Optional[str] = None

    # Print order info (for physical orders)
    print_order: Optional[PrintOrderStatus] = None

    # UI helper fields
    is_generating: bool = False
    is_complete: bool = False
    is_failed: bool = False
    can_retry: bool = False
    error_message: Optional[str] = None

    # User-friendly status message
    status_message: str


# Phase to status message mapping
PHASE_MESSAGES = {
    GenerationPhase.PREVIEW.value: "Preview ready",
    GenerationPhase.GENERATING_FULL.value: "Generating your personalized storybook...",
    GenerationPhase.PAGES_COMPLETE.value: "Creating your PDF...",
    GenerationPhase.COMPLETE.value: "Your storybook is ready!",
    GenerationPhase.PREPARING_PRINT.value: "Preparing your book for printing...",
    GenerationPhase.SUBMITTING_PRINT.value: "Submitting to print facility...",
    GenerationPhase.PRINT_SUBMITTED.value: "Your book is being printed!",
    GenerationPhase.PDF_FAILED.value: "PDF generation failed",
    GenerationPhase.PRINT_FAILED.value: "Print submission failed",
    GenerationPhase.FAILED.value: "Generation failed",
}


@router.get("/full-status/{preview_id}", response_model=FullStatusResponse)
async def get_full_status(preview_id: str):
    """
    Get comprehensive status for a preview including order and print status.

    This is the primary endpoint for frontend polling after checkout.
    Returns all information needed to display the appropriate UI state:
    - Generation progress for remaining pages
    - PDF creation status
    - Print order submission status (for physical orders)
    - Tracking info when available
    """
    logger.debug("Getting full status", preview_id=preview_id)

    db = get_db()

    try:
        # Get preview record
        preview_resp = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_resp.data:
            raise HTTPException(status_code=404, detail="Preview not found")

        preview = preview_resp.data[0]
        generation_phase = preview.get("generation_phase", GenerationPhase.PREVIEW.value)

        # Get order record if exists
        order = None
        order_resp = db.table("orders").select("*").eq("preview_id", preview_id).execute()
        if order_resp.data:
            order = order_resp.data[0]

        # Get print order if exists (for physical orders)
        print_order_data = None
        if order:
            print_resp = db.table("print_orders").select(
                "print_order_id,lulu_status,lulu_print_job_id,tracking_number,"
                "tracking_url,carrier,estimated_delivery,shipped_at,delivered_at"
            ).eq("order_id", order.get("order_id")).execute()

            if print_resp.data:
                po = print_resp.data[0]
                print_order_data = PrintOrderStatus(
                    print_order_id=po.get("print_order_id"),
                    lulu_status=po.get("lulu_status"),
                    lulu_print_job_id=po.get("lulu_print_job_id"),
                    tracking_number=po.get("tracking_number"),
                    tracking_url=po.get("tracking_url"),
                    carrier=po.get("carrier"),
                    estimated_delivery=po.get("estimated_delivery"),
                    shipped_at=po.get("shipped_at"),
                    delivered_at=po.get("delivered_at"),
                )

        # Determine order type
        order_type = None
        if order:
            order_type = order.get("order_type", "digital")

        # Determine UI state flags
        generating_phases = {
            GenerationPhase.GENERATING_FULL.value,
            GenerationPhase.PAGES_COMPLETE.value,
            GenerationPhase.PREPARING_PRINT.value,
            GenerationPhase.SUBMITTING_PRINT.value,
        }
        complete_phases = {
            GenerationPhase.COMPLETE.value,
            GenerationPhase.PRINT_SUBMITTED.value,
        }
        failed_phases = {
            GenerationPhase.PDF_FAILED.value,
            GenerationPhase.PRINT_FAILED.value,
            GenerationPhase.FAILED.value,
        }

        is_generating = generation_phase in generating_phases
        is_complete = generation_phase in complete_phases
        is_failed = generation_phase in failed_phases

        # For print_submitted, also check lulu_status for shipped/delivered
        if print_order_data and print_order_data.lulu_status in ("shipped", "delivered"):
            is_complete = True

        # Can retry if failed and has an order
        can_retry = is_failed and order is not None

        # Get status message
        status_message = PHASE_MESSAGES.get(generation_phase, "Processing...")

        # Override message for shipped/delivered
        if print_order_data:
            if print_order_data.lulu_status == "shipped":
                status_message = "Your book has shipped!"
            elif print_order_data.lulu_status == "delivered":
                status_message = "Your book has been delivered!"
            elif print_order_data.lulu_status == "in_production":
                status_message = "Your book is being printed!"

        return FullStatusResponse(
            preview_id=preview_id,
            generation_phase=generation_phase,
            order_type=order_type,
            preview_status=preview.get("status", ""),
            child_name=preview.get("child_name"),
            theme=preview.get("theme"),
            pdf_url=preview.get("pdf_url"),
            order_id=order.get("order_id") if order else None,
            order_status=order.get("status") if order else None,
            print_order=print_order_data,
            is_generating=is_generating,
            is_complete=is_complete,
            is_failed=is_failed,
            can_retry=can_retry,
            error_message=order.get("error_message") if order and is_failed else None,
            status_message=status_message,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get full status", preview_id=preview_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve status. Please try again."
        )