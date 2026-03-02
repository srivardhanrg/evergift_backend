"""
Lulu Print Background Tasks

Called after StoryGift PDF generation completes (i.e. after order is paid).

Flow:
1. Generate Lulu-spec interior PDF (8.75x8.75" with bleed, 12 pages)
2. Generate Lulu-spec cover wrap PDF
3. Create print_orders record (status: pending)
4. Submit print job to Lulu API
5. Update print_orders with Lulu job ID + status
6. (Optional) Send shipping confirmation email when Lulu webhook arrives
"""

import json
from datetime import datetime
import structlog

from app.config import get_settings
from app.models.database import get_db
from app.models.enums import OrderStatus, GenerationPhase
from app.services.lulu_service import create_print_job, map_lulu_status
from app.services.lulu_pdf_generator import generate_interior_pdf, generate_cover_pdf

logger = structlog.get_logger()


def _build_shipping_address(order: dict, preview: dict) -> dict:
    """
    Convert Shopify shipping address format to Lulu's format.

    Shopify fields (from webhook):
        first_name, last_name, address1, address2, city,
        province, province_code, country, country_code, zip, phone, email
    Lulu fields (required):
        name, street1, city, country_code, postcode, phone_number, email
    """
    shopify_addr = order.get("shipping_address") or {}

    first = shopify_addr.get("first_name", "")
    last = shopify_addr.get("last_name", "")
    name = f"{first} {last}".strip() or order.get("customer_name", "Customer")

    # Email can come from: shipping_address, order email, or preview customer_email
    email = (
        shopify_addr.get("email")
        or order.get("email")
        or order.get("customer_email")
        or preview.get("customer_email")
        or ""
    )

    return {
        "name": name,
        "street1": shopify_addr.get("address1", ""),
        "street2": shopify_addr.get("address2", ""),
        "city": shopify_addr.get("city", ""),
        "state_code": shopify_addr.get("province_code") or shopify_addr.get("province", ""),
        "country_code": shopify_addr.get("country_code") or shopify_addr.get("country", "IN"),
        "postcode": shopify_addr.get("zip", ""),
        "phone_number": shopify_addr.get("phone", ""),
        "email": email,  # Required by Lulu API
    }


def _collect_pages(preview: dict) -> list:
    """
    Collect all story pages from a preview record.
    Combines cover (page 0) + hires_images (pages 1-10) + story_pages (text).
    """
    pages = []

    # hires_images: [{page: int, url: string}, ...]
    hires = preview.get("hires_images") or []
    if isinstance(hires, str):
        try:
            hires = json.loads(hires)
        except Exception:
            hires = []

    # story_pages: [{page: int, text: string}, ...]
    story = preview.get("story_pages") or []
    if isinstance(story, str):
        try:
            story = json.loads(story)
        except Exception:
            story = []

    text_map = {p.get("page", p.get("page_number", 0)): p.get("text", p.get("story_text", "")) for p in story}

    for item in hires:
        page_num = item.get("page", item.get("page_number", 0))
        pages.append({
            "page_number": page_num,
            "image_url": item.get("url", item.get("image_url", "")),
            "story_text": text_map.get(page_num, ""),
        })

    # Also check preview_images for cover (page 0) if not in hires
    page_nums_in_hires = {p["page_number"] for p in pages}
    preview_imgs = preview.get("preview_images") or []
    if isinstance(preview_imgs, str):
        try:
            preview_imgs = json.loads(preview_imgs)
        except Exception:
            preview_imgs = []

    for item in preview_imgs:
        page_num = item.get("page", item.get("page_number", 0))
        if page_num not in page_nums_in_hires:
            pages.append({
                "page_number": page_num,
                "image_url": item.get("url", item.get("image_url", "")),
                "story_text": text_map.get(page_num, ""),
            })

    return sorted(pages, key=lambda p: p["page_number"])


async def submit_lulu_print_job(order_id: str, preview_id: str) -> None:
    """
    Background task: Generate Lulu-spec PDFs and submit a print job.

    Called from the Shopify webhook handler after PDF generation completes.

    Args:
        order_id:   Shopify order ID (matches orders.order_id)
        preview_id: UUID of the preview (matches previews.preview_id)
    """
    import time as _time
    task_start_time = _time.monotonic()

    settings = get_settings()
    db = get_db()

    logger.info(
        "=== LULU PRINT JOB SUBMISSION STARTED ===",
        order_id=order_id,
        preview_id=preview_id,
        lulu_api_base=settings.lulu_api_base,
        is_sandbox="sandbox" in settings.lulu_api_base,
    )

    try:
        # ----------------------------------------------------------------
        # 1. Load preview and order data
        # ----------------------------------------------------------------
        preview_resp = db.table("previews").select("*").eq("preview_id", preview_id).execute()
        if not preview_resp.data:
            logger.error("Preview not found for Lulu job", preview_id=preview_id)
            return
        preview = preview_resp.data[0]

        order_resp = db.table("orders").select("*").eq("order_id", order_id).execute()
        if not order_resp.data:
            logger.error("Order not found for Lulu job", order_id=order_id)
            return
        order = order_resp.data[0]

        child_name = preview.get("child_name", "Child")
        story_title = f"{child_name}'s Magical Adventure"

        # ----------------------------------------------------------------
        # 2. Check if print_order already exists (idempotency)
        # ----------------------------------------------------------------
        existing = db.table("print_orders").select("print_order_id,lulu_status").eq(
            "order_id", order_id
        ).execute()

        if existing.data:
            existing_status = existing.data[0].get("lulu_status", "")
            if existing_status not in ("failed", "pending"):
                logger.info(
                    "Print order already exists and is not failed",
                    order_id=order_id,
                    status=existing_status,
                )
                return

        # ----------------------------------------------------------------
        # 3. Verify pages are ready (should always be true since we're called
        #    from generate_remaining_pages_and_pdf AFTER PDF is created)
        # ----------------------------------------------------------------
        hires = preview.get("hires_images") or []
        if isinstance(hires, str):
            try:
                import json as _json
                hires = _json.loads(hires)
            except Exception:
                hires = []

        phase = preview.get("generation_phase", "")
        # Valid phases: pages_complete (legacy), preparing_print (new physical flow), complete (digital)
        valid_phases = (
            GenerationPhase.PAGES_COMPLETE.value,
            GenerationPhase.PREPARING_PRINT.value,
            GenerationPhase.COMPLETE.value,
        )
        if phase not in valid_phases and len(hires) < 10:
            logger.error(
                "Pages not ready for Lulu submission — this should not happen "
                "since we're called after PDF generation",
                phase=phase,
                pages=len(hires),
                preview_id=preview_id
            )
            raise RuntimeError(
                f"Pages not ready: phase={phase}, pages={len(hires)}. "
                "submit_lulu_print_job must be called after PDF generation."
            )

        logger.info("Pages verified ready for Lulu", pages=len(hires), preview_id=preview_id)

        # ----------------------------------------------------------------
        # 4. Collect pages from preview record
        # ----------------------------------------------------------------
        pages = _collect_pages(preview)
        if len(pages) < 2:
            logger.error(
                "Not enough pages to generate Lulu PDFs",
                order_id=order_id,
                pages_found=len(pages),
            )
            return

        cover_page = next((p for p in pages if p["page_number"] == 0), None)
        cover_image_url = cover_page["image_url"] if cover_page else None

        # ----------------------------------------------------------------
        # 4. Generate interior + cover PDFs
        # ----------------------------------------------------------------
        pdf_start_time = _time.monotonic()

        logger.info("Generating Lulu interior PDF", preview_id=preview_id, pages_count=len(pages))
        interior_url = await generate_interior_pdf(pages, preview_id, child_name)
        interior_duration_ms = round((_time.monotonic() - pdf_start_time) * 1000)
        logger.info(
            "Lulu interior PDF generated",
            preview_id=preview_id,
            interior_url=interior_url[:80] + "..." if interior_url else None,
            duration_ms=interior_duration_ms,
        )

        cover_start_time = _time.monotonic()
        logger.info("Generating Lulu cover PDF", preview_id=preview_id)
        cover_url = await generate_cover_pdf(
            cover_image_url=cover_image_url,
            child_name=child_name,
            story_title=story_title,
            preview_id=preview_id,
        )
        cover_duration_ms = round((_time.monotonic() - cover_start_time) * 1000)
        logger.info(
            "Lulu cover PDF generated",
            preview_id=preview_id,
            cover_url=cover_url[:80] + "..." if cover_url else None,
            duration_ms=cover_duration_ms,
        )

        # ----------------------------------------------------------------
        # 5. Insert or update print_orders record
        # ----------------------------------------------------------------
        shipping_address = _build_shipping_address(order, preview)

        logger.info(
            "Shipping address prepared for Lulu submission",
            order_id=order_id,
            name_initials=(shipping_address.get("name") or "")[:2] + "***",
            city=shipping_address.get("city"),
            state_code=shipping_address.get("state_code"),
            country_code=shipping_address.get("country_code"),
            postcode_prefix=(shipping_address.get("postcode") or "")[:3] + "***",
            has_phone=bool(shipping_address.get("phone_number")),
            has_email=bool(shipping_address.get("email")),
            street1_present=bool(shipping_address.get("street1")),
        )
        print_order_data = {
            "order_id": order_id,
            "preview_id": preview_id,
            "interior_pdf_url": interior_url,
            "cover_pdf_url": cover_url,
            "pod_package_id": settings.lulu_pod_package_id,
            "lulu_status": "pending",
            "shipping_address": shipping_address,
            "shipping_option": "MAIL",
            "attempts": 0,
            "created_at": datetime.utcnow().isoformat(),
        }

        if existing.data:
            # Update existing failed record
            db.table("print_orders").update(print_order_data).eq("order_id", order_id).execute()
            print_order_id = existing.data[0]["print_order_id"]
        else:
            insert_resp = db.table("print_orders").insert(print_order_data).execute()
            print_order_id = insert_resp.data[0].get("print_order_id") if insert_resp.data else None

        # ----------------------------------------------------------------
        # 6. Update phase to submitting_print and submit to Lulu
        # ----------------------------------------------------------------
        logger.info("Submitting print job to Lulu", order_id=order_id)

        # Update preview phase to indicate Lulu submission in progress
        db.table("previews").update({
            "generation_phase": GenerationPhase.SUBMITTING_PRINT.value,
        }).eq("preview_id", preview_id).execute()

        lulu_response = await create_print_job(
            interior_url=interior_url,
            cover_url=cover_url,
            shipping_address=shipping_address,
            order_id=order_id,
            child_name=child_name,
            quantity=1,
            shipping_option="MAIL",
        )

        lulu_job_id = str(lulu_response.get("id", ""))
        lulu_status_raw = lulu_response.get("status", {}).get("name", "")
        mapped_status = map_lulu_status(lulu_status_raw)

        logger.info(
            "Lulu API response received",
            order_id=order_id,
            lulu_job_id=lulu_job_id,
            lulu_status_raw=lulu_status_raw,
            lulu_status_mapped=mapped_status,
            response_keys=list(lulu_response.keys()) if lulu_response else [],
        )

        # ----------------------------------------------------------------
        # 7. Update print_orders with Lulu response
        # ----------------------------------------------------------------
        update_data = {
            "lulu_print_job_id": lulu_job_id,
            "lulu_status": mapped_status,
            "lulu_status_raw": lulu_status_raw,
            "lulu_api_response": lulu_response,
            "submitted_at": datetime.utcnow().isoformat(),
            "attempts": 1,
        }

        if print_order_id:
            db.table("print_orders").update(update_data).eq(
                "print_order_id", print_order_id
            ).execute()
        else:
            db.table("print_orders").update(update_data).eq("order_id", order_id).execute()

        # ----------------------------------------------------------------
        # 8. Update preview phase to print_submitted and order to COMPLETED
        # ----------------------------------------------------------------
        db.table("previews").update({
            "generation_phase": GenerationPhase.PRINT_SUBMITTED.value,
        }).eq("preview_id", preview_id).execute()

        db.table("orders").update({
            "status": OrderStatus.COMPLETED.value,
        }).eq("order_id", order_id).execute()

        total_duration_ms = round((_time.monotonic() - task_start_time) * 1000)
        logger.info(
            "=== LULU PRINT JOB SUBMITTED SUCCESSFULLY ===",
            order_id=order_id,
            lulu_job_id=lulu_job_id,
            lulu_status=lulu_status_raw,
            generation_phase=GenerationPhase.PRINT_SUBMITTED.value,
            total_duration_ms=total_duration_ms,
            interior_pdf_duration_ms=interior_duration_ms,
            cover_pdf_duration_ms=cover_duration_ms,
        )

    except Exception as e:
        total_duration_ms = round((_time.monotonic() - task_start_time) * 1000)
        logger.error(
            "=== LULU PRINT JOB SUBMISSION FAILED ===",
            order_id=order_id,
            preview_id=preview_id,
            error=str(e),
            error_type=type(e).__name__,
            total_duration_ms=total_duration_ms,
        )

        # Record the failure in DB - update both print_orders and preview phase
        try:
            db.table("print_orders").update({
                "lulu_status": "failed",
                "last_error": str(e),
            }).eq("order_id", order_id).execute()

            # Set preview phase to print_failed (PDF is ready, Lulu submission failed)
            db.table("previews").update({
                "generation_phase": GenerationPhase.PRINT_FAILED.value,
            }).eq("preview_id", preview_id).execute()

            # Update order status to failed
            db.table("orders").update({
                "status": OrderStatus.FAILED.value,
                "error_message": f"Lulu print submission failed: {str(e)}",
            }).eq("order_id", order_id).execute()
        except Exception as db_error:
            logger.error(
                "Failed to update database after Lulu submission error",
                order_id=order_id,
                preview_id=preview_id,
                db_error=str(db_error),
            )
