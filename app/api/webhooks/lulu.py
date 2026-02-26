"""
Lulu Print API Webhook Handler

Listens for PRINT_JOB_STATUS_CHANGED events from Lulu and updates
the print_orders table accordingly.

Lulu sends webhooks as POST with JSON body:
{
  "topic": "PRINT_JOB_STATUS_CHANGED",
  "data": {
    "id": 12345,           // Lulu print job ID
    "external_id": "...",  // Our Shopify order ID
    "status": {
      "name": "SHIPPED",
      "message": "...",
      "line_item_statuses": [{
        "messages": {
          "tracking_id": "1Z999AA10123456784",
          "tracking_urls": ["https://www.ups.com/track?tracknum=..."],
          "carrier_name": "UPS"
        }
      }]
    }
  }
}

Security: HMAC signature verification in production mode.
Tracking: Extracts tracking info from correct JSON path in Lulu response.
"""

import json
import hmac
import hashlib
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
import structlog

from app.config import get_settings
from app.models.database import get_db
from app.services.lulu_service import map_lulu_status, get_print_job

logger = structlog.get_logger()
router = APIRouter()


@router.post("/lulu")
async def handle_lulu_webhook(request: Request):
    """
    Handle incoming Lulu PRINT_JOB_STATUS_CHANGED webhooks.

    Security: Verifies HMAC signature in production to prevent fake webhooks.

    Flow:
    1. Verify webhook authenticity (HMAC in production)
    2. Parse webhook payload
    3. Find matching print_order by lulu_print_job_id (with fallback)
    4. Update status in DB
    5. If SHIPPED: extract tracking from correct path + send email
    6. Return 200 immediately
    """
    settings = get_settings()

    try:
        # 1. Read raw body for HMAC verification
        body = await request.body()
        if not body:
            return {"success": True, "message": "Empty webhook body"}

        # 2. SECURITY: Verify HMAC signature in production
        # Lulu signs webhooks with your client secret (no separate webhook secret)
        webhook_secret = settings.lulu_webhook_secret or settings.lulu_client_secret
        if settings.app_env == "production" and webhook_secret:
            # Lulu uses the header "Lulu-HMAC-SHA256" (NOT X-Lulu-Signature)
            signature = request.headers.get("Lulu-HMAC-SHA256", "")
            if not signature:
                logger.warning("Lulu webhook missing Lulu-HMAC-SHA256 header")
                raise HTTPException(status_code=401, detail="Missing webhook signature")

            # Compute expected HMAC-SHA256 using raw body
            expected_sig = hmac.new(
                webhook_secret.encode("utf-8"),
                body,
                hashlib.sha256
            ).hexdigest()

            # Constant-time comparison to prevent timing attacks
            if not hmac.compare_digest(signature.lower(), expected_sig.lower()):
                logger.error(
                    "Lulu webhook signature verification failed",
                    expected=expected_sig[:16] + "...",
                    received=signature[:16] + "..."
                )
                raise HTTPException(status_code=403, detail="Invalid webhook signature")

            logger.info("Lulu webhook signature verified successfully")

        # 3. Parse payload
        payload = json.loads(body.decode("utf-8"))
        topic = payload.get("topic", "")
        data = payload.get("data", {})

        logger.info("Lulu webhook received", topic=topic, lulu_job_id=data.get("id"))

        if topic != "PRINT_JOB_STATUS_CHANGED":
            # Acknowledge but ignore other topics
            return {"success": True, "message": f"Topic {topic} ignored"}

        lulu_job_id = str(data.get("id", ""))
        external_id = str(data.get("external_id", ""))  # Our Shopify order_id

        if not lulu_job_id:
            logger.warning("Lulu webhook missing job ID")
            return {"success": True, "message": "No job ID"}

        status_obj = data.get("status", {})
        lulu_status_name = status_obj.get("name", "")
        mapped_status = map_lulu_status(lulu_status_name)

        db = get_db()

        # 4. Find print_order (with fallback for race conditions)
        result = db.table("print_orders").select("*").eq(
            "lulu_print_job_id", lulu_job_id
        ).execute()

        # EDGE CASE: Webhook arrived before lulu_print_job_id was saved
        # This can happen if Lulu sends CREATED webhook very quickly
        if not result.data and external_id:
            logger.info(
                "Trying fallback lookup by order_id",
                order_id=external_id,
                lulu_job_id=lulu_job_id
            )
            result = db.table("print_orders").select("*").eq(
                "order_id", external_id
            ).execute()

            # If found via fallback, update with lulu_print_job_id
            if result.data:
                db.table("print_orders").update({
                    "lulu_print_job_id": lulu_job_id
                }).eq("order_id", external_id).execute()
                logger.info(
                    "Updated print_order with lulu_print_job_id via fallback",
                    order_id=external_id,
                    lulu_job_id=lulu_job_id
                )

        if not result.data:
            logger.warning(
                "No print_order found for Lulu job",
                lulu_job_id=lulu_job_id,
                external_id=external_id
            )
            return {"success": True, "message": "Print order not found"}

        record = result.data[0]
        print_order_id = record.get("print_order_id")
        preview_id = record.get("preview_id")
        order_id = record.get("order_id")

        # 5. Build update payload
        update_data: dict = {
            "lulu_status": mapped_status,
            "lulu_status_raw": lulu_status_name,
            "lulu_api_response": data,
        }

        # 6. FIX: Extract tracking from CORRECT path when SHIPPED
        # Lulu puts tracking info in status.line_item_statuses[0].messages
        # NOT in line_items[0].tracking_id (that was the bug!)
        tracking_number = None
        tracking_url = None
        carrier_name = None
        estimated_delivery = None

        if lulu_status_name.upper() == "SHIPPED":
            update_data["shipped_at"] = datetime.utcnow().isoformat()

            try:
                # Fetch full job details to get tracking info
                job_details = await get_print_job(lulu_job_id)

                # CORRECT PATH: status.line_item_statuses[0].messages
                job_status = job_details.get("status", {})
                line_item_statuses = job_status.get("line_item_statuses", [])

                if not line_item_statuses:
                    logger.warning(
                        "SHIPPED webhook has no line_item_statuses",
                        lulu_job_id=lulu_job_id
                    )
                else:
                    messages = line_item_statuses[0].get("messages", {})
                    tracking_number = messages.get("tracking_id", "")
                    tracking_urls = messages.get("tracking_urls", [])
                    carrier_name = messages.get("carrier_name", "")

                    if not tracking_number:
                        logger.warning(
                            "SHIPPED webhook missing tracking_id in messages",
                            lulu_job_id=lulu_job_id,
                            messages=messages
                        )
                    else:
                        # Save tracking data
                        update_data["tracking_number"] = tracking_number

                        if carrier_name:
                            update_data["carrier"] = carrier_name

                        if tracking_urls and len(tracking_urls) > 0:
                            # Use first URL (Lulu puts official carrier URL first)
                            tracking_url = tracking_urls[0]
                            update_data["tracking_url"] = tracking_url

                        logger.info(
                            "Tracking info extracted successfully",
                            tracking_number=tracking_number,
                            carrier=carrier_name,
                            tracking_url=tracking_url[:50] + "..." if tracking_url else None
                        )

                # Get estimated delivery date
                estimated = job_details.get("estimated_shipping_dates", [])
                if estimated:
                    estimated_delivery = estimated[0].get("date")
                    update_data["estimated_delivery"] = estimated_delivery

            except Exception as e:
                logger.error(
                    "Failed to fetch tracking info from Lulu API",
                    error=str(e),
                    lulu_job_id=lulu_job_id
                )
                # Continue - update status even if tracking fetch fails

        if lulu_status_name.upper() == "DELIVERED":
            update_data["delivered_at"] = datetime.utcnow().isoformat()

        # 7. Update database
        try:
            db.table("print_orders").update(update_data).eq(
                "print_order_id", print_order_id
            ).execute()

            logger.info(
                "Print order status updated in database",
                print_order_id=print_order_id,
                lulu_status=lulu_status_name,
                mapped_status=mapped_status,
                has_tracking=bool(tracking_number)
            )
        except Exception as db_error:
            logger.error("Database update failed", error=str(db_error))
            # Return 500 for DB connection issues so Lulu retries
            if "connection" in str(db_error).lower() or "timeout" in str(db_error).lower():
                raise HTTPException(status_code=500, detail="Database unavailable")
            # Return 200 for logic errors to prevent infinite retry loop
            return {"success": False, "error": str(db_error)}

        # 8. Send shipping notification email to customer
        if lulu_status_name.upper() == "SHIPPED" and tracking_number:
            await _send_shipping_email(
                db=db,
                preview_id=preview_id,
                order_id=order_id,
                tracking_number=tracking_number,
                tracking_url=tracking_url,
                carrier=carrier_name,
                estimated_delivery=estimated_delivery
            )

        return {"success": True, "message": "Status updated"}

    except HTTPException:
        # Re-raise HTTP exceptions (401, 403, 500)
        raise
    except Exception as e:
        logger.error("Lulu webhook processing failed", error=str(e))
        # Return 200 to prevent Lulu retry loop on logic errors
        return {"success": False, "error": str(e)}


async def _send_shipping_email(
    db,
    preview_id: str,
    order_id: str,
    tracking_number: str,
    tracking_url: str | None,
    carrier: str | None,
    estimated_delivery: str | None
) -> None:
    """
    Send shipping notification email to customer.

    This is a best-effort operation - we log errors but don't fail the webhook.
    """
    try:
        from app.services.email_service import get_email_service

        # Get customer info from preview
        preview_resp = db.table("previews").select(
            "customer_email,child_name"
        ).eq("preview_id", preview_id).execute()

        if not preview_resp.data:
            logger.warning(
                "Cannot send shipping email - preview not found",
                preview_id=preview_id
            )
            return

        preview = preview_resp.data[0]
        customer_email = preview.get("customer_email")
        child_name = preview.get("child_name", "Your child")

        if not customer_email:
            logger.warning(
                "Cannot send shipping email - no customer email",
                preview_id=preview_id
            )
            return

        # Fallback tracking URL if not provided by Lulu
        final_tracking_url = tracking_url or f"https://parcelsapp.com/en/tracking/{tracking_number}"

        email_service = get_email_service()
        await email_service.send_book_shipped_email(
            to_email=customer_email,
            child_name=child_name,
            tracking_number=tracking_number,
            tracking_url=final_tracking_url,
            carrier=carrier or "Carrier",
            estimated_delivery=estimated_delivery
        )

        logger.info(
            "Shipping notification email sent successfully",
            customer_email=customer_email[:3] + "***",  # Partially mask email for logs
            tracking_number=tracking_number
        )

    except Exception as email_error:
        # Don't fail webhook processing if email fails
        # Log as error so it can be manually followed up
        logger.error(
            "CRITICAL: Shipping notification email failed - manual resend may be needed",
            preview_id=preview_id,
            order_id=order_id,
            tracking_number=tracking_number,
            error=str(email_error)
        )
