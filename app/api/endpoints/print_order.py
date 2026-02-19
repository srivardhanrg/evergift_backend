"""
Print Order API Endpoints

Exposes Lulu print functionality via REST API:
  GET  /api/print/cost-estimate  - Estimate print + shipping cost
  POST /api/print/order          - Manually trigger a print job
  GET  /api/print/status/{id}    - Get print order status
  GET  /api/print/shipping-options - Available shipping options
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import structlog

from app.config import get_settings
from app.models.database import get_db
from app.services.lulu_service import (
    calculate_print_cost,
    get_shipping_options,
    get_print_job,
    get_print_job_status,
)

logger = structlog.get_logger()
router = APIRouter(prefix="/print")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class PrintOrderRequest(BaseModel):
    order_id: str
    shipping_option: str = "MAIL"


# ---------------------------------------------------------------------------
# GET /api/print/shipping-options
# ---------------------------------------------------------------------------

@router.get("/shipping-options")
async def list_shipping_options(
    country_code: str = Query(default="IN", description="ISO 3166-1 alpha-2 country code"),
    state_code: Optional[str] = Query(default=None),
):
    """
    Return available shipping options and prices for a destination country.
    Useful for letting customer pick shipping tier at checkout.
    """
    try:
        options = await get_shipping_options(country_code, state_code)
        return {"success": True, "shipping_options": options}
    except Exception as e:
        logger.error("Failed to fetch shipping options", error=str(e))
        raise HTTPException(status_code=502, detail=f"Could not retrieve shipping options: {str(e)}")


# ---------------------------------------------------------------------------
# GET /api/print/cost-estimate
# ---------------------------------------------------------------------------

@router.get("/cost-estimate")
async def cost_estimate(
    preview_id: str = Query(..., description="Preview ID to estimate cost for"),
    country_code: str = Query(default="IN"),
    shipping_option: str = Query(default="MAIL"),
):
    """
    Return estimated Lulu print + shipping cost for a preview.
    Requires interior and cover PDFs to already exist (i.e. after payment).
    """
    db = get_db()
    try:
        # Look up print_order for this preview_id to get PDF URLs
        result = db.table("print_orders").select("interior_pdf_url,cover_pdf_url").eq(
            "preview_id", preview_id
        ).execute()

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="No print order found for this preview. Has payment been completed?"
            )

        row = result.data[0]
        interior_url = row.get("interior_pdf_url")
        cover_url = row.get("cover_pdf_url")

        if not interior_url or not cover_url:
            raise HTTPException(status_code=400, detail="Print PDFs not yet generated for this order.")

        cost_data = await calculate_print_cost(
            interior_url=interior_url,
            cover_url=cover_url,
            shipping_option=shipping_option,
            country_code=country_code,
        )

        return {"success": True, "cost": cost_data}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Cost estimate failed", error=str(e), preview_id=preview_id)
        raise HTTPException(status_code=502, detail=str(e))


# ---------------------------------------------------------------------------
# GET /api/print/status/{print_order_id}
# ---------------------------------------------------------------------------

@router.get("/status/{print_order_id}")
async def get_print_status(print_order_id: str):
    """
    Get the current status of a print order.
    Returns our internal record + latest Lulu status if a job was submitted.
    """
    db = get_db()
    result = db.table("print_orders").select("*").eq("print_order_id", print_order_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Print order not found")

    record = result.data[0]
    lulu_job_id = record.get("lulu_print_job_id")

    # If submitted to Lulu, fetch live status
    live_status = None
    if lulu_job_id:
        try:
            live_status = await get_print_job_status(lulu_job_id)
        except Exception as e:
            logger.warning("Could not fetch live Lulu status", error=str(e), lulu_job_id=lulu_job_id)

    return {
        "success": True,
        "print_order": record,
        "lulu_live_status": live_status,
    }


# ---------------------------------------------------------------------------
# GET /api/print/by-order/{order_id}
# ---------------------------------------------------------------------------

@router.get("/by-order/{order_id}")
async def get_print_by_order(order_id: str):
    """Get print order status by Shopify order ID."""
    db = get_db()
    result = db.table("print_orders").select("*").eq("order_id", order_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="No print order found for this order")

    return {"success": True, "print_order": result.data[0]}


# ---------------------------------------------------------------------------
# GET /api/print/by-preview/{preview_id}
# ---------------------------------------------------------------------------

@router.get("/by-preview/{preview_id}")
async def get_print_by_preview(preview_id: str):
    """Get print order status by preview ID (used by frontend preview page)."""
    db = get_db()
    result = db.table("print_orders").select(
        "print_order_id,order_id,preview_id,lulu_status,tracking_number,estimated_delivery,shipped_at,delivered_at,created_at"
    ).eq("preview_id", preview_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="No print order found for this preview")

    return {"success": True, "print_order": result.data[0]}
