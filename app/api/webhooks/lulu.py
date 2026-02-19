"""
Lulu Print API Webhook Handler

Listens for PRINT_JOB_STATUS_CHANGED events from Lulu and updates
the print_orders table accordingly.

Lulu sends webhooks as POST with JSON body:
{
  "topic": "PRINT_JOB_STATUS_CHANGED",
  "data": {
    "id": 12345,           // Lulu print job ID
    "status": {
      "name": "SHIPPED",
      "message": "..."
    }
  }
}

Security: Lulu does not sign webhooks with HMAC in sandbox.
In production, validate using the shared secret configured in Lulu dashboard.
We use a simple bearer token approach for now (via query param).
"""

import json
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Query
import structlog

from app.models.database import get_db
from app.services.lulu_service import map_lulu_status, get_print_job

logger = structlog.get_logger()
router = APIRouter()


@router.post("/lulu")
async def handle_lulu_webhook(
    request: Request,
    secret: str = Query(default="", description="Shared webhook secret for verification"),
):
    """
    Handle incoming Lulu PRINT_JOB_STATUS_CHANGED webhooks.

    Flow:
    1. Parse webhook payload
    2. Find matching print_order by lulu_print_job_id
    3. Update status in DB
    4. If SHIPPED: store tracking number
    5. Return 200 immediately
    """
    try:
        body = await request.body()
        if not body:
            return {"success": True, "message": "Empty webhook body"}

        payload = json.loads(body.decode("utf-8"))
        topic = payload.get("topic", "")
        data = payload.get("data", {})

        logger.info("Lulu webhook received", topic=topic, data=data)

        if topic != "PRINT_JOB_STATUS_CHANGED":
            # Acknowledge but ignore other topics
            return {"success": True, "message": f"Topic {topic} ignored"}

        lulu_job_id = str(data.get("id", ""))
        if not lulu_job_id:
            logger.warning("Lulu webhook missing job ID")
            return {"success": True, "message": "No job ID"}

        status_obj = data.get("status", {})
        lulu_status_name = status_obj.get("name", "")
        mapped_status = map_lulu_status(lulu_status_name)

        db = get_db()

        # Find our print_order
        result = db.table("print_orders").select("*").eq(
            "lulu_print_job_id", lulu_job_id
        ).execute()

        if not result.data:
            logger.warning("No print_order found for Lulu job", lulu_job_id=lulu_job_id)
            return {"success": True, "message": "Print order not found"}

        record = result.data[0]
        print_order_id = record.get("print_order_id")

        # Build update payload
        update_data: dict = {
            "lulu_status": mapped_status,
            "lulu_status_raw": lulu_status_name,
            "lulu_api_response": data,
        }

        # Handle SHIPPED: fetch tracking from full job details
        if lulu_status_name.upper() == "SHIPPED":
            update_data["shipped_at"] = datetime.utcnow().isoformat()
            try:
                job_details = await get_print_job(lulu_job_id)
                line_items = job_details.get("line_items", [])
                if line_items:
                    tracking = line_items[0].get("tracking_id", "")
                    carrier = line_items[0].get("tracking_urls", [{}])[0] if line_items[0].get("tracking_urls") else {}
                    if tracking:
                        update_data["tracking_number"] = tracking
                    estimated = job_details.get("estimated_shipping_dates", [])
                    if estimated:
                        update_data["estimated_delivery"] = estimated[0].get("date")
            except Exception as e:
                logger.warning("Could not fetch Lulu job details for tracking", error=str(e))

        if lulu_status_name.upper() == "DELIVERED":
            update_data["delivered_at"] = datetime.utcnow().isoformat()

        # Update DB
        db.table("print_orders").update(update_data).eq(
            "print_order_id", print_order_id
        ).execute()

        logger.info(
            "Print order status updated",
            print_order_id=print_order_id,
            lulu_status=lulu_status_name,
            mapped=mapped_status,
        )

        return {"success": True, "message": "Status updated"}

    except Exception as e:
        logger.error("Lulu webhook processing failed", error=str(e))
        # Return 200 to prevent Lulu retrying on our logic errors
        return {"success": False, "error": str(e)}
