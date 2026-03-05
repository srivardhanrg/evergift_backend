"""
Security utilities for webhook verification and signed URLs.
"""

import hmac
import hashlib
import base64
from fastapi import Request, HTTPException
import structlog

logger = structlog.get_logger()


async def verify_shopify_webhook(request: Request, secret: str) -> bytes:
    """
    Verify Shopify webhook HMAC signature and return verified body.

    CRITICAL: Returns the verified body bytes for safe parsing.
    This prevents race conditions from reading the body twice.
    
    Returns:
        bytes: The verified webhook body for parsing
        
    Raises:
        HTTPException: If HMAC verification fails
    """
    try:
        # Get signature from header
        shopify_hmac = request.headers.get("X-Shopify-Hmac-Sha256")
        if not shopify_hmac:
            logger.warning("Missing HMAC signature in webhook")
            raise HTTPException(status_code=401, detail="Missing HMAC signature")

        # Get raw body - read once and return for parsing
        body = await request.body()

        # Compute expected signature
        computed_hmac = base64.b64encode(
            hmac.new(
                secret.encode("utf-8"),
                body,
                hashlib.sha256
            ).digest()
        ).decode("utf-8")

        # Compare signatures using timing-safe comparison
        if not hmac.compare_digest(computed_hmac, shopify_hmac):
            logger.warning("Invalid HMAC signature in webhook")
            raise HTTPException(status_code=401, detail="Invalid HMAC signature")

        logger.info("Webhook HMAC signature verified")
        return body  # Return verified body for safe parsing

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Webhook verification failed", error=str(e))
        raise HTTPException(status_code=500, detail="Webhook verification failed")


def verify_shop_domain(request: Request, expected_domain: str) -> bool:
    """Verify webhook came from expected shop.

    Supports multiple domains via comma-separated list in expected_domain.
    Example: "storygift-2061.myshopify.com,w8vbed-6m.myshopify.com"

    In development, this only logs a warning but allows the request.
    In production, this raises an exception on mismatch.
    """
    from app.config import get_settings
    settings = get_settings()

    shop_domain = request.headers.get("X-Shopify-Shop-Domain")

    # Support comma-separated list of allowed domains
    allowed_domains = [d.strip() for d in expected_domain.split(",") if d.strip()]

    if shop_domain in allowed_domains:
        logger.info("Shop domain verified", received=shop_domain)
        return True

    logger.warning("Shop domain mismatch", received=shop_domain, allowed=allowed_domains)

    # In development, allow the request (for test webhooks)
    if settings.app_env == "development":
        logger.info("Allowing mismatched domain in development mode")
        return True

    # In production, reject the request
    raise HTTPException(status_code=401, detail="Invalid shop domain")