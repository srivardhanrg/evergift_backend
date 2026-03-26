"""
Lulu Print Background Tasks

Called after StoryGift PDF generation completes (i.e. after order is paid).

Flow:
1. Generate Lulu-spec interior PDF (8.75x8.75" with bleed, 24 pages)
2. Generate Lulu-spec cover wrap PDF (front + spine + back)
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
from app.stories.themes import get_theme

logger = structlog.get_logger()


def _validate_page_count(page_count: int, cover_type: str) -> None:
    """
    Validate that page count meets Lulu's requirements for the given cover type.

    Lulu Requirements:
    - Saddle Stitch (softcover): 4-48 pages, must be even
    - Hardcover (casewrap): 24-800 pages, must be even

    Args:
        page_count: Number of interior pages
        cover_type: "softcover" or "hardcover"

    Raises:
        ValueError: If page count doesn't meet requirements
    """
    # Page count must be even (required by all binding types)
    if page_count % 2 != 0:
        raise ValueError(
            f"Page count must be even for Lulu print jobs. Got {page_count} pages. "
            f"This is a critical error - Lulu will reject the job."
        )

    # Cover-type specific validation
    if cover_type == "softcover":
        # Saddle stitch: 4-48 pages
        if page_count < 4:
            raise ValueError(
                f"Softcover (saddle stitch) requires minimum 4 pages. Got {page_count} pages."
            )
        if page_count > 48:
            raise ValueError(
                f"Softcover (saddle stitch) supports maximum 48 pages. Got {page_count} pages. "
                f"Use hardcover binding for books with more than 48 pages."
            )
    else:  # hardcover
        # Hardcover casewrap: 24-800 pages
        if page_count < 24:
            raise ValueError(
                f"Hardcover (casewrap) requires minimum 24 pages. Got {page_count} pages. "
                f"Use softcover binding for books with fewer than 24 pages."
            )
        if page_count > 800:
            raise ValueError(
                f"Hardcover (casewrap) supports maximum 800 pages. Got {page_count} pages."
            )

    logger.info(
        "Page count validation passed",
        page_count=page_count,
        cover_type=cover_type,
        is_even=page_count % 2 == 0,
    )


def _truncate_field(value: str, max_length: int) -> str:
    """Truncate a field to max_length, preserving whole words if possible."""
    if not value or len(value) <= max_length:
        return value
    # Try to break at a space
    truncated = value[:max_length]
    last_space = truncated.rfind(" ")
    if last_space > max_length // 2:
        return truncated[:last_space].strip()
    return truncated.strip()


def _build_shipping_address(order: dict, preview: dict) -> dict:
    """
    Convert Shopify shipping address format to Lulu's format.

    Shopify fields (from webhook):
        first_name, last_name, address1, address2, city,
        province, province_code, country, country_code, zip, phone, email
    Lulu fields (required):
        name, street1, city, country_code, postcode, phone_number, email

    Lulu field limits:
        name: 30 chars, street1: 30 chars, street2: 30 chars, city: 30 chars
    """
    # Lulu API field character limits
    LULU_MAX_NAME = 30
    LULU_MAX_STREET = 30
    LULU_MAX_CITY = 30

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

    # Handle long addresses: if street1 > 30 chars, overflow to street2
    street1 = shopify_addr.get("address1", "") or ""
    street2 = shopify_addr.get("address2", "") or ""

    if len(street1) > LULU_MAX_STREET:
        # Try to split at a sensible point
        overflow = street1[LULU_MAX_STREET:].strip()
        street1 = _truncate_field(street1, LULU_MAX_STREET)
        # Prepend overflow to street2
        if overflow:
            street2 = f"{overflow} {street2}".strip() if street2 else overflow

    return {
        "name": _truncate_field(name, LULU_MAX_NAME),
        "street1": _truncate_field(street1, LULU_MAX_STREET),
        "street2": _truncate_field(street2, LULU_MAX_STREET),
        "city": _truncate_field(shopify_addr.get("city", ""), LULU_MAX_CITY),
        "state_code": shopify_addr.get("province_code") or shopify_addr.get("province", ""),
        "country_code": shopify_addr.get("country_code") or shopify_addr.get("country", "IN"),
        "postcode": shopify_addr.get("zip", ""),
        "phone_number": shopify_addr.get("phone", ""),
        "email": email,  # Required by Lulu API
    }


def _collect_pages_v2(preview: dict) -> list:
    """
    Collect all interior pages from a V2 preview record for Lulu print.

    V2 format uses book_structure.pages (26-page structure):
    - Index 0: Cover (excluded - goes to cover wrap PDF)
    - Indices 1-24: Interior pages (ALL must be included for 24-page book)
    - Index 25: Back cover (excluded - TODO: not yet in cover wrap)

    For Lulu interior PDF, we collect all pages with indices 1-24.

    Returns:
        List of dicts with keys: page_number, image_url, story_text
        page_number is the Lulu page number (1-24)

    Raises:
        RuntimeError: If any of the 24 interior pages are missing or have no image
    """
    preview_id = preview.get("preview_id", "unknown")

    # Get book structure
    book_structure = preview.get("book_structure") or {}
    if isinstance(book_structure, str):
        try:
            book_structure = json.loads(book_structure)
        except Exception:
            book_structure = {}

    # V2 format stores pages as flat dict with string keys: {"0": {...}, "1": {...}, ...}
    # Convert to index → page mapping
    pages_by_index = {}
    for idx_str, page_data in book_structure.items():
        if idx_str.isdigit():  # Skip non-numeric keys
            page_index = int(idx_str)
            pages_by_index[page_index] = {
                "index": page_index,
                "imageUrl": page_data.get("url"),
                "pageType": page_data.get("type"),
                "isLocked": page_data.get("is_locked", False)
            }

    # Get story texts for text pages
    story_texts = preview.get("story_texts") or {}
    if isinstance(story_texts, str):
        try:
            story_texts = json.loads(story_texts)
        except Exception:
            story_texts = {}

    # Collect all interior pages (indices 1-24)
    pages = []
    missing_pages = []
    missing_images = []

    for page_index in range(1, 25):  # Indices 1 through 24 inclusive
        page = pages_by_index.get(page_index)

        if not page:
            missing_pages.append(page_index)
            logger.error(
                "Interior page missing from book_structure",
                preview_id=preview_id,
                page_index=page_index
            )
            continue

        # Validate that page has an image
        image_url = page.get("imageUrl")
        if not image_url:
            missing_images.append(page_index)
            logger.error(
                "Interior page missing imageUrl",
                preview_id=preview_id,
                page_index=page_index,
                page_type=page.get("pageType")
            )
            continue

        # Get story text for text pages
        story_text = ""
        if page.get("pageType") == "text":
            # story_texts uses string keys (book indices)
            story_text = story_texts.get(str(page_index), "")

        # Lulu page number = sequential 1-24
        pages.append({
            "page_number": page_index,  # Use index directly as page_number
            "image_url": image_url,
            "story_text": story_text,
        })

    # Fail fast if any pages are missing or incomplete
    if missing_pages or missing_images:
        error_msg = f"Cannot generate Lulu PDF: "
        if missing_pages:
            error_msg += f"{len(missing_pages)} pages missing (indices: {missing_pages})"
        if missing_images:
            if missing_pages:
                error_msg += ", "
            error_msg += f"{len(missing_images)} pages missing images (indices: {missing_images})"

        logger.error(
            "Lulu PDF generation blocked - incomplete book structure",
            preview_id=preview_id,
            missing_pages=missing_pages,
            missing_images=missing_images,
            total_collected=len(pages)
        )
        raise RuntimeError(error_msg)

    # Validate we have exactly 24 pages
    if len(pages) != 24:
        error_msg = f"Expected 24 interior pages, but collected {len(pages)}"
        logger.error(
            "Invalid page count for Lulu PDF",
            preview_id=preview_id,
            expected=24,
            actual=len(pages)
        )
        raise RuntimeError(error_msg)

    logger.info(
        "Collected V2 pages for Lulu print - 24-page interior PDF",
        preview_id=preview_id,
        pages_count=len(pages),
        page_indices=list(range(1, 25))
    )

    return sorted(pages, key=lambda p: p["page_number"])


def _collect_pages(preview: dict) -> list:
    """
    Collect all story pages from a preview record.
    Supports both V1 (legacy) and V2 (book_structure) formats.

    V1: Reads from hires_images, preview_images, story_pages columns
    V2: Reads from book_structure.pages, story_texts columns
    """
    # Check if this is a V2 preview (has book_structure)
    book_structure = preview.get("book_structure")
    if book_structure:
        logger.debug("Using V2 page collection", preview_id=preview.get("preview_id"))
        return _collect_pages_v2(preview)

    # Otherwise use legacy V1 logic
    logger.debug("Using V1 (legacy) page collection", preview_id=preview.get("preview_id"))

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

        # Read cover_type early — needed for PDF generation (spine, safety zone)
        cover_type = order.get("cover_type")
        if not cover_type or cover_type not in ("softcover", "hardcover"):
            logger.error(
                "Missing or invalid cover_type in order. Cannot proceed with print job.",
                order_id=order_id,
                cover_type=cover_type,
            )
            raise ValueError(f"Missing or invalid cover_type '{cover_type}' for physical order")
        logger.info("Cover type for this order", order_id=order_id, cover_type=cover_type)

        child_name = preview.get("child_name", "Child")
        # Derive story title from the actual theme — each theme has its own title template
        # e.g. Ocean Explorer → "{name}'s Underwater Kingdom", not "Magical Adventure"
        _theme_id = preview.get("theme", "")
        try:
            _template = get_theme(_theme_id)
            story_title = _template.get_title(child_name)
        except Exception:
            # Fallback: generic title if theme not found (should never happen in practice)
            logger.warning(
                "Could not load theme for story title — using generic fallback",
                theme_id=_theme_id,
                preview_id=preview_id,
            )
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
        # 4. Collect interior pages and resolve cover image URL
        # ----------------------------------------------------------------
        pages = _collect_pages(preview)
        if len(pages) < 2:
            logger.error(
                "Not enough pages to generate Lulu PDFs",
                order_id=order_id,
                pages_found=len(pages),
            )
            return

        # The cover image is stored in previews.cover_url (a dedicated column set during
        # preview generation). It is NOT in hires_images or preview_images — those arrays
        # only contain story pages 1-10. _collect_pages() will never find page 0.
        cover_image_url = preview.get("cover_url") or None
        cover_url_source = "preview.cover_url"

        if not cover_image_url:
            # Fallback for legacy orders where cover_url column may not be populated:
            # use the first hires_image (page 1) as the cover image.
            cover_page = next((p for p in pages if p["page_number"] == 1), None)
            cover_image_url = cover_page["image_url"] if cover_page else None
            cover_url_source = "hires_images[page_1]_fallback"

        logger.info(
            "Cover image URL resolved for Lulu cover PDF",
            preview_id=preview_id,
            has_cover_image=bool(cover_image_url),
            source=cover_url_source,
        )

        # ----------------------------------------------------------------
        # 4. Generate interior + cover PDFs (with MD5 hashes)
        # ----------------------------------------------------------------
        pdf_start_time = _time.monotonic()

        logger.info("Generating Lulu interior PDF", preview_id=preview_id, pages_count=len(pages))
        interior_url, interior_md5 = await generate_interior_pdf(pages, preview_id, child_name)
        interior_duration_ms = round((_time.monotonic() - pdf_start_time) * 1000)
        logger.info(
            "Lulu interior PDF generated",
            preview_id=preview_id,
            interior_url=interior_url[:80] + "..." if interior_url else None,
            interior_md5=interior_md5,
            duration_ms=interior_duration_ms,
        )

        cover_start_time = _time.monotonic()
        logger.info("Generating Lulu cover PDF", preview_id=preview_id, cover_type=cover_type)
        cover_url, cover_md5 = await generate_cover_pdf(
            cover_image_url=cover_image_url,
            child_name=child_name,
            story_title=story_title,
            preview_id=preview_id,
            cover_type=cover_type,
        )
        cover_duration_ms = round((_time.monotonic() - cover_start_time) * 1000)
        logger.info(
            "Lulu cover PDF generated",
            preview_id=preview_id,
            cover_url=cover_url[:80] + "..." if cover_url else None,
            cover_md5=cover_md5,
            duration_ms=cover_duration_ms,
        )

        # ----------------------------------------------------------------
        # 4b. Validate page count before Lulu submission (pre-flight check)
        # ----------------------------------------------------------------
        # The interior PDF is always generated with 24 pages (TOTAL_PAGES constant),
        # but we validate explicitly as a safeguard and to make requirements clear.
        # Lulu will reject jobs with odd page counts or out-of-range counts AFTER
        # job creation, wasting API calls and causing silent failures.
        from app.services.lulu_pdf_generator import TOTAL_PAGES

        try:
            _validate_page_count(TOTAL_PAGES, cover_type)
        except ValueError as e:
            logger.error(
                "Page count validation failed - cannot submit to Lulu",
                order_id=order_id,
                preview_id=preview_id,
                page_count=TOTAL_PAGES,
                cover_type=cover_type,
                error=str(e),
            )
            raise RuntimeError(
                f"Page count validation failed: {e}. "
                f"This is a configuration error - please contact support."
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
        # Select pod_package_id based on cover_type (now guaranteed to be set)
        if cover_type == "softcover":
            pod_package_id = settings.lulu_pod_package_id_softcover
        else:
            pod_package_id = settings.lulu_pod_package_id_hardcover

        print_order_data = {
            "order_id": order_id,
            "preview_id": preview_id,
            "interior_pdf_url": interior_url,
            "cover_pdf_url": cover_url,
            "pod_package_id": pod_package_id,
            "cover_type": cover_type,
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
        # 7. Update phase to submitting_print and submit to Lulu
        # ----------------------------------------------------------------
        logger.info("Submitting print job to Lulu", order_id=order_id, cover_type=cover_type)

        # Update preview phase to indicate Lulu submission in progress
        db.table("previews").update({
            "generation_phase": GenerationPhase.SUBMITTING_PRINT.value,
        }).eq("preview_id", preview_id).execute()

        lulu_response = await create_print_job(
            interior_url=interior_url,
            interior_md5=interior_md5,
            cover_url=cover_url,
            cover_md5=cover_md5,
            shipping_address=shipping_address,
            order_id=order_id,
            child_name=child_name,
            quantity=1,
            shipping_option="MAIL",
            cover_type=cover_type,
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

        # Re-raise so caller knows submission failed
        raise
