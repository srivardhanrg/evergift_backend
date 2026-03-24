"""
Feedback endpoint for collecting user feedback.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import Optional
import structlog

from app.models.database import get_db

logger = structlog.get_logger()
router = APIRouter()


class FeedbackRequest(BaseModel):
    star_rating: Optional[int] = None
    feedback_text: Optional[str] = None
    name: Optional[str] = None

    @validator("star_rating")
    def validate_star_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError("star_rating must be between 1 and 5")
        return v

    @validator("feedback_text")
    def validate_feedback_text(cls, v, values):
        # This runs after star_rating validator, so we can check both
        if v is None and values.get("star_rating") is None:
            raise ValueError("At least one of star_rating or feedback_text must be provided")
        return v


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback with an optional star rating and/or text.

    At least one of star_rating or feedback_text must be provided.
    """
    logger.info(
        "Feedback submission received",
        has_rating=request.star_rating is not None,
        has_text=request.feedback_text is not None,
        has_name=request.name is not None,
    )

    try:
        db = get_db()

        insert_data = {}
        if request.star_rating is not None:
            insert_data["star_rating"] = request.star_rating
        if request.feedback_text is not None:
            insert_data["feedback_text"] = request.feedback_text
        if request.name is not None:
            insert_data["name"] = request.name

        result = db.table("feedback").insert(insert_data).execute()

        logger.info("Feedback stored successfully", feedback_id=result.data[0]["id"] if result.data else None)

        return {"success": True, "message": "Thank you for your feedback!"}

    except Exception as e:
        logger.error("Failed to store feedback", error=str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "code": "FEEDBACK_STORAGE_ERROR",
                "message": "Failed to store feedback. Please try again later.",
            },
        )
