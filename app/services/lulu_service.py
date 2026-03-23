"""
Lulu Print API Service

Handles OAuth2 authentication and all Lulu API interactions:
- Token management (auto-refresh)
- Cost calculations
- Print job creation
- Status polling
- Shipping options
- Webhook registration
"""

import os
import time
import httpx
import structlog
from typing import Optional
from app.config import get_settings

logger = structlog.get_logger()

# ---------------------------------------------------------------------------
# Token cache (in-memory, sufficient for single-process FastAPI)
# ---------------------------------------------------------------------------
_token_cache: dict = {
    "access_token": None,
    "expires_at": 0.0,
}


async def _get_access_token() -> str:
    """
    Get a valid Lulu OAuth2 access token.
    Refreshes automatically when within 60s of expiry.
    """
    settings = get_settings()

    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["access_token"]

    logger.info("Fetching new Lulu access token")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            settings.lulu_auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.lulu_client_key,
                "client_secret": settings.lulu_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if resp.status_code != 200:
        logger.error("Lulu auth failed", status=resp.status_code, body=resp.text)
        raise RuntimeError(f"Lulu authentication failed: {resp.status_code} {resp.text}")

    data = resp.json()
    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data.get("expires_in", 3600)

    logger.info("Lulu access token obtained", expires_in=data.get("expires_in"))
    return _token_cache["access_token"]


async def _lulu_headers() -> dict:
    token = await _get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# ---------------------------------------------------------------------------
# Cost Calculation
# ---------------------------------------------------------------------------

async def calculate_print_cost(
    interior_url: str,
    cover_url: str,
    quantity: int = 1,
    shipping_option: str = "MAIL",
    country_code: str = "IN",
    cover_type: str = "hardcover",
) -> dict:
    """
    Calculate the cost of a Lulu print job before ordering.

    Args:
        interior_url: URL to interior PDF (24 pages)
        cover_url: URL to cover wrap PDF
        quantity: Number of copies (default 1)
        shipping_option: Lulu shipping level (default MAIL)
        country_code: Destination country (default IN)
        cover_type: Cover type - "softcover" (saddle stitch) or "hardcover" (perfect bound)

    Returns a dict with:
        total_cost_incl_tax, print_cost, shipping_cost, currency
    """
    import time as _time
    start_time = _time.monotonic()

    settings = get_settings()
    headers = await _lulu_headers()

    # Select pod_package_id based on cover type
    if cover_type == "softcover":
        pod_package_id = settings.lulu_pod_package_id_softcover
    elif cover_type == "hardcover":
        pod_package_id = settings.lulu_pod_package_id_hardcover
    else:
        # Fallback to hardcover for invalid values
        logger.warning(
            "Invalid cover_type provided, falling back to hardcover",
            cover_type=cover_type
        )
        pod_package_id = settings.lulu_pod_package_id_hardcover

    payload = {
        "line_items": [
            {
                "page_count": 24,           # 24 interior pages (indices 1-24)
                "pod_package_id": pod_package_id,
                "quantity": quantity,
                "title": "MagicTales Storybook",
                "cover": {"source_url": cover_url},
                "interior": {"source_url": interior_url},
            }
        ],
        "shipping_address": {
            "country": country_code,
        },
        "shipping_level": shipping_option,  # API field is shipping_level
    }

    logger.info(
        "Lulu API request - calculating cost",
        endpoint=f"{settings.lulu_api_base}/print-job-cost-calculations/",
        country_code=country_code,
        shipping_level=shipping_option,
        quantity=quantity,
        cover_type=cover_type,
        pod_package_id=pod_package_id,
    )

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/print-job-cost-calculations/",
            json=payload,
            headers=headers,
        )

    duration_ms = round((_time.monotonic() - start_time) * 1000)

    if resp.status_code not in (200, 201):
        logger.error(
            "Lulu cost calculation failed",
            status=resp.status_code,
            body=resp.text,
            duration_ms=duration_ms,
        )
        raise RuntimeError(f"Lulu cost calc failed: {resp.status_code} {resp.text}")

    data = resp.json()
    logger.info(
        "Lulu cost calculated successfully",
        total_cost=data.get("total_cost_incl_tax"),
        currency=data.get("currency"),
        shipping_cost=data.get("shipping_cost"),
        duration_ms=duration_ms,
    )
    return data


# ---------------------------------------------------------------------------
# Print Job Creation
# ---------------------------------------------------------------------------

async def create_print_job(
    interior_url: str,
    cover_url: str,
    shipping_address: dict,
    order_id: str,
    child_name: str,
    quantity: int = 1,
    shipping_option: str = "MAIL",
    cover_type: str = "hardcover",
) -> dict:
    """
    Create a Lulu print job.

    Args:
        interior_url: URL to interior PDF (24 pages)
        cover_url: URL to cover wrap PDF
        shipping_address: Dict with name, street1, city, state_code, country_code, postcode, phone_number
        order_id: Shopify order ID (used as external_id)
        child_name: Child's name for book title
        quantity: Number of copies (default 1)
        shipping_option: Lulu shipping level (default MAIL)
        cover_type: Cover type - "softcover" (saddle stitch) or "hardcover" (perfect bound)

    Returns the full Lulu API response (contains id, status, etc.)
    """
    import time as _time
    start_time = _time.monotonic()

    settings = get_settings()
    headers = await _lulu_headers()

    # Select pod_package_id based on cover type
    if cover_type == "softcover":
        pod_package_id = settings.lulu_pod_package_id_softcover
    elif cover_type == "hardcover":
        pod_package_id = settings.lulu_pod_package_id_hardcover
    else:
        # Fallback to hardcover for invalid values
        logger.warning(
            "Invalid cover_type provided, falling back to hardcover",
            cover_type=cover_type
        )
        pod_package_id = settings.lulu_pod_package_id_hardcover

    payload = {
        # contact_email is for Lulu to contact about print issues, NOT customer email
        "contact_email": "support@storygift.in",
        "line_items": [
            {
                "title": f"{child_name}'s MagicTales Storybook",
                "quantity": quantity,
                # Lulu API requires cover/interior/pod_package_id nested inside
                # printable_normalization (the shorthand flat structure causes 500 errors)
                "printable_normalization": {
                    "pod_package_id": pod_package_id,
                    "cover": {
                        "source_url": cover_url,
                    },
                    "interior": {
                        "source_url": interior_url,
                    },
                },
            }
        ],
        # production_delay must be 60–2880 minutes per Lulu API docs.
        # 0 is invalid and causes a 500 Internal Server Error on their servers.
        # 60 minutes gives a 1-hour window to cancel before printing starts.
        "production_delay": 60,
        "shipping_address": {
            "name": shipping_address.get("name", ""),
            "street1": shipping_address.get("street1", ""),
            "street2": shipping_address.get("street2", ""),
            "city": shipping_address.get("city", ""),
            "state_code": shipping_address.get("state_code", ""),
            "country_code": shipping_address.get("country_code", "IN"),
            "postcode": shipping_address.get("postcode", ""),
            "phone_number": shipping_address.get("phone_number", ""),
            "email": shipping_address.get("email", ""),  # Required by Lulu API
        },
        "shipping_level": shipping_option,  # API field is shipping_level
        "external_id": order_id,  # Our order reference
    }

    # NOTE: Webhooks must be registered separately via POST /webhooks/
    # The event_notifications field in print job payload is not supported.
    # Use register_webhook() to set up webhook before creating print jobs.

    # DEBUG: Log sanitized request payload
    logger.info(
        "Lulu API request - creating print job",
        endpoint=f"{settings.lulu_api_base}/print-jobs/",
        order_id=order_id,
        pod_package_id=pod_package_id,
        cover_type=cover_type,
        quantity=quantity,
        shipping_level=shipping_option,
        shipping_country=shipping_address.get("country_code", "IN"),
        shipping_city=shipping_address.get("city", ""),
        shipping_state=shipping_address.get("state_code", ""),
        has_phone=bool(shipping_address.get("phone_number")),
        has_email=bool(shipping_address.get("email")),
        has_street1=bool(shipping_address.get("street1")),
        interior_url_prefix=interior_url[:50] + "..." if interior_url else None,
        cover_url_prefix=cover_url[:50] + "..." if cover_url else None,
    )

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/print-jobs/",
            json=payload,
            headers=headers,
        )

    duration_ms = round((_time.monotonic() - start_time) * 1000)

    if resp.status_code not in (200, 201):
        logger.error(
            "Lulu print job creation failed",
            status=resp.status_code,
            body=resp.text,
            order_id=order_id,
            duration_ms=duration_ms,
        )
        raise RuntimeError(f"Lulu print job failed: {resp.status_code} {resp.text}")

    data = resp.json()

    # DEBUG: Log full success response for debugging
    logger.info(
        "Lulu print job created successfully",
        lulu_job_id=data.get("id"),
        status_name=data.get("status", {}).get("name"),
        status_message=data.get("status", {}).get("message"),
        order_id=order_id,
        duration_ms=duration_ms,
        costs=data.get("costs"),
        estimated_shipping=data.get("estimated_shipping_dates"),
        response_keys=list(data.keys()),
    )
    return data


# ---------------------------------------------------------------------------
# Job Status
# ---------------------------------------------------------------------------

async def get_print_job_status(lulu_job_id: str) -> dict:
    """
    Get the current status of a Lulu print job.
    Returns the full status object from Lulu.
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{settings.lulu_api_base}/print-jobs/{lulu_job_id}/status/",
            headers=headers,
        )

    if resp.status_code != 200:
        logger.error("Lulu status check failed", status=resp.status_code, lulu_job_id=lulu_job_id)
        raise RuntimeError(f"Lulu status check failed: {resp.status_code}")

    return resp.json()


async def get_print_job(lulu_job_id: str) -> dict:
    """
    Get the full print job details (includes tracking, line items, etc.)
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{settings.lulu_api_base}/print-jobs/{lulu_job_id}/",
            headers=headers,
        )

    if resp.status_code != 200:
        logger.error("Lulu job fetch failed", status=resp.status_code, lulu_job_id=lulu_job_id)
        raise RuntimeError(f"Lulu job fetch failed: {resp.status_code}")

    return resp.json()


# ---------------------------------------------------------------------------
# Shipping Options
# ---------------------------------------------------------------------------

async def get_shipping_options(
    country_code: str,
    state_code: Optional[str] = None,
    cover_type: str = "hardcover",
) -> list:
    """
    Get available shipping options and their costs for a destination.

    Args:
        country_code: Destination country code
        state_code: Optional state code (required for some countries like US)
        cover_type: Cover type - "softcover" (saddle stitch) or "hardcover" (perfect bound)
    """
    settings = get_settings()
    headers = await _lulu_headers()

    # Select pod_package_id based on cover type
    if cover_type == "softcover":
        pod_package_id = settings.lulu_pod_package_id_softcover
    else:
        pod_package_id = settings.lulu_pod_package_id_hardcover

    payload = {
        "line_items": [
            {
                "page_count": 24,
                "pod_package_id": pod_package_id,
                "quantity": 1,
            }
        ],
        "shipping_address": {
            "country": country_code,
            **({"state_code": state_code} if state_code else {}),
        },
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/shipping-options/",
            json=payload,
            headers=headers,
        )

    if resp.status_code not in (200, 201):
        logger.error("Lulu shipping options failed", status=resp.status_code, body=resp.text)
        raise RuntimeError(f"Lulu shipping options failed: {resp.status_code}")

    data = resp.json()
    return data.get("results", [])


# ---------------------------------------------------------------------------
# Cancel Job
# ---------------------------------------------------------------------------

async def cancel_print_job(lulu_job_id: str) -> bool:
    """
    Cancel a Lulu print job (only possible before IN_PRODUCTION).
    Returns True if cancelled successfully.
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.put(
            f"{settings.lulu_api_base}/print-jobs/{lulu_job_id}/status/",
            json={"name": "CANCELLED"},
            headers=headers,
        )

    success = resp.status_code in (200, 204)
    if not success:
        logger.warning(
            "Lulu job cancellation failed",
            status=resp.status_code,
            lulu_job_id=lulu_job_id,
        )
    return success





# ---------------------------------------------------------------------------
# Webhook Management
# ---------------------------------------------------------------------------

async def register_webhook(webhook_url: str) -> dict:
    """
    Register a webhook URL with Lulu to receive PRINT_JOB_STATUS_CHANGED events.

    This is a one-time setup. The webhook will be called whenever a print job
    status changes (e.g., CREATED → IN_PRODUCTION → SHIPPED).

    Args:
        webhook_url: Full URL where Lulu should send webhook notifications
                     e.g., "https://magictales-backend.onrender.com/webhooks/lulu/lulu"

    Returns:
        Lulu API response with webhook id, is_active, topics, url
    """
    settings = get_settings()
    headers = await _lulu_headers()

    payload = {
        "topics": ["PRINT_JOB_STATUS_CHANGED"],
        "url": webhook_url,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/webhooks/",
            json=payload,
            headers=headers,
        )

    if resp.status_code not in (200, 201):
        logger.error(
            "Lulu webhook registration failed",
            status=resp.status_code,
            body=resp.text,
            webhook_url=webhook_url,
        )
        raise RuntimeError(f"Lulu webhook registration failed: {resp.status_code} {resp.text}")

    data = resp.json()
    logger.info(
        "Lulu webhook registered successfully",
        webhook_id=data.get("id"),
        is_active=data.get("is_active"),
        url=data.get("url"),
    )
    return data


async def list_webhooks() -> list:
    """
    List all registered webhooks for the current Lulu account.

    Returns:
        List of webhook configurations with id, is_active, topics, url
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{settings.lulu_api_base}/webhooks/",
            headers=headers,
        )

    if resp.status_code != 200:
        logger.error("Failed to list Lulu webhooks", status=resp.status_code)
        raise RuntimeError(f"Failed to list webhooks: {resp.status_code}")

    data = resp.json()
    # Lulu returns paginated results
    return data.get("results", [])


async def delete_webhook(webhook_id: str) -> bool:
    """
    Delete a registered webhook.

    Args:
        webhook_id: UUID of the webhook to delete

    Returns:
        True if deleted successfully
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.delete(
            f"{settings.lulu_api_base}/webhooks/{webhook_id}/",
            headers=headers,
        )

    success = resp.status_code in (200, 204)
    if not success:
        logger.warning(
            "Lulu webhook deletion failed",
            status=resp.status_code,
            webhook_id=webhook_id,
        )
    return success


async def test_webhook(webhook_id: str) -> dict:
    """
    Send a test webhook from Lulu to verify the endpoint is working.

    Args:
        webhook_id: UUID of the webhook to test

    Returns:
        Test submission result
    """
    settings = get_settings()
    headers = await _lulu_headers()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/webhooks/{webhook_id}/test/",
            headers=headers,
        )

    if resp.status_code not in (200, 201):
        logger.error("Lulu webhook test failed", status=resp.status_code, webhook_id=webhook_id)
        raise RuntimeError(f"Webhook test failed: {resp.status_code}")

    return resp.json()


# ---------------------------------------------------------------------------
# Map Lulu status string → our LuluPrintStatus enum value
# ---------------------------------------------------------------------------

LULU_STATUS_MAP = {
    "CREATED": "submitted",
    "NEW": "submitted",           # Legacy status - kept for backwards compatibility
    "ACCEPTED": "accepted",       # Legacy status - kept for backwards compatibility
    "REJECTED": "rejected",
    "UNPAID": "pending",
    "PAYMENT_IN_PROGRESS": "pending",
    "PRODUCTION_DELAYED": "accepted",
    "PRODUCTION_READY": "accepted",
    "IN_PRODUCTION": "in_production",
    "SHIPPED": "shipped",
    "DELIVERED": "delivered",     # Not in official Lulu API but kept for internal use
    "CANCELED": "cancelled",      # Official Lulu spelling (American English)
    "CANCELLED": "cancelled",     # British spelling - kept for backwards compatibility
    "ERROR": "failed",
}


def map_lulu_status(lulu_status_name: str) -> str:
    """Convert raw Lulu status string to our LuluPrintStatus value."""
    return LULU_STATUS_MAP.get(lulu_status_name.upper(), "submitted")
