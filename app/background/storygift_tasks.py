"""
StoryGift-style background tasks for image generation and PDF creation.

Using:
- Photorealistic pipeline with identity-preserving image reference
- Static identity lock prompt (VLM disabled - see photorealistic_pipeline.py)
- 26-page book structure with filler pages and text overlays
- StoryGift themes with cover + 10 AI-generated story pages + filler pages
- Superior PDF generation

Book Structure (26 pages):
- Index 0: Cover (AI-generated)
- Index 1: Dedication (filler + text overlay)
- Indices 2-3: Intro pages (filler, no text)
- Indices 4, 6, 8, 10, 12: AI-generated story pages (preview)
- Indices 5, 7, 9, 11: Text pages with story text overlay (preview)
- Indices 14, 16, 18, 20, 22: AI-generated story pages (locked)
- Indices 13, 15, 17, 19, 21, 23: Text pages with story text overlay (locked)
- Index 24: End page (filler)
- Index 25: Back cover (filler)

Preview shows pages 0-13 (14 pages)
Locked pages are 14-25 (12 pages until payment)
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import structlog
from uuid import UUID

from app.config import get_settings
from app.models.database import get_db
from app.models.enums import PreviewStatus, OrderStatus, JobStatus
from app.services.storage import StorageService
from app.services.email_service import get_email_service
from app.services.filler_pages import get_filler_pages_service
from app.services.image_processor import get_image_processor
from app.stories.themes import get_theme
from app.ai.factory import get_pipeline_for_style
from app.core.exceptions import ImageGenerationError, StorageError
from app.core.sanitization import sanitize_child_name, sanitize_for_prompt
from app.config.book_structure import (
    BOOK_STRUCTURE,
    PageType,
    PREVIEW_AI_INDICES,
    LOCKED_AI_INDICES,
    AI_GENERATED_INDICES,
    TOTAL_PAGE_COUNT,
    PREVIEW_PAGE_COUNT,
    get_page_config,
)

# Import helper functions from utils (not tasks) to avoid circular import
from app.background.utils import (
    update_job_progress,
    update_job_status,
    update_preview_status,
    create_watermarked_preview
    # update_preview_pages_incrementally removed - V1 columns don't exist
)

logger = structlog.get_logger()

# Story-themed progress messages for each generation phase
PROGRESS_MESSAGES = {
    "face_analysis": [
        "Discovering your hero's magical features... ✨",
        "Reading the sparkle in their eyes... 👀",
        "Learning what makes them special... 🌟",
    ],
    "cover": [
        "Designing your magical book cover... 📚",
        "Painting the entrance to adventure... 🎨",
        "Creating the perfect first impression... ✨",
    ],
    "page_1": [
        "Opening the enchanted storybook... 📖",
        "Your hero is waking up to adventure! 🌅",
        "Chapter 1 is brewing with magic... ☕",
    ],
    "page_2": [
        "The adventure begins! 🚀",
        "Magic sparkles fill the air... ✨",
        "New discoveries await around every corner... 🔮",
    ],
    "page_3": [
        "Meeting wonderful new friends! 🤝",
        "The story grows more exciting... 🎭",
        "Courage is building in your hero's heart... 💪",
    ],
    "page_4": [
        "Plot twist incoming! 🎢",
        "The adventure reaches new heights... 🏔️",
        "Magic swirls all around... 🌀",
    ],
    "page_5": [
        "Creating a magical moment! 🌈",
        "Almost at the grand finale... 🎆",
        "Wrapping up this chapter beautifully... 🎁",
    ],
    "finalizing": [
        "Sprinkling final fairy dust... ✨",
        "Putting the finishing touches... 🖌️",
        "Your magical story is almost ready! 🎉",
    ],
}

def get_progress_message(phase: str, page_num: int = None) -> str:
    """Get a themed progress message for the current generation phase."""
    import random

    if page_num is not None:
        # Use page-specific message if available
        page_key = f"page_{page_num}"
        if page_key in PROGRESS_MESSAGES:
            return random.choice(PROGRESS_MESSAGES[page_key])

    # Fall back to phase-based message
    if phase in PROGRESS_MESSAGES:
        return random.choice(PROGRESS_MESSAGES[phase])

    # Default fallback
    return "Creating magic... ✨"


async def generate_storygift_preview(
    job_id: str,
    preview_id: str,
    photo_urls: List[str],  # Changed from single photo_url to multiple photo_urls
    child_name: str,
    child_age: int,
    child_gender: str,
    theme: str
):
    """
    Generate StoryGift-style preview with photorealistic pipeline.

    Uses photorealistic pipeline with VLM face analysis.
    Supports testing mode (5 pages) vs production mode (10 pages).

    Note: Cartoon pipeline code preserved but not exposed in API.
    """
    # Hardcoded to photorealistic - cartoon pipeline preserved but not exposed
    style = "photorealistic"

    try:
        # PREVIEW MODE: Always generate 5 pages first (remaining 5 after payment)
        preview_pages = 5
        total_pages = 10  # Total pages in full book

        # Sanitize child name to prevent prompt injection
        safe_child_name = sanitize_child_name(child_name)

        logger.info(
            "Starting StoryGift preview generation (5-page preview mode)",
            preview_id=preview_id,
            child_name=safe_child_name,
            original_name_length=len(child_name),
            theme=theme,
            style=style,
            preview_pages=preview_pages,
            total_pages=total_pages
        )

        await update_job_status(job_id, JobStatus.PROCESSING, progress=0)
        await update_job_progress(job_id, 0, "Preparing your magical adventure... 🎭")

        # Get StoryGift theme
        try:
            template = get_theme(theme)
            logger.info("StoryGift template loaded", theme=theme, page_count=len(template.pages))
        except Exception as e:
            logger.error("Failed to load StoryGift theme", theme=theme, error=str(e))
            raise

        # Initialize appropriate pipeline based on style
        try:
            pipeline = get_pipeline_for_style(style)
            logger.info(f"Pipeline initialized for style: {style}", style=style)
        except Exception as e:
            logger.error(f"Failed to initialize pipeline for style {style}", error=str(e))
            raise

        # Prepare story pages for generation (ONLY first 5 for preview)
        pages_to_generate = template.pages[:preview_pages]
        logger.info(f"Generating {len(pages_to_generate)} preview pages (full book has {len(template.pages)} pages)")

        # ============================================
        # PHASE 1: Identity Lock Prompt (5% progress)
        # VLM DISABLED - nano-banana extracts identity from image reference
        # ============================================
        await update_job_progress(job_id, 5, get_progress_message("face_analysis"))

        # VLM ANALYSIS DISABLED (2024-01)
        # Research: nano-banana extracts identity directly from image reference,
        # text descriptions can conflict with image data and reduce quality.
        # Using static identity lock prompt instead.
        #
        # try:
        #     analyzed_features = await pipeline.analyze_face(photo_url)
        #     logger.info("Face analysis completed", features_length=len(analyzed_features))
        # except Exception as e:
        #     logger.error("Face analysis failed", error=str(e))
        #     analyzed_features = "a cute child"

        analyzed_features = "the child exactly as shown in the reference photo, preserving all facial features, skin tone, hair texture, and ethnic characteristics with perfect accuracy"
        logger.info("Using static identity lock prompt (VLM disabled)")

        # Store analyzed_features for consistency when generating remaining pages (6-10)
        db = get_db()
        db.table("previews").update({
            "analyzed_features": analyzed_features
        }).eq("preview_id", preview_id).execute()
        logger.info("Stored identity lock prompt for future generation consistency")

        # Initialize incremental book_structure dict for progressive updates
        # This will grow as each page completes, enabling frontend to show pages one-by-one
        book_structure_incremental = {}

        # ============================================
        # PHASE 1.5: Generate Cover Image (10% progress)
        # ============================================
        await update_job_progress(job_id, 10, get_progress_message("cover"))

        cover_url = None
        try:
            # Get cover prompt from template (using sanitized name, age, gender)
            # Always uses photorealistic style
            cover_prompt = template.get_cover_prompt(safe_child_name, child_age, child_gender)
            logger.info(
                "Generating cover image with face-preserving pipeline",
                preview_id=preview_id,
                style=style,
                child_age=child_age,
                child_gender=child_gender,
                prompt_length=len(cover_prompt),
                prompt_preview=cover_prompt[:200]  # First 200 chars for debugging
            )

            # Generate cover using same face analysis pipeline for consistency
            # Cover uses 1:1 aspect ratio to perfectly fit PDF page (10x10 inches)
            cover_result = await pipeline.generate_with_face_analysis(
                prompt=cover_prompt,
                face_url=photo_urls,  # Pass all photo URLs
                child_name=safe_child_name,
                child_age=child_age,
                child_gender=child_gender,
                analyzed_features=analyzed_features,
                aspect_ratio="1:1",  # Square format for all pages
                scene_type="cover",
                preview_id=preview_id,
                page_number=0  # Cover is page 0
            )

            logger.info(
                "Cover generation result",
                preview_id=preview_id,
                success=cover_result.success,
                has_image_url=bool(cover_result.image_url),
                error_message=cover_result.error_message if hasattr(cover_result, 'error_message') else None
            )

            if cover_result.success and cover_result.image_url:
                settings = get_settings()

                # Check if image is already in R2 (cartoon pipeline uploads directly)
                if cover_result.image_url.startswith(settings.r2_public_url):
                    # Already in R2, use directly
                    cover_url = cover_result.image_url
                    logger.info("Cover already in R2 storage", cover_url=cover_url)
                else:
                    # Download from external URL and upload to R2 (photorealistic pipeline)
                    cover_storage_path = f"final/{preview_id}/cover.jpg"
                    logger.info("Uploading cover to storage", path=cover_storage_path)
                    cover_url = await StorageService().download_and_upload(
                        cover_result.image_url, cover_storage_path
                    )

                logger.info("Cover uploaded to storage", cover_url=cover_url)

                # ============================================
                # Apply text overlay to cover (theme title + "Starring {name}")
                # ============================================
                try:
                    # Get story title from theme template
                    story_title = template.get_title(safe_child_name)
                    # Extract just the theme name portion
                    # e.g., "Emma's Enchanted Forest Adventure" -> "Enchanted Forest"
                    # e.g., "Emma and the Enchanted Forest" -> "The Enchanted Forest"
                    theme_display_name = (
                        template.title_template
                        .replace("{name}'s ", "")
                        .replace("{name} and the ", "The ")
                        .replace("{name} and The ", "The ")
                        .replace(" Adventure", "")
                    )

                    logger.info(
                        "Processing cover text overlay",
                        story_title=story_title,
                        theme_display_name=theme_display_name,
                        child_name=safe_child_name
                    )

                    image_processor = get_image_processor()
                    cover_with_text_bytes = await image_processor.process_cover_page(
                        cover_image_url=cover_url,
                        story_title=theme_display_name,
                        child_name=safe_child_name
                    )

                    # Upload processed cover (with text) to R2
                    cover_with_text_path = f"final/{preview_id}/cover_final.png"
                    cover_url = await StorageService().upload_image(
                        image_bytes=cover_with_text_bytes,
                        path=cover_with_text_path,
                        content_type="image/png"
                    )

                    logger.info("Cover with text overlay uploaded", cover_url=cover_url)

                except Exception as cover_text_error:
                    logger.error(
                        "Cover text overlay failed, using original cover",
                        error=str(cover_text_error),
                        preview_id=preview_id
                    )
                    # Continue with original cover_url if text overlay fails

                # Update database with cover URL
                update_result = db.table("previews").update({
                    "cover_url": cover_url
                }).eq("preview_id", preview_id).execute()

                logger.info(
                    "Cover URL saved to database",
                    preview_id=preview_id,
                    cover_url=cover_url,
                    db_update_success=bool(update_result.data)
                )

                # V2: Incremental book_structure update for cover
                # Add cover to book_structure so frontend can show it immediately
                book_structure_incremental["0"] = {
                    "type": "cover",
                    "url": cover_url,
                    "is_locked": False,
                    "is_generated": True
                }

                # Update database with cover in book_structure
                db.table("previews").update({
                    "book_structure": book_structure_incremental,
                    "current_generating_page": 4,  # Next: first story page (index 4)
                    "generation_progress": 15
                }).eq("preview_id", preview_id).execute()

                logger.info("Incremental update: cover added to book_structure", preview_id=preview_id)

                # ============================================
                # PHASE 1.6-1.9: Process early filler pages (1, 2, 3, 4) sequentially
                # ============================================
                # Extract story texts now (needed for text pages)
                from app.services.story_text_extractor import extract_story_texts
                story_texts = extract_story_texts(theme, safe_child_name)
                logger.info(
                    "Story texts extracted for sequential processing",
                    theme=theme,
                    count=len(story_texts)
                )

                filler_service = get_filler_pages_service()
                early_filler_indices = [1, 2, 3, 4]  # Dedication, Intro1, Intro2, Text1

                for filler_idx in early_filler_indices:
                    page_config = get_page_config(filler_idx)
                    if not page_config:
                        continue

                    # Calculate progress: pages 1-3 get 12%, 14%, 16%
                    progress = 10 + (filler_idx * 2)
                    await update_job_progress(
                        job_id,
                        progress,
                        f"Adding magical touches to page {filler_idx + 1}... ✨"
                    )

                    try:
                        filler_url = await filler_service.process_single_page(
                            preview_id=preview_id,
                            page_config=page_config,
                            theme=theme,
                            style=style,
                            child_name=safe_child_name,
                            story_texts=story_texts
                        )

                        if filler_url:
                            # Add to incremental book_structure
                            book_structure_incremental[str(filler_idx)] = {
                                "type": page_config.page_type.value,
                                "url": filler_url,
                                "is_locked": False,
                                "is_generated": True
                            }

                            # Update database incrementally
                            db.table("previews").update({
                                "book_structure": book_structure_incremental,
                                "current_generating_page": filler_idx,
                                "generation_progress": progress
                            }).eq("preview_id", preview_id).execute()

                            logger.info(
                                f"Sequential filler page {filler_idx} processed",
                                preview_id=preview_id,
                                url=filler_url[:80] if filler_url else None
                            )
                    except Exception as filler_err:
                        logger.error(
                            f"Failed to process filler page {filler_idx}",
                            preview_id=preview_id,
                            error=str(filler_err)
                        )
                        # Continue - don't block on filler errors

            else:
                logger.warning(
                    "Cover generation failed, will use first page as cover",
                    preview_id=preview_id,
                    success=cover_result.success,
                    error=getattr(cover_result, 'error_message', 'Unknown error')
                )
                # Still need to extract story_texts for later use
                from app.services.story_text_extractor import extract_story_texts
                story_texts = extract_story_texts(theme, safe_child_name)

        except Exception as e:
            logger.error(
                "Cover generation error (non-fatal)",
                preview_id=preview_id,
                error=str(e),
                error_type=type(e).__name__
            )
            import traceback
            logger.error("Cover generation traceback", traceback=traceback.format_exc())
            # Continue without cover - will fall back to using first page
            # Still need to extract story_texts for later use
            from app.services.story_text_extractor import extract_story_texts
            story_texts = extract_story_texts(theme, safe_child_name)

        # ============================================
        # PHASE 2: Generate story pages (15% to 90%)
        # ============================================
        hires_images = []
        story_pages = []

        for i, page_template in enumerate(pages_to_generate):
            page_num = i + 1

            try:
                # Calculate progress (15% to 90% for story page generation)
                progress = 15 + int((i / len(pages_to_generate)) * 75)
                await update_job_progress(
                    job_id,
                    progress,
                    get_progress_message(f"page_{page_num}", page_num)
                )

                # Get prompt for this page
                prompt = page_template.realistic_prompt or page_template.artistic_prompt or ""

                if not prompt:
                    logger.warning(f"No prompt found for page {page_num}, skipping")
                    continue

                # Generate image with pipeline (photorealistic or cartoon3d)
                # Get scene_type and face_expression from page template
                scene_type = getattr(page_template, 'scene_type', None) or ""
                face_expression = getattr(page_template, 'face_expression', None) or ""

                logger.info(f"Generating page {page_num} with {style} pipeline", child_age=child_age, child_gender=child_gender, scene_type=scene_type, face_expression=face_expression or "fallback")

                result = await pipeline.generate_with_face_analysis(
                    prompt=prompt,
                    face_url=photo_urls,  # Pass all photo URLs
                    child_name=safe_child_name,
                    child_age=child_age,
                    child_gender=child_gender,
                    analyzed_features=analyzed_features,
                    aspect_ratio="1:1",  # Square format for consistency with flipbook viewer
                    scene_type=scene_type,
                    preview_id=preview_id,
                    page_number=page_num,
                    face_expression=face_expression
                )

                if result.success and result.image_url:
                    settings = get_settings()

                    # Check if image is already in R2 (cartoon pipeline uploads directly)
                    if result.image_url.startswith(settings.r2_public_url):
                        # Already in R2, use directly
                        stored_url = result.image_url
                    else:
                        # Download from external URL and upload to R2 (photorealistic pipeline)
                        storage_path = f"final/{preview_id}/page_{page_num:02d}.jpg"
                        stored_url = await StorageService().download_and_upload(
                            result.image_url, storage_path
                        )

                    # Store in format expected by preview.py
                    hires_images.append({"page": page_num, "url": stored_url})

                    # Prepare page data (use both 'text' and 'story_text' for compatibility)
                    # Use sanitize_for_prompt to safely insert name into story text
                    story_text_value = sanitize_for_prompt(page_template.story_text, safe_child_name)
                    story_pages.append({
                        'page': page_num,
                        'image_url': stored_url,
                        'text': story_text_value,  # For preview.py
                        'story_text': story_text_value,  # For PDF generator
                        'dialogue': [],  # StoryGift handles dialogue in HTML template
                        'realistic_prompt': prompt
                    })

                    logger.info(f"Page {page_num} generated successfully")

                    # PROGRESSIVE LOADING: Update database after each page so frontend can show it
                    # Create watermarked preview for this page immediately
                    if page_num <= 5:  # Only first 5 pages get previews
                        try:
                            preview_path = f"final/{preview_id}/preview_{page_num:02d}.jpg"
                            watermarked_url = await create_watermarked_preview(
                                source_url=stored_url,
                                output_path=preview_path,
                                watermark_text="PREVIEW - zelavokids.com",
                                resize_width=800
                            )

                            # Store preview URL in story_pages for tracking
                            story_pages[-1]["preview_url"] = watermarked_url

                        except Exception as preview_err:
                            logger.error(f"Failed to create preview for page {page_num}: {preview_err}")
                            # Don't wipe previous pages - just skip this page's preview
                            # Frontend will show the high-res version instead

                    # Build preview_images list from story_pages that have preview_url
                    current_preview_images = [
                        {"page": sp["page"], "url": sp["preview_url"]}
                        for sp in story_pages
                        if sp.get("preview_url")
                    ]

                    # V2: Incremental book_structure update after each page
                    # This enables frontend to show pages one-by-one as they complete
                    try:
                        # Map story page number (1-5) to book index (5, 7, 9, 11, 13)
                        # page_num 1→5, 2→7, 3→9, 4→11, 5→13
                        # NEW ORDER: Text on LEFT, AI on RIGHT
                        book_index = 5 + (page_num - 1) * 2

                        # Add this page to incremental book_structure
                        book_structure_incremental[str(book_index)] = {
                            "type": "generated",
                            "url": stored_url,
                            "is_locked": False,
                            "is_generated": True
                        }

                        # Calculate progress: cover=15%, pages 1-5 = 15% to 90%
                        incremental_progress = 15 + int((page_num / len(pages_to_generate)) * 75)

                        # Determine NEXT generating page for frontend to show loading state
                        # Preview AI indices: [0, 5, 7, 9, 11, 13] (NEW ORDER)
                        preview_ai_indices = [5, 7, 9, 11, 13]
                        current_idx_pos = preview_ai_indices.index(book_index) if book_index in preview_ai_indices else -1
                        next_generating = preview_ai_indices[current_idx_pos + 1] if current_idx_pos >= 0 and current_idx_pos + 1 < len(preview_ai_indices) else None

                        # Update database with incremental book_structure
                        db.table("previews").update({
                            "book_structure": book_structure_incremental,
                            "current_generating_page": next_generating,
                            "generation_progress": incremental_progress
                        }).eq("preview_id", preview_id).execute()

                        logger.info(
                            f"Incremental update: page {page_num} (index {book_index}) added to book_structure",
                            preview_id=preview_id,
                            progress=incremental_progress,
                            next_generating=next_generating
                        )

                        # ============================================
                        # SEQUENTIAL: Process text page after AI page
                        # AI page 5 → Text page 6, 7→8, 9→10, 11→12, 13→(skip 14, locked)
                        # ============================================
                        text_page_index = book_index + 1  # e.g., 5→6, 7→8, etc.

                        # Only process if text page is in preview range (6, 8, 10, 12)
                        # Skip page 14 (first locked text page)
                        if text_page_index <= 13:
                            text_page_config = get_page_config(text_page_index)

                            if text_page_config and text_page_config.filler_filename:
                                try:
                                    # Update progress for text page
                                    text_progress = incremental_progress + 3  # Slightly ahead
                                    await update_job_progress(
                                        job_id,
                                        text_progress,
                                        f"Adding story text for page {text_page_index + 1}... ✨"
                                    )

                                    filler_service = get_filler_pages_service()
                                    text_url = await filler_service.process_single_page(
                                        preview_id=preview_id,
                                        page_config=text_page_config,
                                        theme=theme,
                                        style=style,
                                        child_name=safe_child_name,
                                        story_texts=story_texts
                                    )

                                    if text_url:
                                        # Add text page to incremental book_structure
                                        book_structure_incremental[str(text_page_index)] = {
                                            "type": text_page_config.page_type.value,
                                            "url": text_url,
                                            "is_locked": False,
                                            "is_generated": True
                                        }

                                        # Update database with text page
                                        db.table("previews").update({
                                            "book_structure": book_structure_incremental,
                                            "current_generating_page": text_page_index,
                                            "generation_progress": text_progress
                                        }).eq("preview_id", preview_id).execute()

                                        logger.info(
                                            f"Sequential text page {text_page_index} processed",
                                            preview_id=preview_id,
                                            url=text_url[:80] if text_url else None
                                        )
                                except Exception as text_err:
                                    logger.error(
                                        f"Failed to process text page {text_page_index}",
                                        preview_id=preview_id,
                                        error=str(text_err)
                                    )
                                    # Continue - don't block on text page errors

                    except Exception as incr_err:
                        logger.error(f"Incremental book_structure update failed (non-fatal): {incr_err}")
                else:
                    logger.error(f"Page {page_num} generation failed: {result.error_message}")

            except Exception as e:
                logger.error(f"Error generating page {page_num}", error=str(e))
                continue

        # ============================================
        # PHASE 2.5: Finalize Book Structure (90% to 95%)
        # NOTE: Filler pages already processed sequentially above
        # ============================================
        await update_job_progress(job_id, 90, "Finalizing your magical story... ✨")

        # Collect filler_pages_processed from incrementally built book_structure
        # These were processed inline: 1,2,3,4 after cover; 6,8,10,12 after AI pages
        filler_pages_processed: Dict[int, str] = {}
        preview_filler_indices = [1, 2, 3, 4, 6, 8, 10, 12]  # Dedication, Intro1, Intro2, Text1-5

        for idx in preview_filler_indices:
            page_data = book_structure_incremental.get(str(idx))
            if page_data and page_data.get("url"):
                filler_pages_processed[idx] = page_data["url"]

        logger.info(
            "Filler pages collected from sequential processing",
            preview_id=preview_id,
            filler_count=len(filler_pages_processed),
            filler_indices=list(filler_pages_processed.keys())
        )

        # Use the incrementally built book_structure
        book_structure = book_structure_incremental.copy()

        # Build complete book_structure - add locked page markers
        # IMPORTANT: Use string keys for frontend compatibility
        for page_config in BOOK_STRUCTURE:
            page_key = str(page_config.index)

            # Skip if page already exists in book_structure (from incremental updates)
            if page_key in book_structure:
                # Ensure it has the correct type field
                if "type" not in book_structure[page_key]:
                    book_structure[page_key]["type"] = page_config.page_type.value
                continue

            if not page_config.is_preview:
                # Mark locked pages
                book_structure[page_key] = {
                    "type": page_config.page_type.value,
                    "is_locked": True,
                    "url": None
                }
                continue

            # Add missing preview pages as fallback
            page_data = {
                "type": page_config.page_type.value,
                "is_locked": False
            }

            if page_config.page_type == PageType.COVER:
                page_data["url"] = cover_url
            elif page_config.page_type == PageType.GENERATED:
                story_page_num = (page_config.index - 4) // 2 + 1 if page_config.index >= 4 else 0
                matching_page = next(
                    (sp for sp in story_pages if sp.get("page") == story_page_num),
                    None
                )
                if matching_page:
                    page_data["url"] = matching_page.get("image_url")
            else:
                # Filler page fallback
                page_data["url"] = filler_pages_processed.get(page_config.index)

            book_structure[page_key] = page_data

        # ============================================
        # CRITICAL VALIDATION: Ensure ALL preview pages have URLs
        # ============================================
        # Check that all AI-generated preview pages have valid URLs
        missing_ai_pages = []
        for idx in PREVIEW_AI_INDICES:  # [0, 5, 7, 9, 11, 13]
            page_data = book_structure.get(str(idx))
            if not page_data or not page_data.get("url"):
                missing_ai_pages.append(idx)

        # Check that all filler preview pages have valid URLs
        missing_filler_pages = []
        preview_filler_indices = [1, 2, 3, 4, 6, 8, 10, 12]  # Dedication, Intro1, Intro2, Text1-5
        for idx in preview_filler_indices:
            page_data = book_structure.get(str(idx))
            if not page_data or not page_data.get("url"):
                missing_filler_pages.append(idx)

        # FAIL FAST: If any preview pages are missing URLs, fail the generation
        if missing_ai_pages or missing_filler_pages:
            error_msg = f"Preview generation incomplete - Missing AI pages: {missing_ai_pages}, Missing filler pages: {missing_filler_pages}"
            logger.error(
                error_msg,
                preview_id=preview_id,
                job_id=job_id,
                missing_ai_pages=missing_ai_pages,
                missing_filler_pages=missing_filler_pages,
                book_structure_size=len(book_structure)
            )

            await update_preview_status(
                preview_id=preview_id,
                status=PreviewStatus.FAILED
            )

            await update_job_status(
                job_id=job_id,
                status=JobStatus.FAILED,
                error=error_msg
            )
            return

        logger.info(
            "Preview validation passed - all pages have URLs",
            preview_id=preview_id,
            preview_ai_pages=len(PREVIEW_AI_INDICES),
            preview_filler_pages=len(preview_filler_indices),
            total_preview_pages=len(PREVIEW_AI_INDICES) + len(preview_filler_indices)
        )

        # ============================================
        # PHASE 3: Finalize Preview (95% to 100%)
        # ============================================
        await update_job_progress(job_id, 95, get_progress_message("finalizing"))

        # Build final preview_images from story_pages
        preview_images = [
            {"page": sp["page"], "url": sp["preview_url"]}
            for sp in story_pages
            if sp.get("preview_url")
        ]

        # Debug logging before database update
        # Count AI pages in book_structure - use constant from config
        all_ai_indices = AI_GENERATED_INDICES  # [0, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
        ai_pages_present = [idx for idx in all_ai_indices if str(idx) in book_structure]
        preview_ai_pages_present = [idx for idx in PREVIEW_AI_INDICES if str(idx) in book_structure]

        logger.info(
            "About to update database with generation results",
            preview_id=preview_id,
            filler_pages_count=len(filler_pages_processed),
            book_structure_pages=len(book_structure),
            story_texts_count=len(story_texts),
            total_ai_pages=len(ai_pages_present),
            preview_ai_pages=len(preview_ai_pages_present),
            preview_ai_indices_present=preview_ai_pages_present
        )

        # Check if generation was actually successful
        if not hires_images or not story_pages:
            error_msg = f"Generation failed: No images or story pages generated"
            logger.error(error_msg, preview_id=preview_id)

            await update_preview_status(
                preview_id=preview_id,
                status=PreviewStatus.FAILED
            )

            await update_job_status(
                job_id=job_id,
                status=JobStatus.FAILED,
                error=error_msg
            )
            return

        # Update preview in database - set generation_phase to 'preview' (not complete)
        # Include 26-page book structure and filler pages data
        await update_preview_status(
            preview_id=preview_id,
            status=PreviewStatus.ACTIVE,
            # V2 columns only - hires_images, preview_images, story_pages were removed in migration 028
            generation_phase='preview',  # Mark as preview only
            preview_page_count=PREVIEW_PAGE_COUNT,  # 13 pages visible in preview
            total_pages=TOTAL_PAGE_COUNT,  # 26 total pages (database column is 'total_pages')
            book_structure=book_structure,  # Complete page structure JSONB
            filler_pages_processed=filler_pages_processed,  # Processed filler URLs
            child_photo_url=photo_urls[0],  # Primary photo for post-payment generation
            story_texts=story_texts  # All 10 story texts for locked page generation
            # NOTE: pdf_url is NOT set - will be generated after payment
        )

        # Mark job as completed
        await update_job_status(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            result_data={
                "generation_phase": "preview",
                "preview_pages_count": 13,
                "total_pages_count": 26,
                "book_structure_pages": len(book_structure),
                "story_texts_count": len(story_texts),
                "filler_pages_count": len(filler_pages_processed)
            }
        )

        logger.info(
            "StoryGift PREVIEW generation completed (13 preview pages)",
            preview_id=preview_id,
            book_structure_pages=len(book_structure),
            story_texts_count=len(story_texts),
            generation_phase="preview"
        )

        # ============================================
        # PHASE 4: Send Preview Ready Email (only if user opted in)
        # ============================================
        try:
            # Get customer email and notify preference from preview record
            preview_data = db.table("previews").select(
                "customer_email", "notify_on_complete"
            ).eq("preview_id", preview_id).execute()

            if preview_data.data:
                record = preview_data.data[0]
                customer_email = record.get("customer_email")
                notify_on_complete = record.get("notify_on_complete", False)

                # Only send email if user explicitly opted in via the popup
                if notify_on_complete and customer_email:
                    settings = get_settings()

                    # Build preview URL using frontend_url config (hash routing)
                    preview_url = f"{settings.frontend_url}#/preview/{preview_id}"

                    email_service = get_email_service()
                    await email_service.send_preview_ready_email(
                        to_email=customer_email,
                        child_name=safe_child_name,
                        preview_url=preview_url
                    )
                    logger.info("Preview ready email sent", to=customer_email, preview_id=preview_id)
                else:
                    logger.info(
                        "Skipping preview notification (user did not opt in)",
                        preview_id=preview_id,
                        has_email=bool(customer_email),
                        notify_flag=notify_on_complete
                    )
        except Exception as email_error:
            # Email failure should not fail the preview generation
            logger.error("Failed to send preview ready email (non-fatal)", error=str(email_error))

    except Exception as e:
        logger.error(
            "StoryGift preview generation failed",
            preview_id=preview_id,
            error=str(e)
        )

        await update_job_status(
            job_id=job_id,
            status=JobStatus.FAILED,
            error=str(e)
        )

        await update_preview_status(
            preview_id=preview_id,
            status=PreviewStatus.FAILED
        )


async def generate_remaining_pages_and_pdf(
    order_id: str,
    preview_id: str,
    child_name: str,
    max_retries: int = 3,
    order_type: str = "digital"
):
    """
    Generate remaining locked pages (13-25) after payment, then create full 26-page PDF.

    V2 26-Page Structure Post-Payment Flow:
    - Preview pages 0-13: Already generated (14 pages)
    - Locked pages 14-25: Generated here (12 pages)
        - Text pages: 15, 17, 19, 21, 23 (with story text overlays)
        - AI pages: 14, 16, 18, 20, 22 (AI-generated images)
        - Filler pages: 24 (end_page), 25 (back_cover)

    Args:
        order_id: Shopify order ID
        preview_id: Preview to complete
        child_name: Child's name for story
        max_retries: Max retry attempts (default 3)
        order_type: 'digital' or 'physical'
    """
    from app.services.story_text_extractor import extract_story_texts
    from app.services.storygift_pdf_generator_v2 import get_pdf_generator_v2
    from app.config.book_structure import LOCKED_AI_INDICES

    retry_count = 0
    last_error = None

    while retry_count < max_retries:
        try:
            safe_child_name = sanitize_child_name(child_name)

            logger.info(
                "Starting V2 locked page generation (13-25)",
                order_id=order_id,
                preview_id=preview_id,
                child_name=safe_child_name,
                order_type=order_type,
                attempt=retry_count + 1
            )

            generation_start = datetime.utcnow()

            # ===================================================================
            # PHASE 1: Fetch preview data
            # ===================================================================
            db = get_db()
            preview_result = db.table("previews").select("*").eq("preview_id", preview_id).execute()

            if not preview_result.data:
                raise StorageError(f"Preview not found: {preview_id}")

            preview_data = preview_result.data[0]

            # Get existing data from preview phase
            book_structure = preview_data.get("book_structure") or {}
            analyzed_features = preview_data.get("analyzed_features", "a cute child")
            child_photo_url = preview_data.get("child_photo_url") or preview_data.get("photo_url")
            theme = preview_data.get("theme", "storygift_enchanted_forest")
            style = preview_data.get("style", "photorealistic")
            child_age = preview_data.get("child_age", 5)
            child_gender = preview_data.get("child_gender", "male")

            if not child_photo_url:
                raise StorageError(f"No child photo URL found for preview: {preview_id}")

            # Build photo_urls list for multi-face pipeline
            # Prefer stored photo_urls array (JSONB), fallback to single child_photo_url
            stored_photo_urls = preview_data.get("photo_urls")
            if stored_photo_urls and isinstance(stored_photo_urls, list) and len(stored_photo_urls) > 0:
                photo_urls = stored_photo_urls
            else:
                photo_urls = [child_photo_url]

            if not book_structure:
                raise StorageError(f"No book_structure found in preview: {preview_id}")

            # Extract story texts from theme (for all 10 text pages)
            story_texts_dict = extract_story_texts(theme, safe_child_name)

            if not story_texts_dict:
                raise StorageError(f"Failed to extract story texts for theme: {theme}")

            logger.info(
                "Preview data loaded",
                preview_id=preview_id,
                has_book_structure=bool(book_structure),
                book_structure_pages=len(book_structure),
                story_texts_count=len(story_texts_dict)
            )

            # Mark as generating locked pages
            db.table("previews").update({
                "generation_phase": "generating_locked",
                "current_generating_page": 13,
                "generation_progress": 50
            }).eq("preview_id", preview_id).execute()

            db.table("orders").update({
                "status": OrderStatus.GENERATING_PDF.value
            }).eq("order_id", order_id).execute()

            # ===================================================================
            # PHASE 2: Generate locked AI pages (15, 17, 19, 21, 23) - NEW ORDER
            # ===================================================================
            logger.info(
                "Generating locked AI pages",
                preview_id=preview_id,
                ai_indices=LOCKED_AI_INDICES
            )

            template = get_theme(theme)
            pipeline = get_pipeline_for_style(style)

            # Map book indices to theme pages (NEW ORDER: Text on LEFT, AI on RIGHT)
            # Book indices: 15, 17, 19, 21, 23 correspond to theme pages 6, 7, 8, 9, 10
            ai_index_to_theme_page = {
                15: 6,
                17: 7,
                19: 8,
                21: 9,
                23: 10,
            }

            for ai_index in LOCKED_AI_INDICES:
                theme_page_num = ai_index_to_theme_page[ai_index]
                page_template = template.pages[theme_page_num - 1]  # 0-indexed

                logger.info(
                    f"Generating locked AI page {ai_index} (theme page {theme_page_num})",
                    preview_id=preview_id
                )

                # Update progress (50% to 75% for AI pages)
                progress = 50 + int((LOCKED_AI_INDICES.index(ai_index) / len(LOCKED_AI_INDICES)) * 25)
                db.table("previews").update({
                    "generation_progress": progress,
                    "current_generating_page": ai_index
                }).eq("preview_id", preview_id).execute()

                prompt = page_template.realistic_prompt or page_template.artistic_prompt
                scene_type = getattr(page_template, 'scene_type', None) or ""
                face_expression = getattr(page_template, 'face_expression', None) or ""

                # Generate image
                result = await pipeline.generate_with_face_analysis(
                    prompt=prompt,
                    face_url=photo_urls,  # Pass all photo URLs
                    child_name=safe_child_name,
                    child_age=child_age,
                    child_gender=child_gender,
                    analyzed_features=analyzed_features,
                    aspect_ratio="1:1",
                    scene_type=scene_type,
                    preview_id=preview_id,
                    page_number=theme_page_num,
                    face_expression=face_expression
                )

                if not result.success or not result.image_url:
                    raise ImageGenerationError(
                        f"Failed to generate AI page {ai_index}: {result.error}"
                    )

                # Upload to R2 if not already there
                settings = get_settings()
                if result.image_url.startswith(settings.r2_public_url):
                    stored_url = result.image_url
                else:
                    storage_path = f"final/{preview_id}/page_{ai_index:02d}.jpg"
                    stored_url = await StorageService().download_and_upload(
                        result.image_url, storage_path
                    )

                # Update book_structure
                book_structure[str(ai_index)] = {
                    "type": "generated",
                    "url": stored_url,
                    "is_locked": False,  # Unlocked after payment
                    "is_generated": True,
                    "is_preview": False
                }

                logger.info(
                    f"AI page {ai_index} generated successfully",
                    url=stored_url[:80]
                )

            # ===================================================================
            # PHASE 3: Process locked filler pages (14-25) - NEW ORDER
            # ===================================================================
            logger.info(
                "Processing locked filler pages",
                preview_id=preview_id
            )

            # Update progress to 75%
            db.table("previews").update({
                "generation_progress": 75,
                "current_generating_page": 14
            }).eq("preview_id", preview_id).execute()

            filler_service = get_filler_pages_service()

            locked_filler_pages = await filler_service.process_locked_filler_pages(
                preview_id=preview_id,
                theme=theme,
                style=style,
                child_name=safe_child_name,
                story_texts=story_texts_dict
            )

            logger.info(
                "Locked filler pages processed",
                preview_id=preview_id,
                filler_count=len(locked_filler_pages)
            )

            # Update book_structure with filler pages
            for page_index, filler_url in locked_filler_pages.items():
                if str(page_index) in book_structure:
                    # Update existing entry
                    book_structure[str(page_index)]["url"] = filler_url
                else:
                    # Determine page type (NEW ORDER: Text on LEFT at even indices)
                    if page_index in [14, 16, 18, 20, 22]:
                        page_type = "text"
                    elif page_index == 24:
                        page_type = "end_page"
                    elif page_index == 25:
                        page_type = "back_cover"
                    else:
                        page_type = "filler"

                    book_structure[str(page_index)] = {
                        "type": page_type,
                        "url": filler_url,
                        "is_locked": False,
                        "is_generated": True,
                        "is_preview": False
                    }

            # Merge filler pages with existing filler_pages_processed
            all_filler_pages_processed = preview_data.get("filler_pages_processed", {})
            all_filler_pages_processed.update(locked_filler_pages)

            # Update database with complete book structure
            db.table("previews").update({
                "book_structure": book_structure,
                "filler_pages_processed": all_filler_pages_processed,
                "generation_phase": "pages_complete",
                "generation_progress": 90
            }).eq("preview_id", preview_id).execute()

            logger.info(
                "All 26 pages generated successfully",
                preview_id=preview_id,
                order_id=order_id,
                book_structure_size=len(book_structure)
            )

            # ===================================================================
            # PHASE 4: Generate 26-page PDF using V2 generator
            # ===================================================================
            try:
                logger.info("Generating 26-page PDF with V2 generator", preview_id=preview_id)

                # Update progress to 90%
                db.table("previews").update({
                    "generation_progress": 90,
                    "current_generating_page": None
                }).eq("preview_id", preview_id).execute()

                # Prepare page URLs dict (index → URL)
                page_urls = {}
                for idx_str, page_data in book_structure.items():
                    idx = int(idx_str)
                    if page_data.get("url"):
                        page_urls[idx] = page_data["url"]

                # Verify we have all 26 pages
                missing_pages = [i for i in range(26) if i not in page_urls]
                if missing_pages:
                    raise StorageError(
                        f"Missing pages in book structure: {missing_pages}"
                    )

                logger.info(
                    "All pages present for PDF generation",
                    preview_id=preview_id,
                    total_pages=len(page_urls)
                )

                # Get story title
                story_title = template.get_title(safe_child_name) if hasattr(template, 'get_title') else f"{safe_child_name}'s Adventure"

                # Use V2 PDF generator
                pdf_generator_v2 = get_pdf_generator_v2()

                pdf_url = await pdf_generator_v2.generate_pdf(
                    preview_id=preview_id,
                    child_name=safe_child_name,
                    page_urls=page_urls,
                    story_title=story_title,
                    add_blank_back_page=(order_type == "physical")
                )

                logger.info(
                    "PDF generated successfully",
                    preview_id=preview_id,
                    pdf_url=pdf_url[:80]
                )

                # Update database with PDF
                if order_type == "physical":
                    db.table("previews").update({
                        "pdf_url": pdf_url,
                        "status": PreviewStatus.PURCHASED.value,
                        "generation_phase": "preparing_print",
                        "generation_progress": 100,
                        "current_generating_page": None
                    }).eq("preview_id", preview_id).execute()
                else:
                    db.table("previews").update({
                        "pdf_url": pdf_url,
                        "status": PreviewStatus.PURCHASED.value,
                        "generation_phase": "complete",
                        "generation_progress": 100,
                        "current_generating_page": None
                    }).eq("preview_id", preview_id).execute()

                db.table("orders").update({
                    "pdf_url": pdf_url,
                    "status": OrderStatus.COMPLETED.value,
                    "completed_at": datetime.utcnow().isoformat(),
                    "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
                }).eq("order_id", order_id).execute()

                duration = (datetime.utcnow() - generation_start).total_seconds()

                logger.info(
                    "V2 26-page PDF generation complete",
                    order_id=order_id,
                    preview_id=preview_id,
                    pdf_url=pdf_url[:80],
                    duration_sec=round(duration, 1),
                    order_type=order_type
                )

                # Physical order Lulu submission
                if order_type == "physical":
                    logger.info(
                        "Physical order - submitting to Lulu",
                        order_id=order_id,
                        preview_id=preview_id
                    )
                    try:
                        from app.background.lulu_tasks import submit_lulu_print_job

                        lulu_submitted = False
                        for attempt in range(3):
                            try:
                                await submit_lulu_print_job(
                                    order_id=order_id,
                                    preview_id=preview_id
                                )
                                lulu_submitted = True
                                logger.info(
                                    "Lulu submission successful",
                                    order_id=order_id,
                                    attempt=attempt + 1
                                )
                                break
                            except Exception as e:
                                logger.warning(
                                    f"Lulu submission attempt {attempt + 1} failed",
                                    error=str(e)
                                )
                                if attempt < 2:
                                    await asyncio.sleep(2 ** attempt)

                        if not lulu_submitted:
                            logger.error(
                                "Lulu submission failed after retries",
                                order_id=order_id
                            )
                    except Exception as lulu_error:
                        logger.error(
                            "Lulu submission error (non-fatal)",
                            order_id=order_id,
                            error=str(lulu_error)
                        )

                # Send completion email
                try:
                    email_service = get_email_service()
                    customer_email = preview_data.get("customer_email")

                    if customer_email:
                        await email_service.send_book_ready_email(
                            to_email=customer_email,
                            child_name=safe_child_name,
                            preview_id=preview_id,
                            pdf_url=pdf_url,
                            order_type=order_type
                        )
                        logger.info(
                            "Completion email sent",
                            order_id=order_id,
                            email=customer_email
                        )
                except Exception as email_error:
                    logger.warning(
                        "Failed to send completion email (non-fatal)",
                        order_id=order_id,
                        error=str(email_error)
                    )

                return pdf_url

            except Exception as pdf_error:
                logger.error(
                    "PDF generation failed",
                    preview_id=preview_id,
                    order_id=order_id,
                    error=str(pdf_error)
                )
                raise

        except Exception as e:
            retry_count += 1
            last_error = e

            logger.error(
                "Post-payment generation failed",
                order_id=order_id,
                preview_id=preview_id,
                attempt=retry_count,
                max_retries=max_retries,
                error=str(e),
                error_type=type(e).__name__
            )

            if retry_count >= max_retries:
                # Mark as failed
                try:
                    db = get_db()
                    db.table("orders").update({
                        "status": OrderStatus.FAILED.value,
                        "error_message": f"Generation failed after {max_retries} attempts: {str(e)}"
                    }).eq("order_id", order_id).execute()

                    db.table("previews").update({
                        "generation_phase": "failed",
                        "status": PreviewStatus.FAILED.value
                    }).eq("preview_id", preview_id).execute()

                    logger.error(
                        "Order marked as failed after max retries",
                        order_id=order_id,
                        preview_id=preview_id
                    )
                except Exception as db_error:
                    logger.error("Failed to update failure status", error=str(db_error))

                raise

            # Wait before retry (exponential backoff)
            wait_seconds = 2 ** retry_count
            logger.info(
                f"Retrying in {wait_seconds} seconds...",
                attempt=retry_count,
                max_retries=max_retries
            )
            await asyncio.sleep(wait_seconds)


# Legacy alias for backward compatibility
async def generate_storygift_pdf_from_order(
    order_id: str,
    preview_id: str,
    child_name: str,
    order_type: str = "digital"
):
    """Legacy wrapper - now generates remaining pages + PDF (+ Lulu for physical)."""
    return await generate_remaining_pages_and_pdf(
        order_id, preview_id, child_name, order_type=order_type
    )

