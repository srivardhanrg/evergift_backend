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
from app.services.lulu_service import create_print_job, map_lulu_status
from app.services.lulu_pdf_generator import generate_interior_pdf, generate_cover_pdf

logger = structlog.get_logger()


def _build_shipping_address(order: dict, preview: dict) -> dict:
    """
    Convert Shopify shipping address format to Lulu's format.

    Shopify fields (from webhook):
        first_name, last_name, address1, address2, city,
        province, province_code, country, country_code, zip, phone
    Lulu fields:
        name, street1, street2, city, state_code, country_code, postcode, phone_number
    """
    shopify_addr = order.get("shipping_address") or {}

    first = shopify_addr.get("first_name", "")
    last = shopify_addr.get("last_name", "")
    name = f"{first} {last}".strip() or order.get("customer_name", "Customer")

    return {
        "name": name,
        "street1": shopify_addr.get("address1", ""),
        "street2": shopify_addr.get("address2", ""),
        "city": shopify_addr.get("city", ""),
        "state_code": shopify_addr.get("province_code") or shopify_addr.get("province", ""),
        "country_code": shopify_addr.get("country_code") or shopify_addr.get("country", "IN"),
        "postcode": shopify_addr.get("zip", ""),
        "phone_number": shopify_addr.get("phone", ""),
        # Note: email not passed to Lulu - contact_email is set in lulu_service.py
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
    settings = get_settings()
    db = get_db()

    logger.info("Starting Lulu print job submission", order_id=order_id, preview_id=preview_id)

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
        if phase not in ("complete", "pages_complete") and len(hires) < 10:
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
        logger.info("Generating Lulu interior PDF", preview_id=preview_id)
        interior_url = await generate_interior_pdf(pages, preview_id, child_name)

        logger.info("Generating Lulu cover PDF", preview_id=preview_id)
        cover_url = await generate_cover_pdf(
            cover_image_url=cover_image_url,
            child_name=child_name,
            story_title=story_title,
            preview_id=preview_id,
        )

        # ----------------------------------------------------------------
        # 5. Insert or update print_orders record
        # ----------------------------------------------------------------
        shipping_address = _build_shipping_address(order, preview)
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
        # 6. Submit to Lulu
        # ----------------------------------------------------------------
        logger.info("Submitting print job to Lulu", order_id=order_id)

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

        logger.info(
            "Lulu print job submitted successfully",
            order_id=order_id,
            lulu_job_id=lulu_job_id,
            lulu_status=lulu_status_raw,
        )

    except Exception as e:
        logger.error(
            "Lulu print job submission failed",
            order_id=order_id,
            preview_id=preview_id,
            error=str(e),
        )

        # Record the failure in DB
        try:
            db.table("print_orders").update({
                "lulu_status": "failed",
                "last_error": str(e),
            }).eq("order_id", order_id).execute()
        except Exception:
            pass
