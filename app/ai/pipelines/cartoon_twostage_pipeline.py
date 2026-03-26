"""
Two-Stage Cartoon Pipeline - PRESERVED FOR FUTURE USE

⚠️ NOTE: This pipeline is not exposed in the current version of the application.
The application defaults to photorealistic pipeline only.

This code is fully functional and tested, kept for potential feature expansion.

Pipeline Architecture:
- Stage 1: Generate cartoon scene with NanoBanana (placeholder child)
- Stage 2: Face swap using Segmind FaceSwap Comic (real child's face)

Cost per image: ~$0.11 (NanoBanana $0.04 + Segmind $0.07)
Cost per book (11 images): ~$1.21
"""

import asyncio
import hashlib
import time
import structlog
from typing import Optional, Dict, List, Any
import httpx

from app.ai.base import GenerationResult
from app.services.storage import StorageService
from app.config import get_settings

logger = structlog.get_logger()


# =============================================================================
# LOCKED STYLE - Premium 2D Vector Children's Book Illustration
# Reference: User's approved style image
# DO NOT MODIFY without user approval
# =============================================================================
PREMIUM_CARTOON_STYLE = """
Style: A vibrant 2D vector-style digital illustration, flat cel-shading with soft gradients, clean line art, high-end children's storybook aesthetic.

Lighting/Atmosphere: Bright, warm golden afternoon sunlight, clear blue sky, whimsical and magical atmosphere.

Quality: Premium children's book illustration, professional storybook art, print-ready quality.
"""

PREMIUM_CARTOON_NEGATIVE = """
photorealistic, photograph, realistic skin texture, 3D CGI render, plastic,
ugly, deformed, blurry, low quality, dark, scary, horror,
black bars, letterbox, letterboxing, scope, cinema bars, pillarbox, matte bars, widescreen bars, black borders, black border on top, black border on bottom, cropped frame,
face obscured, face in shadow, profile view, back to camera, face not visible,
child looking away, face blocked by objects, side profile
"""


# =============================================================================
# FACE SWAP PRIMER - prepended to Stage 1 prompt to ensure Segmind-friendly face
# Segmind face swap works best when the placeholder face is frontal, clear, well-lit.
# Moving this to the TOP of the prompt gives it maximum weight with nano-banana.
# =============================================================================
FACE_SWAP_PRIMER = """CRITICAL FACE POSITION RULES FOR FACE SWAP COMPATIBILITY:
Child's face must be frontal or at most 30-degree angle from camera.
Face must be large in frame — occupying at least 20% of image height.
Face fully unobstructed: no hands, hair strands, or objects crossing the face area.
Face evenly front-lit — no harsh side shadows splitting the face in half.
Both eyes fully open and clearly visible. No profile views. No back-of-head shots."""


# =============================================================================
# EXPRESSION MAPPING - scene_type → Segmind expression prompt
# Empty string = preserve natural expression from child's photo
# =============================================================================
EXPRESSION_MAP = {
    # Positive/Joyful expressions
    "celebration": "joyful, beaming smile, excited, happy",
    "triumph": "proud, accomplished, confident smile, victorious",
    "wonder": "amazed, wide-eyed wonder, awestruck, delighted",
    "awe": "amazed, mouth slightly open, wonder-struck",
    "flight": "exhilarated, joyful, free, windswept happiness",
    "mischief": "playful grin, mischievous, cheeky smile",
    "chaos": "surprised, amused, delighted, laughing",

    # Special face-angle expressions (for edge-case pages)
    "sleeping": "peaceful, serene, eyes gently closed, sleeping",
    "looking_down": "looking downward, soft expression, contemplative",

    # Warm/Tender expressions
    "bonding": "gentle smile, warm, affectionate, tender",
    "intimate": "soft smile, peaceful, loving, content",
    "peaceful": "serene, calm, gentle smile, relaxed",
    "farewell": "bittersweet smile, warm, grateful",
    "resolution": "content, peaceful smile, satisfied, happy",
    "return": "relieved, happy, warm smile",

    # Adventure/Action expressions
    "discovery": "curious, excited, eager, bright-eyed",
    "action": "determined, focused, brave, confident",
    "adventure": "excited, eager, adventurous spirit, brave",
    "journey": "curious, anticipating, hopeful",
    "heroic": "brave, determined, confident, strong",
    "climax": "intense focus, determined, courageous",
    "challenge": "determined, focused, ready",
    "rescue": "urgent, determined, brave, caring",
    "chase": "alert, focused, determined, quick-thinking",

    # Neutral/Subtle expressions (empty - preserve natural expression from photo)
    "arrival": "",
    "preparation": "confident, determined, ready for action",
    "transformation": "",
    "revelation": "",
    "ceremony": "",
    "briefing": "",
    "stealth": "",
    "infiltration": "clever knowing smile, secretive alertness",
    "confrontation": "",
    "encounter": "",
    "investigation": "focused, concentrating, analytical, determined",
}


def get_expression_for_scene(scene_type: str, page_prompt: str = "") -> str:
    """
    Get expression prompt for Segmind based on scene_type.

    If scene_type not in map or maps to empty string,
    analyze the page prompt to determine if expression is needed.

    Args:
        scene_type: The scene type from page template
        page_prompt: The full page prompt (for analysis if needed)

    Returns:
        Expression prompt string or empty string
    """
    # First check the map
    if scene_type and scene_type in EXPRESSION_MAP:
        expression = EXPRESSION_MAP[scene_type]
        if expression:
            return expression

    # If not in map or empty, analyze prompt for emotional cues
    if page_prompt:
        prompt_lower = page_prompt.lower()

        # Check for emotional keywords in prompt
        if any(word in prompt_lower for word in ["smile", "smiling", "happy", "joy", "laugh", "grin", "delighted"]):
            return "happy, smiling"
        elif any(word in prompt_lower for word in ["scared", "afraid", "nervous", "worried", "anxious"]):
            return "slightly nervous, uncertain"
        elif any(word in prompt_lower for word in ["amazed", "wonder", "awe", "magical", "astonished"]):
            return "amazed, wonder"
        elif any(word in prompt_lower for word in ["brave", "determined", "hero", "courageous"]):
            return "determined, brave"
        elif any(word in prompt_lower for word in ["peaceful", "calm", "serene", "sleep", "rest"]):
            return "peaceful, calm"
        elif any(word in prompt_lower for word in ["excited", "thrilled", "eager"]):
            return "excited, eager"

    # Default: return empty string (preserve natural expression from photo)
    return ""


class CartoonTwoStagePipeline:
    """
    Two-stage cartoon pipeline for illustrated children's storybooks.

    Flow:
    1. Generate illustrated scene with NanoBanana (placeholder child)
    2. Face swap using Segmind FaceSwap Comic (real child's face)
    3. Result: Beautiful cartoon scene + recognizable child

    Cost: ~$0.11 per image ($0.04 NanoBanana + $0.07 Segmind)
    """

    def __init__(self, model_override: Optional[str] = None):
        """
        Initialize two-stage cartoon pipeline.

        Args:
            model_override: Optional model override (not used currently)

        Raises:
            ValueError: If required API keys are not configured
        """
        self.settings = get_settings()
        self.storage = StorageService()

        # Validate required API keys
        if not self.settings.segmind_api_key:
            raise ValueError(
                "SEGMIND_API_KEY is required for cartoon two-stage pipeline. "
                "Set it in your .env file or environment variables."
            )

        if not self.settings.fal_api_key:
            raise ValueError(
                "FAL_API_KEY is required for cartoon two-stage pipeline. "
                "Set it in your .env file or environment variables."
            )

        # Stage 1: Scene generation model
        self.scene_model_id = "fal-ai/nano-banana/edit"

        # Stage 2: Face swap via Segmind
        self.segmind_endpoint = "https://api.segmind.com/v1/faceswap-comic"

        # Pipeline identifier
        self.model_name = "cartoon_twostage_segmind"

        logger.info(
            "CartoonTwoStagePipeline initialized",
            scene_model=self.scene_model_id,
            face_swap="segmind_faceswap_comic",
            testing_mode=self.settings.testing_mode_enabled
        )

    async def _generate_scene(
        self,
        prompt: str,
        face_url: List[str],  # Changed to support multiple reference images
        aspect_ratio: str = "1:1",
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Stage 1: Generate cartoon scene with NanoBanana.

        Creates illustrated scene with the child's face reference.
        NanoBanana embeds a rough face; Stage 2 Segmind does a clean swap.

        Args:
            prompt: Full scene description with style
            face_url: Child's reference photo URL (required by NanoBanana /edit)
            aspect_ratio: Image aspect ratio (default "1:1" for all pages)
            seed: Optional seed for reproducibility

        Returns:
            Dict with image URL and metadata
        """
        start_time = time.time()

        try:
            logger.info("Stage 1: Generating scene with NanoBanana", prompt_length=len(prompt))

            # Build the full prompt: face primer first (highest weight), then style, then scene
            # FACE_SWAP_PRIMER is prepended so nano-banana prioritizes face position rules
            full_prompt = f"{FACE_SWAP_PRIMER}\n\n{PREMIUM_CARTOON_STYLE}\n\n{prompt}"

            payload = {
                "prompt": full_prompt,
                "negative_prompt": PREMIUM_CARTOON_NEGATIVE.strip(),
                "aspect_ratio": aspect_ratio,
                "image_urls": face_url,  # face_url is now a list - pass all references
            }

            if seed:
                payload["seed"] = seed

            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    f"https://fal.run/{self.scene_model_id}",
                    headers={
                        "Authorization": f"Key {self.settings.fal_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

            latency = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception as json_err:
                    error_msg = f"NanoBanana returned invalid JSON: {str(json_err)}"
                    logger.error("Stage 1 failed - JSON parse error", error=error_msg)
                    return {"success": False, "error": error_msg, "latency_ms": latency}

                images = result.get("images", [])

                if images:
                    image_url = images[0].get("url")
                    if not image_url:
                        error_msg = "NanoBanana returned empty image URL"
                        logger.error("Stage 1 failed - no URL", error=error_msg)
                        return {"success": False, "error": error_msg, "latency_ms": latency}

                    logger.info(
                        "Stage 1 complete: Scene generated",
                        latency_ms=latency,
                        image_url=image_url[:80] if image_url else None
                    )
                    return {
                        "success": True,
                        "image_url": image_url,
                        "latency_ms": latency,
                        "seed": result.get("seed")
                    }

            error_msg = f"NanoBanana error: {response.status_code} - {response.text[:200]}"
            logger.error("Stage 1 failed", error=error_msg)
            return {"success": False, "error": error_msg, "latency_ms": latency}

        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            logger.error("Stage 1 exception", error=str(e))
            return {"success": False, "error": str(e), "latency_ms": latency}

    async def _face_swap_segmind(
        self,
        scene_image_url: str,
        child_photo_urls: List[str],  # Changed to support multiple photos
        expression_prompt: str = "",
        preview_id: str = "",
        page_number: int = 0
    ) -> Dict[str, Any]:
        """
        Stage 2: Face swap using Segmind FaceSwap Comic.

        IMPORTANT: Segmind returns raw image bytes, not a URL.
        We upload to R2 and return the R2 URL.

        Args:
            scene_image_url: Cartoon scene from Stage 1
            child_photo_urls: List of child's real photos (will select best for swap)
            expression_prompt: Optional expression guidance (e.g., "happy, smiling")
            preview_id: For R2 storage path
            page_number: For R2 storage path

        Returns:
            Dict with success status and image URL (from R2)
        """
        start_time = time.time()

        try:
            # Select best photo for face swap
            # Photos arrive pre-sorted by quality score (best first from upload endpoint)
            best_photo_url = child_photo_urls[0] if child_photo_urls else None
            if not best_photo_url:
                return {"success": False, "error": "No photo URLs provided for face swap"}

            logger.info(f"Using best photo (1/{len(child_photo_urls)}) for face swap",
                       selected_url=best_photo_url[:60] if best_photo_url else None)
            logger.info(
                "Stage 2: Segmind face swap starting",
                expression=expression_prompt[:50] if expression_prompt else "natural",
                scene_url=scene_image_url[:60] if scene_image_url else None
            )

            # Deterministic per-page seed: varies by page so different pages use different
            # noise patterns, avoiding clashes with variable Stage 1 outputs.
            # preview_id + page_number gives a unique but reproducible seed.
            page_seed = int(hashlib.md5(f"{preview_id}_{page_number}_stage2".encode()).hexdigest()[:8], 16) % 2147483647

            payload = {
                "source_image": best_photo_url,     # Selected child's real face
                "target_image": scene_image_url,    # Cartoon scene
                "face_strength": 0.85,              # High identity preservation
                "style_strength": 0.75,             # Adapt to cartoon style
                "cfg": 2.0,                         # Increased from 1.6 — stronger guidance, less artifacts
                "steps": 25,                        # Increased from 15 — more steps = more stable face reconstruction
                "output_format": "png",
                "output_quality": 95,
                "seed": page_seed,                  # Per-page deterministic seed (not fixed 42)
                "base64": False                     # Get raw bytes
            }

            # Only add expression prompt if not empty
            if expression_prompt:
                payload["prompt"] = expression_prompt

            # Retry up to 2 attempts on timeout (Segmind can be slow under load)
            max_attempts = 2
            last_error = None
            response = None

            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        wait_secs = 5 * attempt
                        logger.warning(f"Stage 2 retry {attempt}/{max_attempts - 1} after {wait_secs}s wait")
                        await asyncio.sleep(wait_secs)

                    # Use separate connect vs read timeouts — connect should be fast,
                    # but read can be slow since Segmind processes the image server-side
                    timeout = httpx.Timeout(connect=10.0, read=150.0, write=30.0, pool=10.0)
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.post(
                            self.segmind_endpoint,
                            headers={
                                "x-api-key": self.settings.segmind_api_key,
                                "Content-Type": "application/json"
                            },
                            json=payload
                        )
                    break  # Success — exit retry loop

                except (httpx.ReadTimeout, httpx.ConnectTimeout) as timeout_err:
                    last_error = timeout_err
                    logger.warning(
                        f"Stage 2 timeout on attempt {attempt + 1}/{max_attempts}",
                        error=str(timeout_err),
                        attempt=attempt + 1
                    )
                    if attempt == max_attempts - 1:
                        raise  # Re-raise on final attempt

            if response is None:
                raise last_error or RuntimeError("Segmind face swap failed with no response")

            latency = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                # Segmind returns raw image bytes
                image_bytes = response.content

                if not image_bytes or len(image_bytes) < 1000:
                    error_msg = f"Segmind returned invalid image data (size: {len(image_bytes) if image_bytes else 0})"
                    logger.error("Stage 2 failed - invalid response", error=error_msg)
                    return {"success": False, "error": error_msg, "latency_ms": latency}

                # Upload directly to final/ location (avoids double upload)
                storage_path = f"final/{preview_id}/page_{page_number:02d}.png"
                r2_url = await self.storage.upload_image(
                    image_bytes,
                    storage_path,
                    content_type="image/png"
                )

                logger.info(
                    "Stage 2 complete: Face swapped and uploaded to R2",
                    latency_ms=latency,
                    r2_url=r2_url[:80] if r2_url else None,
                    image_size_bytes=len(image_bytes)
                )

                return {
                    "success": True,
                    "image_url": r2_url,
                    "latency_ms": latency
                }
            else:
                error_msg = f"Segmind error: {response.status_code} - {response.text[:300]}"
                logger.error("Stage 2 failed", error=error_msg, status_code=response.status_code)
                return {"success": False, "error": error_msg, "latency_ms": latency}

        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            logger.error("Stage 2 exception", error=str(e), exc_info=True)
            return {"success": False, "error": str(e), "latency_ms": latency}

    async def generate_with_face_analysis(
        self,
        prompt: str,
        face_url: List[str],  # Changed to support multiple reference images
        child_name: str,
        child_age: int,
        child_gender: str,
        analyzed_features: Optional[str] = None,
        aspect_ratio: str = "1:1",
        seed: Optional[int] = None,
        scene_type: str = "",
        preview_id: str = "",
        page_number: int = 0,
        face_expression: str = ""
    ) -> GenerationResult:
        """
        Generate a single illustrated page with the child's face.

        Two-stage process:
        1. Generate cartoon scene with placeholder child (NanoBanana)
        2. Face swap to insert real child's face (Segmind)

        Args:
            prompt: Scene description
            face_url: Child's reference photo URL
            child_name: Child's name for prompt personalization
            child_age: Child's age
            child_gender: 'male' or 'female'
            analyzed_features: Not used in two-stage (face comes from photo directly)
            aspect_ratio: Image aspect ratio (default "1:1" square)
            seed: Optional seed for reproducibility
            scene_type: Scene type for expression mapping
            preview_id: Preview ID for storage
            page_number: Page number for storage

        Returns:
            GenerationResult with final image
        """
        start_time = time.time()

        try:
            # Build scene prompt with placeholder child
            scene_prompt = self._build_scene_prompt(
                prompt, child_name, child_age, child_gender
            )

            # ==========================================
            # STAGE 1: Generate cartoon scene
            # ==========================================
            # Use deterministic seed if none passed: ensures same page always produces
            # same Stage 1 output, making failures reproducible and fixable per-page.
            stage1_seed = seed
            if stage1_seed is None and preview_id:
                stage1_seed = int(hashlib.md5(f"{preview_id}_{page_number}_stage1".encode()).hexdigest()[:8], 16) % 2147483647

            scene_result = await self._generate_scene(
                prompt=scene_prompt,
                face_url=face_url,
                aspect_ratio=aspect_ratio,
                seed=stage1_seed
            )

            if not scene_result.get("success"):
                return GenerationResult(
                    success=False,
                    error_message=f"Stage 1 (scene) failed: {scene_result.get('error')}",
                    latency_ms=int((time.time() - start_time) * 1000),
                    model_used=self.model_name
                )

            scene_url = scene_result["image_url"]

            # ==========================================
            # GET EXPRESSION PROMPT
            # Priority: page-level face_expression > EXPRESSION_MAP > keyword fallback
            # ==========================================
            if face_expression:
                expression_prompt = face_expression
                logger.info(
                    "Expression from page template (face_expression)",
                    page_number=page_number,
                    expression=expression_prompt
                )
            else:
                expression_prompt = get_expression_for_scene(scene_type, prompt)
                logger.info(
                    "Expression from EXPRESSION_MAP fallback",
                    scene_type=scene_type,
                    expression=expression_prompt if expression_prompt else "natural (from photo)"
                )

            # ==========================================
            # STAGE 2: Face swap with Segmind
            # ==========================================
            swap_result = await self._face_swap_segmind(
                scene_image_url=scene_url,
                child_photo_urls=face_url,  # Pass all photos
                expression_prompt=expression_prompt,
                preview_id=preview_id,
                page_number=page_number
            )

            if not swap_result.get("success"):
                # Face swap failure is a HARD failure
                # We must NEVER show a scene without the child's actual face
                logger.error(
                    "Face swap failed - cannot show scene without child's face",
                    error=swap_result.get("error")
                )
                return GenerationResult(
                    success=False,
                    error_message=f"Face swap failed: {swap_result.get('error')}. Cannot generate page without child's face.",
                    latency_ms=int((time.time() - start_time) * 1000),
                    model_used=self.model_name
                )

            # Success - use the final image with child's face
            final_url = swap_result["image_url"]
            total_latency = int((time.time() - start_time) * 1000)

            # Cost: NanoBanana (~$0.04) + Segmind (~$0.07)
            estimated_cost = 0.11

            logger.info(
                "Two-stage generation complete",
                total_latency_ms=total_latency,
                stage1_latency=scene_result.get("latency_ms"),
                stage2_latency=swap_result.get("latency_ms"),
                expression_used=expression_prompt if expression_prompt else "natural"
            )

            return GenerationResult(
                success=True,
                image_url=final_url,
                latency_ms=total_latency,
                model_used=self.model_name,
                cost=estimated_cost,
                metadata={
                    "seed": scene_result.get("seed"),
                    "aspect_ratio": aspect_ratio,
                    "scene_type": scene_type,
                    "expression_prompt": expression_prompt,
                    "stage1_url": scene_url,
                    "stage1_latency_ms": scene_result.get("latency_ms"),
                    "stage2_latency_ms": swap_result.get("latency_ms")
                }
            )

        except Exception as e:
            error_msg = f"Two-stage generation failed: {str(e)}"
            logger.error(error_msg, error=e, exc_info=True)
            return GenerationResult(
                success=False,
                error_message=error_msg,
                latency_ms=int((time.time() - start_time) * 1000),
                model_used=self.model_name
            )

    async def generate_all_pages(
        self,
        story_pages: List[Dict[str, Any]],
        face_url: List[str],  # Changed to support multiple reference images
        child_name: str,
        child_age: int,
        child_gender: str,
        preview_id: str,
        testing_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Generate all story pages with two-stage approach.

        Args:
            story_pages: List of page data with prompts and scene_type
            face_url: List of child's reference photo URLs (1-3 images)
            child_name: Child's name
            child_age: Child's age
            child_gender: 'male' or 'female'
            preview_id: Preview ID for storage paths
            testing_mode: If True, generate only 5 pages

        Returns:
            Dict with successful pages and generation metadata
        """
        logger.info(
            "Starting batch two-stage generation",
            total_pages=len(story_pages),
            testing_mode=testing_mode,
            preview_id=preview_id
        )

        page_count = self.settings.testing_mode_pages if testing_mode else len(story_pages)
        pages_to_generate = story_pages[:page_count]

        successful_pages = []
        failed_pages = []
        total_cost = 0.0

        for i, page_data in enumerate(pages_to_generate):
            page_number = i + 1
            logger.info(f"Generating two-stage page {page_number}/{page_count}")

            try:
                # Get prompt from page data
                prompt = page_data.get("prompt", page_data.get("realistic_prompt", ""))
                if not prompt:
                    logger.warning(f"No prompt found for page {page_number}")
                    continue

                # Get scene_type for expression mapping
                scene_type = page_data.get("scene_type", "")

                result = await self.generate_with_face_analysis(
                    prompt=prompt,
                    face_url=face_url,
                    child_name=child_name,
                    child_age=child_age,
                    child_gender=child_gender,
                    scene_type=scene_type,
                    preview_id=preview_id,
                    page_number=page_number
                )

                if result.success:
                    # Image is already uploaded to final/ by _face_swap_segmind
                    # No need to re-upload
                    successful_pages.append({
                        "page_number": page_number,
                        "image_url": result.image_url,
                        "original_prompt": prompt,
                        "scene_type": scene_type,
                        "expression_used": result.metadata.get("expression_prompt", ""),
                        "latency_ms": result.latency_ms
                    })

                    total_cost += result.cost
                    logger.info(f"Two-stage page {page_number} generated successfully")
                else:
                    logger.error(f"Two-stage page {page_number} failed: {result.error_message}")
                    failed_pages.append({
                        "page_number": page_number,
                        "error": result.error_message
                    })

            except Exception as e:
                logger.error(f"Two-stage page {page_number} error", error=str(e))
                failed_pages.append({
                    "page_number": page_number,
                    "error": str(e)
                })

        logger.info(
            "Batch two-stage generation completed",
            successful_pages=len(successful_pages),
            failed_pages=len(failed_pages),
            total_cost=total_cost
        )

        return {
            "successful_pages": successful_pages,
            "failed_pages": failed_pages,
            "total_cost": total_cost,
            "analyzed_features": None,  # Not used in two-stage
            "testing_mode": testing_mode,
            "pages_generated": len(successful_pages)
        }

    def _build_scene_prompt(
        self,
        base_prompt: str,
        child_name: str,
        child_age: int,
        child_gender: str
    ) -> str:
        """
        Build scene prompt with placeholder child character.

        Face visibility is CRITICAL for Stage 2 face swap to work.
        """
        # Replace {name} tokens
        personalized_prompt = base_prompt.replace("{name}", child_name)

        # Gender word
        gender_word = "boy" if child_gender.lower() == "male" else "girl"

        return f"""Subject: A {child_age}-year-old {gender_word} named {child_name}.

Scene: {personalized_prompt}

CRITICAL FACE REQUIREMENTS (Essential for final result):
- The child's face MUST be clearly visible, facing the camera or at 3/4 angle
- Face must be well-lit with no shadows obscuring features
- Face should be prominent in the frame (not tiny in background)
- No objects blocking or covering the face
- Child's facial expression should match the scene emotion"""

    # Alias for compatibility with existing code
    async def analyze_face(self, face_image_url: str) -> str:
        """
        Face analysis - not needed for two-stage pipeline.

        The face comes directly from the reference photo in Stage 2.
        This method exists for interface compatibility.
        """
        return "Face analysis not used in two-stage pipeline - face comes from Segmind face swap"
