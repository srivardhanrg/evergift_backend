"""
Health check endpoint with database verification.
"""

from fastapi import APIRouter
from datetime import datetime
import structlog
import os

from app.models.database import get_db
from app.config.text_styling import FONT_PATHS

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint with database verification.

    Returns:
        - status: "healthy" if all systems operational, "degraded" if DB issues
        - database: "connected" or "disconnected"
        - timestamp: Current UTC timestamp
    """
    db_status = "disconnected"

    try:
        db = get_db()
        # Simple query to verify database connection
        result = db.table("previews").select("preview_id").limit(1).execute()
        if result.error:
            db_status = "error"
        else:
            db_status = "connected"
    except Exception as e:
        logger.warning("Health check database connection failed", error=str(e))
        db_status = "disconnected"

    overall_status = "healthy" if db_status == "connected" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "zelavo-kids-backend"
    }


@router.get("/health/fonts")
async def font_health_check():
    """
    Check if font files are accessible.

    Returns:
        - fonts_loaded: Count of accessible fonts
        - fonts_missing: Count of missing fonts
        - details: Status of each font file
    """
    font_status = {}
    fonts_loaded = 0
    fonts_missing = 0

    for font_name, font_path in FONT_PATHS.items():
        if font_path is None:
            # System font - not checked
            font_status[font_name] = {"status": "system_font", "path": "system"}
            continue

        if os.path.exists(font_path):
            fonts_loaded += 1
            font_status[font_name] = {"status": "ok", "path": font_path}
        else:
            fonts_missing += 1
            font_status[font_name] = {"status": "missing", "path": font_path}

    overall_status = "healthy" if fonts_missing == 0 else "degraded"

    return {
        "status": overall_status,
        "fonts_loaded": fonts_loaded,
        "fonts_missing": fonts_missing,
        "details": font_status,
        "timestamp": datetime.utcnow().isoformat()
    }
