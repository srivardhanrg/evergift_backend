"""
Recovery script to manually generate PDF for stuck orders.

This handles cases where:
- All pages are generated (generation_phase: "pages_complete")
- But PDF generation was interrupted (pdf_url is None)
- Worker restart killed the background task
"""

import asyncio
import structlog
from datetime import datetime, timedelta

from app.models.database import get_supabase_client
from app.models.enums import PreviewStatus, OrderStatus
from app.services.storygift_pdf_generator_v2 import get_pdf_generator_v2
from app.stories.themes import get_theme
from app.core.sanitization import sanitize_child_name

logger = structlog.get_logger()


async def recover_stuck_pdf(preview_id: str, order_id: str, order_type: str = "physical"):
    """
    Generate PDF for a preview where all pages are complete but PDF generation failed.

    Args:
        preview_id: Preview UUID
        order_id: Shopify order ID
        order_type: "digital" or "physical"
    """
    try:
        logger.info("Starting PDF recovery", preview_id=preview_id, order_id=order_id)

        # Fetch preview data
        db = get_supabase_client()
        preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

        if not preview_result.data:
            logger.error("Preview not found", preview_id=preview_id)
            return

        preview_data = preview_result.data[0]

        # Check if PDF already exists
        existing_pdf = preview_data.get("pdf_url")
        if existing_pdf:
            logger.warning(
                "PDF already exists - skipping",
                preview_id=preview_id,
                pdf_url=existing_pdf[:80]
            )
            return

        # Check if all pages are generated
        generation_phase = preview_data.get("generation_phase")
        if generation_phase != "pages_complete":
            logger.error(
                "Pages not complete - cannot generate PDF",
                preview_id=preview_id,
                generation_phase=generation_phase
            )
            return

        # Get book structure
        book_structure = preview_data.get("book_structure")
        if not book_structure:
            logger.error("No book_structure found", preview_id=preview_id)
            return

        # Build page URLs dict
        page_urls = {}
        for idx_str, page_data in book_structure.items():
            idx = int(idx_str)
            if page_data.get("url"):
                page_urls[idx] = page_data["url"]

        # Verify all 26 pages present
        missing_pages = [i for i in range(26) if i not in page_urls]
        if missing_pages:
            logger.error(
                "Missing pages - cannot generate PDF",
                preview_id=preview_id,
                missing_pages=missing_pages
            )
            return

        logger.info(
            "All pages present, starting PDF generation",
            preview_id=preview_id,
            total_pages=len(page_urls)
        )

        # Update status to generating
        db.table("previews").update({
            "generation_progress": 90,
            "current_generating_page": None
        }).eq("preview_id", preview_id).execute()

        # Get child name and theme
        child_name = sanitize_child_name(preview_data.get("child_name", "Child"))
        theme = preview_data.get("theme", "storygift_enchanted_forest")

        # Get story title
        try:
            template = get_theme(theme)
            story_title = template.get_title(child_name) if hasattr(template, 'get_title') else f"{child_name}'s Adventure"
        except Exception as e:
            logger.warning(f"Failed to get theme title: {e}")
            story_title = f"{child_name}'s Adventure"

        # Generate PDF using V2 generator
        pdf_generator_v2 = get_pdf_generator_v2()

        logger.info("Calling PDF generator", preview_id=preview_id)
        pdf_url = await pdf_generator_v2.generate_pdf(
            preview_id=preview_id,
            child_name=child_name,
            page_urls=page_urls,
            story_title=story_title,
            add_blank_back_page=(order_type == "physical")
        )

        logger.info(
            "PDF generated successfully",
            preview_id=preview_id,
            pdf_url=pdf_url[:80] if pdf_url else None
        )

        # Update database
        if order_type == "physical":
            db.table("previews").update({
                "pdf_url": pdf_url,
                "status": PreviewStatus.PURCHASED.value,
                "generation_phase": "preparing_print",
                "generation_progress": 100,
                "current_generating_page": None
            }).eq("preview_id", preview_id).execute()
        else:
            db.table("previews").update({
                "pdf_url": pdf_url,
                "status": PreviewStatus.PURCHASED.value,
                "generation_phase": "complete",
                "generation_progress": 100,
                "current_generating_page": None
            }).eq("preview_id", preview_id).execute()

        # Update order
        db.table("orders").update({
            "pdf_url": pdf_url,
            "status": OrderStatus.COMPLETED.value if order_type == "digital" else OrderStatus.GENERATING_PDF.value,
            "completed_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }).eq("order_id", order_id).execute()

        logger.info(
            "PDF recovery complete",
            preview_id=preview_id,
            order_id=order_id,
            pdf_url=pdf_url[:80] if pdf_url else None
        )

        print(f"\n✅ PDF recovery successful!")
        print(f"   Preview ID: {preview_id}")
        print(f"   Order ID: {order_id}")
        print(f"   PDF URL: {pdf_url}")

    except Exception as e:
        logger.error("PDF recovery failed", error=str(e), preview_id=preview_id)
        print(f"\n❌ PDF recovery failed: {str(e)}")
        raise


async def main():
    """Run recovery for the stuck order."""
    preview_id = "55226b47-9f8a-48fe-ab5b-e908f6e15e38"
    order_id = "6924856623380"
    order_type = "physical"  # This is a physical hardcover book order

    await recover_stuck_pdf(preview_id, order_id, order_type)


if __name__ == "__main__":
    asyncio.run(main())
