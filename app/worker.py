"""
ARQ worker configuration for background job processing.

This worker handles async generation tasks that were previously run with BackgroundTasks.
Workers are deployed as separate Render services and connect to the same Redis instance.

Run with: python -m arq app.worker.WorkerSettings
"""

import asyncio
from typing import Any
import structlog
from arq import cron
from arq.connections import RedisSettings

from app.config import get_settings
from app.models.database import get_db
from app.models.enums import JobStatus, PreviewStatus
from app.background.tasks import (
    generate_full_preview,
    generate_remaining_pages_and_pdf
)

logger = structlog.get_logger()


# ============================================================================
# ARQ Task Wrapper Functions
# ============================================================================
# These functions wrap the existing generation logic and handle failures.
# They are enqueued from API endpoints and executed by ARQ workers.
# ============================================================================

async def preview_generation_task(
    ctx: dict,
    job_id: str,
    preview_id: str,
    photo_urls: list[str],
    child_name: str,
    child_age: int,
    child_gender: str,
    theme: str,
    style: str = "photorealistic"
) -> dict[str, Any]:
    """
    ARQ task wrapper for preview generation.

    Calls the existing generate_full_preview function and handles failures.
    """
    try:
        logger.info(
            "ARQ worker: Starting preview generation",
            job_id=job_id,
            preview_id=preview_id,
            theme=theme,
            style=style
        )

        # Call existing generation function
        await generate_full_preview(
            job_id=job_id,
            preview_id=preview_id,
            photo_urls=photo_urls,
            child_name=child_name,
            child_age=child_age,
            child_gender=child_gender,
            theme=theme,
            style=style
        )

        logger.info(
            "ARQ worker: Preview generation completed",
            job_id=job_id,
            preview_id=preview_id
        )

        return {"success": True, "preview_id": preview_id}

    except Exception as e:
        error_msg = f"Preview generation failed: {str(e)}"
        logger.error(
            "ARQ worker: Preview generation failed",
            job_id=job_id,
            preview_id=preview_id,
            error=str(e),
            error_type=type(e).__name__
        )

        # Check if this is the final attempt
        current_attempt = ctx.get("job_try", 1)
        max_tries = 3  # Should match WorkerSettings.max_tries
        is_final_attempt = current_attempt >= max_tries

        # Update job and preview status in database
        try:
            db = get_db()

            # Only set FAILED on final attempt, otherwise set to indicate retry
            if is_final_attempt:
                db.table("generation_jobs").update({
                    "status": JobStatus.FAILED.value,
                    "error": error_msg
                }).eq("job_id", job_id).execute()

                db.table("previews").update({
                    "status": PreviewStatus.FAILED.value
                }).eq("preview_id", preview_id).execute()

                logger.error(
                    "Preview generation failed after all retries",
                    job_id=job_id,
                    preview_id=preview_id,
                    attempts=current_attempt
                )
            else:
                # Not final attempt - will retry
                logger.warning(
                    "Preview generation failed, will retry",
                    job_id=job_id,
                    preview_id=preview_id,
                    attempt=current_attempt,
                    max_tries=max_tries
                )

        except Exception as db_error:
            logger.error(
                "Failed to update status in database",
                job_id=job_id,
                preview_id=preview_id,
                error=str(db_error)
            )

        # Re-raise to trigger ARQ retry
        raise


async def post_payment_generation_task(
    ctx: dict,
    order_id: str,
    preview_id: str,
    child_name: str,
    order_type: str = "digital"
) -> dict[str, Any]:
    """
    ARQ task wrapper for post-payment book generation.

    Calls the existing generate_remaining_pages_and_pdf function and handles failures.
    """
    try:
        logger.info(
            "ARQ worker: Starting post-payment generation",
            order_id=order_id,
            preview_id=preview_id,
            order_type=order_type
        )

        # Call existing generation function
        pdf_url = await generate_remaining_pages_and_pdf(
            order_id=order_id,
            preview_id=preview_id,
            child_name=child_name,
            order_type=order_type
        )

        logger.info(
            "ARQ worker: Post-payment generation completed",
            order_id=order_id,
            preview_id=preview_id,
            pdf_url=pdf_url[:80] if pdf_url else None
        )

        return {"success": True, "order_id": order_id, "pdf_url": pdf_url}

    except Exception as e:
        error_msg = f"Post-payment generation failed: {str(e)}"
        logger.error(
            "ARQ worker: Post-payment generation failed",
            order_id=order_id,
            preview_id=preview_id,
            error=str(e),
            error_type=type(e).__name__
        )

        # Check if this is the final attempt
        current_attempt = ctx.get("job_try", 1)
        max_tries = 3  # Should match WorkerSettings.max_tries
        is_final_attempt = current_attempt >= max_tries

        # Update order status in database
        try:
            from app.models.enums import OrderStatus
            db = get_db()

            # Only set FAILED on final attempt, otherwise set to indicate retry
            if is_final_attempt:
                db.table("orders").update({
                    "status": OrderStatus.FAILED.value,
                    "error_message": error_msg
                }).eq("order_id", order_id).execute()

                db.table("previews").update({
                    "generation_phase": "failed",
                    "status": PreviewStatus.FAILED.value
                }).eq("preview_id", preview_id).execute()

                logger.error(
                    "Post-payment generation failed after all retries",
                    order_id=order_id,
                    preview_id=preview_id,
                    attempts=current_attempt
                )
            else:
                # Not final attempt - will retry
                logger.warning(
                    "Post-payment generation failed, will retry",
                    order_id=order_id,
                    preview_id=preview_id,
                    attempt=current_attempt,
                    max_tries=max_tries
                )

        except Exception as db_error:
            logger.error(
                "Failed to update status in database",
                order_id=order_id,
                preview_id=preview_id,
                error=str(db_error)
            )

        # Re-raise to trigger ARQ retry
        raise


# ============================================================================
# ARQ Worker Configuration
# ============================================================================

async def startup(ctx: dict) -> None:
    """Called when worker starts up."""
    logger.info("ARQ worker starting up")
    settings = get_settings()
    logger.info(
        "ARQ worker initialized",
        environment=settings.app_env,
        redis_url=settings.redis_url[:20] + "..." if settings.redis_url else None
    )


async def shutdown(ctx: dict) -> None:
    """Called when worker shuts down."""
    logger.info("ARQ worker shutting down")


async def health_check(ctx: dict) -> None:
    """Periodic health check for worker monitoring."""
    logger.info("ARQ worker health check")


class WorkerSettings:
    """
    ARQ worker settings.

    Configuration:
    - max_jobs=3: Maximum concurrent jobs (matches fal.ai semaphore)
    - job_timeout=600: 10 minutes timeout (enough for full generation)
    - max_tries=3: Retry failed jobs up to 3 times
    - retry_delay=10: Wait 10 seconds between retries
    """

    functions = [
        preview_generation_task,
        post_payment_generation_task
    ]

    on_startup = startup
    on_shutdown = shutdown

    # Redis connection
    settings = get_settings()
    redis_settings = RedisSettings.from_dsn(settings.redis_url)

    # Job execution settings
    max_jobs = 3  # Max concurrent jobs (matches fal.ai semaphore limit)
    job_timeout = 600  # 10 minutes (enough for 5-page preview or full book)
    max_tries = 3  # Retry failed jobs 3 times
    retry_delay = 10  # Wait 10 seconds between retries

    # Worker polling settings
    poll_delay = 0.5  # Check for new jobs every 0.5 seconds

    # Health check cron (runs every 15 minutes)
    cron_jobs = [
        cron(func=health_check, minute={0, 15, 30, 45})
    ]
