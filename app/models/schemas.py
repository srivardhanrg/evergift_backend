"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.enums import PreviewStatus, OrderStatus, JobStatus, JobType, BookStyle, Theme


# ==================
# Request Schemas
# ==================

class PhotoUploadRequest(BaseModel):
    """Request for uploading a child's photo."""
    session_id: Optional[str] = None


class PreviewCreateRequest(BaseModel):
    """Request to create a new preview."""
    photo_url: str = Field(..., description="URL of uploaded photo")
    child_name: str = Field(..., min_length=2, max_length=50)
    child_age: int = Field(..., ge=2, le=12)
    child_gender: str = Field(..., pattern="^(male|female)$")
    theme: Theme
    style: BookStyle = BookStyle.PHOTOREALISTIC
    session_id: Optional[str] = None
    customer_email: Optional[str] = None

    @validator("child_name")
    def validate_name(cls, v):
        """Validate name contains only letters and spaces."""
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError("Name must contain only letters and spaces")
        return v.strip()


# ==================
# Response Schemas
# ==================

class FaceValidationResult(BaseModel):
    """Result of face validation."""
    is_valid: bool
    face_count: int
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class PhotoUploadResponse(BaseModel):
    """Response after successful photo upload."""
    photo_id: str
    photo_url: str
    face_valid: bool
    face_count: int


class JobStartResponse(BaseModel):
    """Response when a background job is started."""
    job_id: str
    preview_id: str
    status: JobStatus
    estimated_time_seconds: int
    message: str


class JobStatusResponse(BaseModel):
    """Response for job status polling."""
    job_id: str
    status: JobStatus
    progress: int = Field(..., ge=0, le=100)
    current_step: Optional[str] = None
    preview_id: Optional[str] = None
    redirect_url: Optional[str] = None
    error: Optional[str] = None
    can_retry: bool = False


class GenerationProgressResponse(BaseModel):
    """
    Enhanced generation progress response for 26-page structure.

    Provides detailed page-level progress for the frontend's
    generating state animation and progress display.
    """
    job_id: str
    status: JobStatus
    progress: int = Field(..., ge=0, le=100, description="Overall progress percentage")
    preview_id: Optional[str] = None

    # Page-level progress
    current_phase: str = Field(
        "initializing",
        description="Phase: 'initializing', 'analyzing_face', 'generating_cover', 'generating_pages', 'processing_fillers', 'complete'"
    )
    current_page_index: Optional[int] = Field(
        None,
        description="Index of page currently being generated (0-22)"
    )
    current_page_type: Optional[str] = Field(
        None,
        description="Type of current page: 'cover', 'generated'"
    )
    pages_completed: List[int] = Field(
        default_factory=list,
        description="List of page indices that are complete"
    )
    total_ai_pages_in_phase: int = Field(
        6,
        description="Total AI pages to generate in current phase (6 for preview, 5 for post-payment)"
    )
    ai_pages_completed: int = Field(
        0,
        description="Number of AI pages completed in current phase"
    )

    # Filler status
    filler_pages_processed: bool = Field(
        False,
        description="True when all filler pages are processed"
    )

    # Display helpers
    step_description: str = Field(
        "Preparing your magical story...",
        description="Human-readable description of current step"
    )
    estimated_seconds_remaining: Optional[int] = Field(
        None,
        description="Estimated seconds until completion"
    )

    # Completion
    redirect_url: Optional[str] = None
    error: Optional[str] = None
    can_retry: bool = False


class PageData(BaseModel):
    """Data for a single storybook page."""
    page_number: int
    image_url: str
    story_text: str
    is_watermarked: bool = False
    is_locked: bool = False
    is_cover: bool = False  # True for cover page (page 0)
    # Optional fields for StoryGift compatibility
    dialogue: Optional[List[dict]] = None  # For dialogue data
    realistic_prompt: Optional[str] = None  # For generation metadata
    generation_metadata: Optional[dict] = None  # For analytics


# ==================
# 26-Page Book Structure Schemas
# ==================

class PageTypeEnum(str):
    """Page types in the 26-page storybook structure."""
    COVER = "cover"
    DEDICATION = "dedication"
    INTRO = "intro"
    GENERATED = "generated"
    TEXT = "text"
    END_PAGE = "end_page"
    BACK_COVER = "back_cover"


class BookPageInfo(BaseModel):
    """
    Information about a single page in the 26-page book structure.

    Used for frontend rendering with proper page states.
    """
    index: int = Field(..., ge=0, le=25, description="Page index (0-25)")
    page_type: str = Field(..., description="Type of page: cover, dedication, intro, generated, text, end_page, back_cover")
    image_url: Optional[str] = Field(None, description="URL of the page image (None if not yet generated)")
    story_text: Optional[str] = Field(None, description="Story text for text pages")
    is_preview: bool = Field(..., description="True if visible in preview (pages 0-13)")
    is_locked: bool = Field(..., description="True if locked until purchase (pages 14-25)")
    is_filler: bool = Field(False, description="True if this is a filler page (not AI-generated)")
    is_generating: bool = Field(False, description="True if currently being AI-generated")
    is_generated: bool = Field(False, description="True if AI generation is complete")
    requires_text_overlay: bool = Field(False, description="True if page needs text overlay")
    text_page_number: Optional[int] = Field(None, description="For text pages, which text page (1-10)")


class BookStructureResponse(BaseModel):
    """
    Complete 26-page book structure for the frontend.

    Contains all page metadata for rendering the book viewer
    with proper states (generating, locked, available).
    """
    total_pages: int = Field(26, description="Total pages in the book")
    preview_boundary: int = Field(12, description="Last page index visible in preview (0-12 = 13 pages)")
    preview_page_count: int = Field(13, description="Number of pages visible in preview")
    locked_page_count: int = Field(13, description="Number of locked pages (13-25)")
    pages: List[BookPageInfo] = Field(..., description="All 26 pages with their current state")

    # Generation progress tracking
    generation_progress: int = Field(0, ge=0, le=100, description="Overall generation progress percentage")
    current_generating_page: Optional[int] = Field(None, description="Index of page currently being generated")
    pages_generated: int = Field(0, description="Number of AI pages generated so far")
    total_ai_pages: int = Field(11, description="Total AI-generated pages (cover + 10 story)")

    # Filler page processing
    filler_pages_ready: bool = Field(False, description="True if all filler pages are processed")


class PreviewResponseV2(BaseModel):
    """
    Enhanced preview response with 26-page book structure.

    This is the V2 response format that includes the complete
    book structure with page-level state tracking.
    """
    preview_id: str
    status: PreviewStatus
    generation_phase: str = Field(
        "preview",
        description="Generation phase: 'preview', 'generating_full', 'complete'"
    )

    # Story metadata
    story_title: str
    child_name: str
    theme: str
    style: str

    # Book structure
    book_structure: BookStructureResponse = Field(
        ...,
        description="Complete 26-page book structure with page states"
    )

    # Legacy compatibility fields
    cover_url: Optional[str] = None
    preview_pages: List[PageData] = Field(
        default_factory=list,
        description="Legacy: Preview pages for backward compatibility"
    )
    locked_pages: Optional[List[PageData]] = Field(
        None,
        description="Legacy: Locked pages for backward compatibility"
    )
    total_pages: int = Field(26, description="Total pages in book")
    preview_pages_count: int = Field(13, description="Pages visible in preview")
    locked_pages_count: int = Field(13, description="Pages locked until purchase")

    # Expiration
    expires_at: datetime
    days_remaining: int

    # Purchase info
    purchase: dict

    # PDF (available after payment + full generation)
    pdf_url: Optional[str] = None

    # Metadata
    testing_mode: Optional[bool] = None
    analyzed_features: Optional[str] = None
    generation_model: Optional[str] = None


class PreviewResponse(BaseModel):
    """Complete preview data for display."""
    preview_id: str
    status: PreviewStatus
    generation_phase: str = "preview"  # 'preview', 'generating_full', 'complete'
    story_title: str
    child_name: str
    theme: str  # Changed from Theme to str for flexibility
    style: str  # Changed from BookStyle to str for flexibility
    cover_url: Optional[str] = None  # Dedicated cover image URL
    preview_pages: List[PageData]
    locked_pages: Optional[List[PageData]] = None
    total_pages: int  # Now 11 (1 cover + 10 story pages)
    preview_pages_count: int
    locked_pages_count: int
    expires_at: datetime
    days_remaining: int
    purchase: dict
    # PDF URL - only available after payment and remaining page generation
    pdf_url: Optional[str] = None
    # Optional fields for StoryGift features
    testing_mode: Optional[bool] = None  # Indicates if generated in testing mode
    analyzed_features: Optional[str] = None  # VLM face analysis result
    generation_model: Optional[str] = None  # Model used (e.g., "nano_banana")


class DownloadInfo(BaseModel):
    """Download information for a file."""
    url: str
    filename: str
    size_mb: Optional[float] = None
    expires_in_seconds: int


class DownloadResponse(BaseModel):
    """Response with download links."""
    status: str
    downloads: Optional[dict] = None
    progress: Optional[int] = None
    message: Optional[str] = None
    expires_at: Optional[datetime] = None
    days_remaining: Optional[int] = None


# ==================
# Database Models (for type hints)
# ==================

class PreviewRecord(BaseModel):
    """Preview record from database."""
    id: int
    preview_id: UUID
    session_id: Optional[str]
    customer_id: Optional[str]
    customer_email: Optional[str]
    child_name: str
    child_age: int
    child_gender: str
    theme: str
    style: str
    photo_url: str
    photo_validated: bool
    status: str
    hires_images: List[dict]
    preview_images: List[dict]
    story_pages: List[dict]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class OrderRecord(BaseModel):
    """Order record from database."""
    id: int
    order_id: str
    order_number: Optional[str]
    preview_id: UUID
    customer_email: str
    customer_name: Optional[str]
    status: str
    pdf_url: Optional[str]
    pdf_generated_at: Optional[datetime]
    shipping_address: Optional[dict]
    tracking_number: Optional[str]
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    expires_at: datetime

    class Config:
        from_attributes = True


class GenerationJobRecord(BaseModel):
    """Generation job record from database."""
    id: int
    job_id: UUID
    job_type: str
    reference_id: str
    status: str
    progress: int
    queued_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    attempts: int
    max_attempts: int
    error_message: Optional[str]
    result_data: Optional[dict]

    class Config:
        from_attributes = True


# ==================
# Error Response
# ==================

class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: dict = Field(..., description="Error details")


class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    data: dict
