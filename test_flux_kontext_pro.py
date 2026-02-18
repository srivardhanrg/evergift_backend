"""
Test Flux Kontext Pro - Cartoon Style with Face Identity Preservation

This tests the fal-ai/flux-pro/kontext model which can:
- Transform a photo into cartoon style
- Preserve the person's face identity across the transformation
- Support Disney, Pixar, Anime, Ghibli styles natively

Cost: ~$0.04 per image
"""

import os
import sys
import asyncio

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import get_settings

# Set FAL_KEY from app settings
settings = get_settings()
os.environ["FAL_KEY"] = settings.fal_api_key

import fal_client

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
LOCAL_FACE_PATH = r"C:\Users\santh\Pictures\Screenshots\Screenshot 2026-01-20 001207.png"

CHILD_NAME = "Leo"
CHILD_AGE = 5
CHILD_GENDER = "boy"

# Global variable for uploaded URL
TEST_FACE_URL = None


# ------------------------------------------------------------------
# PROMPTS TO TEST - Each targets a different cartoon style
# ------------------------------------------------------------------
PROMPTS = [
    {
        "name": "Pixar 3D Cartoon",
        "prompt": (
            f"Transform this photo into a premium Pixar-style 3D cartoon illustration. "
            f"The child should look like a Pixar movie character with the EXACT SAME facial features, "
            f"hair style, and skin tone as the original photo. "
            f"3D rendered, smooth skin, big expressive eyes, warm lighting, "
            f"magical enchanted forest background with glowing fireflies and ancient trees. "
            f"The child is wearing a cute adventurer outfit with a small cape. "
            f"Children's book illustration quality, vibrant saturated colors, "
            f"cinematic lighting, shallow depth of field. "
            f"CRITICAL: Preserve the child's exact face - same nose shape, eye shape, and facial structure."
        ),
    },
    {
        "name": "Studio Ghibli Style",
        "prompt": (
            f"Transform this photo into a beautiful Studio Ghibli anime-style illustration. "
            f"Keep the child's EXACT facial features, hair, and skin tone from the original photo. "
            f"Soft watercolor-like backgrounds, hand-painted feel, warm golden hour lighting. "
            f"The child is sitting on a grassy hilltop overlooking a magical valley "
            f"with floating islands and a gentle breeze blowing through wildflowers. "
            f"Miyazaki-inspired art style, dreamy atmosphere, detailed scenery. "
            f"Premium children's book illustration, print-ready quality."
        ),
    },
    {
        "name": "Disney 2D Illustration",
        "prompt": (
            f"Transform this photo into a classic Disney-style 2D cartoon illustration. "
            f"The child must have the IDENTICAL face, hair color, skin tone, and facial proportions "
            f"as in the original photo - do not change any facial features. "
            f"Vibrant cel-shaded colors, clean lines, warm inviting atmosphere. "
            f"Scene: The child is discovering a treasure map in a cozy sunlit bedroom, "
            f"eyes wide with excitement, holding the magical map that glows with golden light. "
            f"Toys scattered around, warm morning sunlight streaming through the window. "
            f"Professional children's book quality, rich color palette."
        ),
    },
]


async def upload_face_image():
    """Upload local face image to fal.ai CDN."""
    global TEST_FACE_URL

    if not os.path.exists(LOCAL_FACE_PATH):
        print(f"[ERROR] File not found: {LOCAL_FACE_PATH}")
        print("Please update LOCAL_FACE_PATH to your child's photo.")
        return False

    print(f"[UPLOAD] Uploading {os.path.basename(LOCAL_FACE_PATH)} to fal.ai CDN...")
    try:
        url = fal_client.upload_file(LOCAL_FACE_PATH)
        TEST_FACE_URL = url
        print(f"[SUCCESS] Uploaded: {url[:80]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return False


async def test_kontext_pro(prompt_config):
    """Test Flux Kontext Pro with a specific prompt."""
    name = prompt_config["name"]
    prompt = prompt_config["prompt"]

    print(f"\n{'='*60}")
    print(f"  TEST: {name}")
    print(f"{'='*60}")
    print(f"[PROMPT] {prompt[:120]}...")
    print(f"[MODEL] fal-ai/flux-pro/kontext")
    print(f"[COST] ~$0.04")
    print(f"[GENERATING] Please wait (10-30 seconds)...")

    try:
        result = fal_client.subscribe(
            "fal-ai/flux-pro/kontext",
            arguments={
                "prompt": prompt,
                "image_url": TEST_FACE_URL,
            },
        )

        # Extract image URL from result
        if result and result.get("images"):
            image_url = result["images"][0].get("url", "No URL")
            print(f"\n[SUCCESS] {name}")
            print(f"[IMAGE URL] {image_url}")

            # Save to results file
            with open("kontext_pro_results.txt", "a", encoding="utf-8") as f:
                f.write(f"\n--- {name} ---\n")
                f.write(f"URL: {image_url}\n")
                f.write(f"Prompt: {prompt[:200]}\n\n")

            return image_url
        else:
            print(f"[FAIL] No images in response")
            print(f"[RESPONSE] {str(result)[:300]}")
            return None

    except Exception as e:
        print(f"\n[ERROR] {name} failed: {e}")
        return None


async def main():
    print("=" * 60)
    print("  FLUX KONTEXT PRO - Cartoon Face Identity Test")
    print("  Model: fal-ai/flux-pro/kontext")
    print("  Cost: ~$0.04 per image (3 tests = ~$0.12 total)")
    print("=" * 60)

    # Step 1: Upload reference image
    if not await upload_face_image():
        return

    # Clear previous results
    with open("kontext_pro_results.txt", "w", encoding="utf-8") as f:
        f.write("FLUX KONTEXT PRO TEST RESULTS\n")
        f.write(f"Reference: {LOCAL_FACE_PATH}\n")
        f.write(f"Face URL: {TEST_FACE_URL}\n")
        f.write("=" * 40 + "\n")

    # Step 2: Run all prompt tests
    results = []
    for prompt_config in PROMPTS:
        url = await test_kontext_pro(prompt_config)
        results.append({"name": prompt_config["name"], "url": url})

    # Summary
    print(f"\n\n{'='*60}")
    print("  RESULTS SUMMARY")
    print(f"{'='*60}")
    for r in results:
        status = "[OK]" if r["url"] else "[FAILED]"
        print(f"  {status} {r['name']}")
        if r["url"]:
            print(f"       {r['url']}")
    print(f"\nAll URLs saved to: kontext_pro_results.txt")
    print(f"Open each URL in your browser to compare face resemblance + cartoon quality.")


if __name__ == "__main__":
    asyncio.run(main())
