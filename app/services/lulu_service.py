"""
Lulu Print API Service

Handles OAuth2 authentication and all Lulu API interactions:
- Token management (auto-refresh)
- Cost calculations
- Print job creation
- Status polling
- Shipping options
"""

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
) -> dict:
    """
    Calculate the cost of a Lulu print job before ordering.

    Returns a dict with:
        total_cost_incl_tax, print_cost, shipping_cost, currency
    """
    settings = get_settings()
    headers = await _lulu_headers()

    payload = {
        "line_items": [
            {
                "page_count": 12,           # 10 story pages + cover + back = padded to 12
                "pod_package_id": settings.lulu_pod_package_id,
                "quantity": quantity,
                "title": "MagicTales Storybook",
                "cover": {"source_url": cover_url},
                "interior": {"source_url": interior_url},
            }
        ],
        "shipping_address": {
            "country": country_code,
        },
        "shipping_option": shipping_option,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/print-job-cost-calculations/",
            json=payload,
            headers=headers,
        )

    if resp.status_code not in (200, 201):
        logger.error("Lulu cost calculation failed", status=resp.status_code, body=resp.text)
        raise RuntimeError(f"Lulu cost calc failed: {resp.status_code} {resp.text}")

    data = resp.json()
    logger.info("Lulu cost calculated", data=data)
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
) -> dict:
    """
    Create a Lulu print job.

    shipping_address must contain:
        name, street1, city, state_code, country_code, postcode, phone_number

    Returns the full Lulu API response (contains id, status, etc.)
    """
    settings = get_settings()
    headers = await _lulu_headers()

    payload = {
        # contact_email is for Lulu to contact about print issues, NOT customer email
        "contact_email": "support@storygift.in",
        "line_items": [
            {
                "title": f"{child_name}'s MagicTales Storybook",
                "cover": {
                    "source_url": cover_url,
                },
                "interior": {
                    "source_url": interior_url,
                },
                "pod_package_id": settings.lulu_pod_package_id,
                "quantity": quantity,
                "page_count": 12,
            }
        ],
        "production_delay": 0,
        "shipping_address": {
            "name": shipping_address.get("name", ""),
            "street1": shipping_address.get("street1", ""),
            "street2": shipping_address.get("street2", ""),
            "city": shipping_address.get("city", ""),
            "state_code": shipping_address.get("state_code", ""),
            "country_code": shipping_address.get("country_code", "IN"),
            "postcode": shipping_address.get("postcode", ""),
            "phone_number": shipping_address.get("phone_number", ""),
        },
        "shipping_option": shipping_option,
        "external_id": order_id,  # Our order reference
    }

    # Add webhook configuration at the root of the payload
    # Lulu requires us to set the webhook URL per print job
    if settings.app_env in ["production", "staging"]:
        webhook_url = f"https://magictales-backend.onrender.com/webhooks/lulu/lulu"
        # For testing, you could also configure this via env vars:
        # webhook_url = settings.lulu_webhook_url
        payload["event_notifications"] = [
            {
                "url": webhook_url,
                "events": ["PRINT_JOB_STATUS_CHANGED"]
            }
        ]
    elif os.getenv("LULU_WEBHOOK_URL"): # For local testing with Ngrok/Cloudflare
        payload["event_notifications"] = [
            {
                "url": os.getenv("LULU_WEBHOOK_URL"),
                "events": ["PRINT_JOB_STATUS_CHANGED"]
            }
        ]

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.lulu_api_base}/print-jobs/",
            json=payload,
            headers=headers,
        )

    if resp.status_code not in (200, 201):
        logger.error(
            "Lulu print job creation failed",
            status=resp.status_code,
            body=resp.text,
            order_id=order_id,
        )
        raise RuntimeError(f"Lulu print job failed: {resp.status_code} {resp.text}")

    data = resp.json()
    logger.info(
        "Lulu print job created",
        lulu_job_id=data.get("id"),
        status=data.get("status", {}).get("name"),
        order_id=order_id,
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
) -> list:
    """
    Get available shipping options and their costs for a destination.
    """
    settings = get_settings()
    headers = await _lulu_headers()

    payload = {
        "line_items": [
            {
                "page_count": 12,
                "pod_package_id": settings.lulu_pod_package_id,
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
# Map Lulu status string → our LuluPrintStatus enum value
# ---------------------------------------------------------------------------

LULU_STATUS_MAP = {
    "CREATED": "submitted",
    "NEW": "submitted",
    "ACCEPTED": "accepted",
    "REJECTED": "rejected",
    "UNPAID": "pending",
    "PAYMENT_IN_PROGRESS": "pending",
    "PRODUCTION_DELAYED": "accepted",
    "PRODUCTION_READY": "accepted",
    "IN_PRODUCTION": "in_production",
    "SHIPPED": "shipped",
    "DELIVERED": "delivered",
    "CANCELLED": "cancelled",
    "ERROR": "failed",
}


def map_lulu_status(lulu_status_name: str) -> str:
    """Convert raw Lulu status string to our LuluPrintStatus value."""
    return LULU_STATUS_MAP.get(lulu_status_name.upper(), "submitted")
