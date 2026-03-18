"""
Main API router that combines all endpoints.
"""

from fastapi import APIRouter

from app.api.endpoints import upload, preview, status, download, health, my_creations, print_order
from app.api.webhooks import shopify, lulu
from app.config import get_settings

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])  # Health check also under /api/
api_router.include_router(upload.router, tags=["upload"])
api_router.include_router(preview.router, tags=["preview"])  # No prefix - routes already have /preview
api_router.include_router(status.router, tags=["status"])
api_router.include_router(download.router, tags=["download"])
api_router.include_router(my_creations.router, tags=["my-creations"])
api_router.include_router(print_order.router, tags=["print"])

# Development & Test endpoints - ONLY in development/testing mode
# Set TESTING_MODE_ENABLED=true in .env for local development
settings = get_settings()
if settings.testing_mode_enabled or settings.app_env in ["development", "local", "testing"]:
    from app.api.endpoints import development, dev_tools
    api_router.include_router(development.router, tags=["development"])
    api_router.include_router(dev_tools.router, tags=["dev-tools"])

    from app.api.endpoints import test_shopify
    api_router.include_router(test_shopify.router, tags=["test"])

# Health check (no prefix)
health_router = APIRouter()
health_router.include_router(health.router, tags=["health"])

# Webhook router
webhook_router = APIRouter()
webhook_router.include_router(shopify.router, prefix="/shopify", tags=["webhooks"])
webhook_router.include_router(lulu.router, prefix="/lulu", tags=["webhooks"])