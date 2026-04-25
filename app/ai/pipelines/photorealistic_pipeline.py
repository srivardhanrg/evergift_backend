"""
Photorealistic Pipeline - Identity-preserving photorealistic generation.

Uses fal.ai nano-banana model with image reference:
- Identity-preserving generation via image_urls parameter
- nano-banana extracts identity directly from reference photo
- Sequential generation to avoid API limits
- 5:4 aspect ratio optimized for print

NOTE: VLM face analysis has been disabled (2024-01).
Research showed that nano-banana preserves identity from image reference alone,
and text descriptions can conflict with image data, reducing quality.
The model extracts facial features directly from the reference image.
"""

import time
import structlog
from typing import Optional, Dict, List, Any
import httpx

from app.ai.base import GenerationResult
from app.services.storage import StorageService
from app.config import get_settings

logger = structlog.get_logger()


class PhotorealisticPipeline:
    """
    Photorealistic pipeline for identity-preserving image generation.

    Flow:
    1. Use static identity lock prompt (VLM disabled - see module docstring)
    2. Generate each page with identity prompt + scene prompt + image reference
    3. Sequential generation to avoid API concurrency limits
    4. Store results in cloud storage

    Identity preservation is handled by nano-banana's image_urls parameter,
    which extracts facial features directly from the reference photo.
    """

    def __init__(self, model_override: Optional[str] = None):
        """
        Initialize photorealistic pipeline.

        Args:
            model_override: Optional model override
        """
        self.settings = get_settings()
        self.storage = StorageService()

        # Model configuration
        self.model_id = "openai/gpt-image-2"
        self.model_name = "photorealistic"

        logger.info(
            "Photorealistic pipeline initialized",
            model_id=self.model_id,
            testing_mode=self.settings.testing_mode_enabled
        )

    async def analyze_face(self, face_image_url: str) -> str:
        """
        Analyze child's face using LLaVA-Next VLM.

        Extracts detailed facial features for consistent generation.

        Args:
            face_image_url: URL of child's reference photo

        Returns:
            Detailed facial description string
        """
        try:
            logger.info("Starting VLM face analysis", image_url=face_image_url)
            start_time = time.time()

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://fal.run/fal-ai/llava-next",
                    headers={
                        "Authorization": f"Key {self.settings.fal_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "image_url": face_image_url,
                        "prompt": "Describe the child's face in precise detail: EXACT skin tone (light/medium/dark/very dark brown, or pale/beige/tan/olive), facial structure, hair color and texture (straight/wavy/curly/kinky), eye color and shape, nose shape, cheek fullness, and any distinctive features like bindi, moles, or facial marks. Be very specific about skin tone - describe it accurately using brown/tan/beige/olive/pale descriptors. Include ethnic features if visible (South Asian, East Asian, African, etc.). Do not describe clothing or background. Example: 'a young child with medium-dark brown South Asian skin tone, round full cheeks, small nose, curly dark brown hair, large expressive dark eyes, and a bindi on the forehead'.",
                        "max_tokens": 200
                    }
                )

            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception as json_err:
                    logger.error("VLM returned invalid JSON", error=str(json_err))
                    return "a cute child"

                analysis_result = result.get("output", "")

                latency = int((time.time() - start_time) * 1000)
                logger.info(
                    "VLM face analysis completed",
                    latency_ms=latency,
                    analysis_length=len(analysis_result)
                )

                return analysis_result or "a cute child"
            else:
                logger.error(
                    "VLM analysis failed",
                    status_code=response.status_code,
                    response=response.text[:200] if response.text else "No response"
                )
                return "a cute child"

        except Exception as e:
            logger.error("VLM analysis error", error=str(e))
            return "a cute child"

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
        face_expression: str = "",
        **kwargs  # Accept extra params (scene_type, preview_id, etc.) from shared caller
    ) -> GenerationResult:
        """
        Generate single image with face analysis.

        Args:
            prompt: Scene description prompt
            face_url: Child's reference photo URL
            child_name: Child's name for prompt personalization
            child_age: Child's age for age-appropriate features
            child_gender: Child's gender ('male' or 'female')
            analyzed_features: Pre-analyzed facial features (optional)
            aspect_ratio: Image aspect ratio (default 1:1 for all pages)
            seed: Random seed for generation

        Returns:
            GenerationResult with image URL and metadata
        """
        start_time = time.time()

        try:
            # ============================================================
            # VLM ANALYSIS DISABLED - Using static identity lock prompt
            # Research: nano-banana extracts identity from image reference,
            # text descriptions can conflict with image data and reduce quality
            # ============================================================
            # if not analyzed_features:
            #     analyzed_features = await self.analyze_face(face_url)
            if not analyzed_features:
                analyzed_features = "the child exactly as shown in the reference photo, preserving all facial features, skin tone, hair texture, and ethnic characteristics with perfect accuracy"

            enhanced_prompt = self._build_enhanced_prompt(
                prompt, child_name, child_age, child_gender, analyzed_features
            )

            # Append page-specific expression to prompt for single-call photorealistic pipeline
            if face_expression:
                enhanced_prompt = enhanced_prompt.rstrip() + f"\n\nChild's facial expression: {face_expression}."

            logger.info(
                "Starting photorealistic generation",
                prompt_length=len(enhanced_prompt),
                child_name=child_name,
                face_expression=face_expression or "from prompt"
            )

            async with httpx.AsyncClient(timeout=300.0) as client:
                payload = {
                    "prompt": enhanced_prompt,
                    "image_urls": face_url,
                    "image_size": "square_hd",
                    "quality": "high",
                    "output_format": "jpeg",
                }

                if seed:
                    payload["seed"] = seed

                response = await client.post(
                    "https://fal.run/openai/gpt-image-2",
                    headers={
                        "Authorization": f"Key {self.settings.fal_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception as json_err:
                    return GenerationResult(
                        success=False,
                        error_message=f"API returned invalid JSON: {str(json_err)}",
                        latency_ms=int((time.time() - start_time) * 1000),
                        model_used=self.model_name
                    )

                images = result.get("images", [])

                if images and len(images) > 0:
                    image_url = images[0].get("url")

                    if not image_url:
                        return GenerationResult(
                            success=False,
                            error_message="API returned empty image URL",
                            latency_ms=int((time.time() - start_time) * 1000),
                            model_used=self.model_name
                        )

                    latency = int((time.time() - start_time) * 1000)

                    logger.info(
                        "Photorealistic generation successful",
                        latency_ms=latency,
                        image_url=image_url
                    )

                    return GenerationResult(
                        success=True,
                        image_url=image_url,
                        latency_ms=latency,
                        model_used=self.model_name,
                        cost=0.04,
                        metadata={
                            "analyzed_features": analyzed_features,
                            "seed": seed,
                            "aspect_ratio": aspect_ratio
                        }
                    )
                else:
                    return GenerationResult(
                        success=False,
                        error_message="No images returned from generation",
                        latency_ms=int((time.time() - start_time) * 1000),
                        model_used=self.model_name
                    )
            else:
                error_msg = f"Generation API error: {response.status_code}"
                logger.error(error_msg, response_text=response.text[:200] if response.text else "No response")

                return GenerationResult(
                    success=False,
                    error_message=error_msg,
                    latency_ms=int((time.time() - start_time) * 1000),
                    model_used=self.model_name
                )

        except Exception as e:
            error_msg = f"Photorealistic generation failed: {str(e)}"
            logger.error(error_msg, error=e)

            return GenerationResult(
                success=False,
                error_message=error_msg,
                latency_ms=int((time.time() - start_time) * 1000),
                model_used=self.model_name
            )

    async def generate_all_pages(
        self,
        story_pages: List[Dict[str, Any]],
        face_url: str,
        child_name: str,
        child_age: int,
        child_gender: str,
        preview_id: str,
        testing_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Generate all story pages sequentially.

        Args:
            story_pages: List of page data with prompts
            face_url: Child's reference photo URL
            child_name: Child's name
            child_age: Child's age
            child_gender: Child's gender ('male' or 'female')
            preview_id: Preview ID for storage paths
            testing_mode: If True, generate only 5 pages, else 10 pages

        Returns:
            Dict with successful pages and generation metadata
        """
        logger.info(
            "Starting batch page generation",
            total_pages=len(story_pages),
            testing_mode=testing_mode,
            preview_id=preview_id
        )

        page_count = self.settings.testing_mode_pages if testing_mode else len(story_pages)
        pages_to_generate = story_pages[:page_count]

        logger.info(f"Generating {page_count} pages in {'testing' if testing_mode else 'production'} mode")

        # ============================================================
        # VLM FACE ANALYSIS - DISABLED (2024-01)
        #
        # Research findings:
        # - nano-banana extracts identity directly from image reference
        # - Text descriptions can CONFLICT with image data, reducing quality
        # - "Text prompts introduce ambiguity: describing a face with words
        #    will never be as precise as showing the model exactly what you
        #    want through reference images"
        # - High-quality reference photos are more critical than text prompts
        #
        # Using static identity lock prompt instead. The model's image_urls
        # parameter handles identity preservation from the reference photo.
        # ============================================================
        # try:
        #     analyzed_features = await self.analyze_face(face_url)
        #     if analyzed_features == "a cute child":
        #         analyzed_features = "the child exactly as shown in the reference photo..."
        #         logger.warning("VLM returned fallback description, using generic anchor")
        # except Exception as e:
        #     logger.error("VLM analysis failed, using fallback", error=str(e))
        #     analyzed_features = "..."

        # Static identity lock prompt - relies on nano-banana's image reference capability
        analyzed_features = "the child exactly as shown in the reference photo, preserving all facial features, skin tone, hair texture, and ethnic characteristics with perfect accuracy"
        logger.info("Using static identity lock prompt (VLM disabled)")

        successful_pages = []
        failed_pages = []
        total_cost = 0.0

        for i, page_data in enumerate(pages_to_generate):
            page_number = i + 1
            logger.info(f"Generating page {page_number}/{page_count}")

            try:
                prompt = page_data.get("prompt", page_data.get("realistic_prompt", ""))
                if not prompt:
                    logger.warning(f"No prompt found for page {page_number}")
                    continue

                result = await self.generate_with_face_analysis(
                    prompt=prompt,
                    face_url=face_url,
                    child_name=child_name,
                    child_age=child_age,
                    child_gender=child_gender,
                    analyzed_features=analyzed_features
                )

                if result.success:
                    storage_path = f"final/{preview_id}/page_{page_number:02d}.jpg"
                    stored_url = await self.storage.download_and_upload(
                        result.image_url, storage_path, content_type="image/jpeg"
                    )

                    successful_pages.append({
                        "page_number": page_number,
                        "image_url": stored_url,
                        "original_prompt": prompt,
                        "latency_ms": result.latency_ms
                    })

                    total_cost += result.cost
                    logger.info(f"Page {page_number} generated successfully")
                else:
                    logger.error(f"Page {page_number} generation failed: {result.error_message}")
                    failed_pages.append({
                        "page_number": page_number,
                        "error": result.error_message
                    })

            except Exception as e:
                logger.error(f"Page {page_number} generation error", error=str(e))
                failed_pages.append({
                    "page_number": page_number,
                    "error": str(e)
                })

        logger.info(
            "Batch generation completed",
            successful_pages=len(successful_pages),
            failed_pages=len(failed_pages),
            total_cost=total_cost
        )

        return {
            "successful_pages": successful_pages,
            "failed_pages": failed_pages,
            "total_cost": total_cost,
            "analyzed_features": analyzed_features,
            "testing_mode": testing_mode,
            "pages_generated": len(successful_pages)
        }

    def _build_enhanced_prompt(
        self,
        base_prompt: str,
        child_name: str,
        child_age: int,
        child_gender: str,
        analyzed_features: str
    ) -> str:
        """
        Build enhanced prompt with identity lock and scene description.

        Layers prompt structure:
        - Subject + Age + Gender + Identity Lock
        - Scene Action
        - Style constraints

        Note: Identity preservation primarily handled by nano-banana's
        image_urls parameter. The text prompt reinforces but doesn't
        replace the image reference.
        """
        personalized_prompt = base_prompt.replace("{name}", child_name)

        # Convert gender to boy/girl for natural language
        gender_word = "boy" if child_gender.lower() == "male" else "girl"

        enhanced_prompt = f"""Subject: A {child_age}-year-old {gender_word} named {child_name}.

IDENTITY LOCK: {analyzed_features}. The child's face must EXACTLY match the reference image provided - same facial structure, same skin tone, same hair, same eyes, same nose, same ethnic features. DO NOT alter, idealize, or modify ANY facial characteristics.

CRITICAL SKIN TONE PRESERVATION: Render the child's EXACT skin tone from the reference photo - do not lighten, darken, or shift skin color regardless of lighting conditions (golden light, moonlight, magical glow, underwater light, etc.). Maintain authentic complexion even in dramatic or colored lighting. The lighting should enhance without altering natural skin tone.

Age-specific features: Render with age-appropriate facial proportions and features for a {child_age}-year-old {gender_word}.

Scene Action: {personalized_prompt}.

Environment: Masterpiece, 8k resolution, photorealistic, intricate details, sharp focus, ray tracing, soft volumetric lighting.

Style: an award-winning cinematic photograph, hyper-realistic, highly detailed skin texture, 8k resolution, deep depth of field, sharp background, soft natural lighting, shot on 35mm film.

Constraint: IDENTICAL face to reference image, consistent clothing, perfect face integration, age-appropriate proportions, authentic skin tone preservation, no face modifications."""

        return enhanced_prompt