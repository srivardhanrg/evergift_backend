"""
Photo upload endpoint.
"""

import uuid
import imghdr
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Request
from typing import Optional, List
import structlog

from app.models.schemas import PhotoUploadResponse, PhotoData, ErrorResponse
from app.services.face_validation import FaceValidationService
from app.services.storage import StorageService
from app.core.exceptions import FaceValidationError, StorageError
from app.core.rate_limiter import limiter

logger = structlog.get_logger()
router = APIRouter()

# Allowed image types (validated by magic bytes)
ALLOWED_IMAGE_TYPES = {'jpeg', 'png', 'gif', 'webp', 'heic', 'heif'}


def _is_heic(file_bytes: bytes) -> bool:
    """Detect HEIC/HEIF by checking the ftyp box signature (imghdr doesn't support it)."""
    if len(file_bytes) < 12:
        return False
    ftyp = file_bytes[4:8]
    brand = file_bytes[8:12]
    return ftyp == b'ftyp' and brand in (b'heic', b'heix', b'hevc', b'hevx', b'mif1', b'msf1', b'MiHE', b'MiHB')


def validate_image_magic_bytes(file_bytes: bytes) -> str:
    """
    Validate image by checking magic bytes (file signature).
    More secure than trusting Content-Type header which can be spoofed.

    Returns the detected image type or raises HTTPException.
    """
    if _is_heic(file_bytes):
        return 'heic'

    image_type = imghdr.what(None, h=file_bytes)

    if image_type not in ALLOWED_IMAGE_TYPES:
        logger.warning(
            "Invalid image magic bytes",
            detected_type=image_type,
            allowed_types=list(ALLOWED_IMAGE_TYPES)
        )
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_IMAGE_FORMAT",
                "message": f"Invalid image format. Allowed formats: JPEG, PNG, WebP, HEIC. Detected: {image_type or 'unknown'}",
                "detected_type": image_type
            }
        )

    return image_type


@router.post("/upload-photos", response_model=PhotoUploadResponse)
@limiter.limit("10/minute")
async def upload_photos(
    request: Request,
    photos: List[UploadFile] = File(..., min_items=1, max_items=3, description="Child's photos (1-3 images)"),
    session_id: Optional[str] = Form(None, description="Optional session ID")
):
    """
    Upload and validate 1-3 child photos.

    - Validates file type and size for each photo
    - Detects and validates face presence
    - Uploads all photos to storage
    - Returns all photo URLs (accepts if ANY photo passes validation)
    """

    try:
        if len(photos) > 3:
            raise HTTPException(
                status_code=400,
                detail="Maximum 3 photos allowed"
            )

        logger.info("Multi-photo upload started", total_photos=len(photos), session_id=session_id)

        uploaded_photos = []
        face_validator = FaceValidationService()
        storage = StorageService()

        # Process each photo
        for i, photo in enumerate(photos):
            try:
                logger.info(f"Processing photo {i+1}/{len(photos)}", filename=photo.filename)

                # Read file bytes
                photo_bytes = await photo.read()

                # Validate file size (10MB limit)
                if len(photo_bytes) > 10 * 1024 * 1024:  # 10MB
                    logger.warning(f"Photo {i+1} too large, skipping")
                    continue

                # Validate image by magic bytes
                detected_type = validate_image_magic_bytes(photo_bytes)

                logger.info(
                    f"Photo {i+1} file validated",
                    size_bytes=len(photo_bytes),
                    detected_type=detected_type
                )

                # Validate face
                validation_result = face_validator.validate(photo_bytes)

                # Generate unique photo ID
                photo_id = str(uuid.uuid4())

                # Upload to storage (upload regardless of validation for user reference)
                photo_path = f"uploads/{photo_id}/photo_{i+1}.jpg"
                photo_url = await storage.upload_image(
                    photo_bytes,
                    photo_path,
                    content_type="image/jpeg"
                )

                uploaded_photos.append({
                    "photo_id": photo_id,
                    "photo_url": photo_url,
                    "upload_order": i + 1,
                    "face_valid": validation_result.is_valid,
                    "face_count": validation_result.face_count,
                    "quality_score": validation_result.quality_score if validation_result.is_valid else 0.0,
                    "error_code": validation_result.error_code if not validation_result.is_valid else None
                })

                logger.info(f"Photo {i+1} processed",
                           photo_id=photo_id,
                           face_valid=validation_result.is_valid)

            except Exception as e:
                logger.error(f"Failed to process photo {i+1}", error=str(e))
                continue

        if not uploaded_photos:
            raise HTTPException(
                status_code=400,
                detail="No photos could be processed successfully"
            )

        # Get valid photos, sorted by quality score (best first)
        valid_photos = sorted(
            [p for p in uploaded_photos if p["face_valid"]],
            key=lambda p: p["quality_score"],
            reverse=True
        )
        valid_urls = [p["photo_url"] for p in valid_photos]

        # Accept if ANY photo passes validation
        if valid_photos:
            logger.info("Upload successful",
                       total_uploaded=len(uploaded_photos),
                       valid_photos=len(valid_photos))
            return PhotoUploadResponse(
                photos=[PhotoData(**photo) for photo in uploaded_photos],
                valid_photo_urls=valid_urls,
                total_uploaded=len(uploaded_photos),
                valid_count=len(valid_photos),
                has_valid_photos=True,
                message=f"Successfully uploaded {len(valid_photos)} valid photos out of {len(uploaded_photos)}"
            )
        else:
            # All photos failed validation
            logger.warning("All photos failed validation")
            return PhotoUploadResponse(
                photos=[PhotoData(**photo) for photo in uploaded_photos],
                valid_photo_urls=[],
                total_uploaded=len(uploaded_photos),
                valid_count=0,
                has_valid_photos=False,
                message="No photos contain valid faces. Please upload clearer photos with visible faces."
            )

    except FaceValidationError as e:
        logger.warning("Face validation error", error=str(e))
        raise HTTPException(
            status_code=400,
            detail={
                "code": e.code,
                "message": e.message,
                "details": e.details
            }
        )

    except StorageError as e:
        logger.error("Storage error during upload", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to upload photo. Please try again."
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        logger.error("Unexpected error during photo upload", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )