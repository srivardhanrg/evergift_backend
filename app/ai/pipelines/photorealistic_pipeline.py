"""
Photorealistic Pipeline - Identity-preserving photorealistic generation.

Uses fal.ai nano-banana model with VLM face analysis:
- VLM face analysis using LLaVA-Next
- Identity-preserving generation with face embedding
- Sequential generation to avoid API limits
- 5:4 aspect ratio optimized for print
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
    1. Analyze child's face using LLaVA-Next VLM
    2. Generate each page with face analysis + scene prompt
    3. Sequential generation to avoid API concurrency limits
    4. Store results in cloud storage
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
        self.model_id = "fal-ai/nano-banana/edit"
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
        face_url: str,
        child_name: str,
        child_age: int,
        child_gender: str,
        analyzed_features: Optional[str] = None,
        aspect_ratio: str = "5:4",
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
            aspect_ratio: Image aspect ratio (default 5:4 for pages, 1:1 for covers)
            seed: Random seed for generation

        Returns:
            GenerationResult with image URL and metadata
        """
        start_time = time.time()

        try:
            if not analyzed_features:
                analyzed_features = await self.analyze_face(face_url)

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

            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "prompt": enhanced_prompt,
                    "image_urls": [face_url],
                    "aspect_ratio": aspect_ratio,
                    "negative_prompt": "black bars, letterbox, scope, cinema bars, blurry, low quality, distorted face",
                }

                if seed:
                    payload["seed"] = seed

                response = await client.post(
                    "https://fal.run/fal-ai/nano-banana/edit",
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
        # VLM FACE ANALYSIS - Enabled for production quality
        # Provides detailed facial description for identity preservation
        # ============================================================
        try:
            analyzed_features = await self.analyze_face(face_url)
            if analyzed_features == "a cute child":
                # VLM returned fallback, use enhanced generic anchor
                analyzed_features = "the child exactly as shown in the reference photo, preserving all facial features, skin tone, hair, and ethnic characteristics"
                logger.warning("VLM returned fallback description, using generic anchor")
        except Exception as e:
            logger.error("VLM analysis failed, using fallback", error=str(e))
            analyzed_features = "the child exactly as shown in the reference photo, preserving all facial features, skin tone, hair, and ethnic characteristics"

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
        Build enhanced prompt with facial analysis, age, and gender.

        Layers prompt structure:
        - Subject + Age + Gender + Appearance
        - Scene Action
        - Style constraints
        """
        personalized_prompt = base_prompt.replace("{name}", child_name)

        # Convert gender to boy/girl for natural language
        gender_word = "boy" if child_gender.lower() == "male" else "girl"

        enhanced_prompt = f"""Subject: A {child_age}-year-old {gender_word} named {child_name}.
Appearance: {analyzed_features}.
CRITICAL SKIN TONE: Accurately render the child's EXACT skin tone as described above - do not lighten, darken, or change skin color regardless of lighting conditions (golden light, moonlight, magical glow, etc.). Preserve authentic skin tone and ethnic features even in bright, dramatic, or colored lighting. The lighting should enhance features without altering natural complexion.
Age-specific features: Render with age-appropriate facial proportions and features for a {child_age}-year-old {gender_word}.

Scene Action: {personalized_prompt}.

Environment: Masterpiece, 8k resolution, photorealistic, intricate details, sharp focus, ray tracing, soft volumetric lighting.

Style: an award-winning cinematic photograph, hyper-realistic, highly detailed skin texture, 8k resolution, deep depth of field, sharp background, soft natural lighting, shot on 35mm film.

Constraint: identical character face, consistent clothing, perfect face integration, age-appropriate proportions, authentic skin tone preservation."""

        return enhanced_prompt