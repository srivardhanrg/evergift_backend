"""
Enums for database status fields.
"""

from enum import Enum


class PreviewStatus(str, Enum):
    """Preview generation and lifecycle status."""
    PENDING = "pending"
    VALIDATING = "validating"
    GENERATING = "generating"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    PURCHASED = "purchased"


class OrderStatus(str, Enum):
    """Order processing status."""
    PAID = "paid"
    GENERATING_PDF = "generating_pdf"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class JobStatus(str, Enum):
    """Background job status."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(str, Enum):
    """Type of background job."""
    PREVIEW_GENERATION = "preview_generation"
    PDF_CREATION = "pdf_creation"


class BookStyle(str, Enum):
    """Storybook visual style. Currently photorealistic only."""
    PHOTOREALISTIC = "photorealistic"
    # CARTOON_3D = "cartoon_3d"  # Removed - pipeline code preserved but not exposed


class LuluPrintStatus(str, Enum):
    """Status of a Lulu print order."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"


class GenerationPhase(str, Enum):
    """
    Generation phase for preview/order lifecycle.

    Digital order flow:
        preview → generating_full → pages_complete → complete

    Physical order flow:
        preview → generating_full → pages_complete → preparing_print
        → submitting_print → print_submitted

    Error states:
        pdf_failed - PDF generation failed (pages preserved, can retry)
        print_failed - Lulu submission failed (PDF ready, can retry)
        failed - Unrecoverable error
    """
    # Initial state
    PREVIEW = "preview"

    # Digital + Physical: Generating remaining pages (6-10)
    GENERATING_FULL = "generating_full"

    # Digital + Physical: All pages generated, creating PDF
    PAGES_COMPLETE = "pages_complete"

    # Digital only: PDF ready, order complete
    COMPLETE = "complete"

    # Physical only: Creating Lulu-specific PDFs (interior + cover wrap)
    PREPARING_PRINT = "preparing_print"

    # Physical only: Calling Lulu API to submit print job
    SUBMITTING_PRINT = "submitting_print"

    # Physical only: Lulu accepted the job, book is being printed
    PRINT_SUBMITTED = "print_submitted"

    # Error states
    PDF_FAILED = "pdf_failed"
    PRINT_FAILED = "print_failed"
    FAILED = "failed"


class Theme(str, Enum):
    """Available story themes."""
    # Primary StoryGift themes (superior quality, 10 pages each)
    STORYGIFT_MAGIC_CASTLE = "storygift_magic_castle"
    STORYGIFT_ENCHANTED_FOREST = "storygift_enchanted_forest"
    # STORYGIFT_SPY_MISSION = "storygift_spy_mission"  # REMOVED
    # New premium themes
    STORYGIFT_COSMIC_DREAMER = "storygift_cosmic_dreamer"
    STORYGIFT_MIGHTY_GUARDIAN = "storygift_mighty_guardian"
    STORYGIFT_OCEAN_EXPLORER = "storygift_ocean_explorer"
    STORYGIFT_BIRTHDAY_MAGIC = "storygift_birthday_magic"
    # Newest premium themes (Safari & Dream Weaver)
    STORYGIFT_SAFARI_ADVENTURE = "storygift_safari_adventure"
    # STORYGIFT_DREAM_WEAVER = "storygift_dream_weaver"  # REMOVED
    STORYGIFT_SECRET_AGENT = "storygift_secret_agent"

    # Legacy themes (for backward compatibility)
    MAGIC_CASTLE = "magic_castle"
    SPACE_ADVENTURE = "space_adventure"
    UNDERWATER = "underwater"
    FOREST_FRIENDS = "forest_friends"

