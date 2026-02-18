import os
import asyncio
import fal_client
from app.config import get_settings

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
# Set FAL_KEY from app settings
settings = get_settings()
os.environ["FAL_KEY"] = settings.fal_api_key

# Local file path provided by user - using raw string to handle backslashes
LOCAL_FACE_PATH = r"C:\Users\santh\Pictures\Screenshots\Screenshot 2026-01-20 001207.png"

CHILD_NAME = "Leo"
CHILD_GENDER = "boy"

# Global variable to hold the uploaded URL
TEST_FACE_URL = None

# ------------------------------------------------------------------
# PROMPT (Scenery Focused)
# ------------------------------------------------------------------
# The user wants "Kontext Pro" level scenery.
# We focus on the ENVIRONMENT description.
PROMPT = f"""
[Subject]
{CHILD_NAME}, a cute {CHILD_GENDER} wearing pajamas.

[Environment - High Definition Scenery]
A breathtaking majestic garden at twilight. Bioluminescent plants glowing in deep blues and purples. 
A hyper-detailed silver rocket ship with complex mechanical details reflecting the moonlight.
In the background, a cozy cottage with warm yellow windows. 
Fireflies creating light trails.
Deep depth of field, sharp focus on background elements.

[Style]
Cinematic composition, rule of thirds, wide angle shot, concept art, unreel engine 5 render, vibrant colors, atmospheric fog.
(Detailed environment, perfect facial integration)
"""

async def generate_kontext_test():
    print(f"Generating Flux Kontext/Pro test for {CHILD_NAME}...")
    
    # 1. Upload the local file to get a URL
    global TEST_FACE_URL
    if os.path.exists(LOCAL_FACE_PATH):
        print(f"Uploading local reference image: {LOCAL_FACE_PATH}...")
        try:
            TEST_FACE_URL = fal_client.upload_file(LOCAL_FACE_PATH)
            print(f"Upload successful: {TEST_FACE_URL}")
        except Exception as e:
            print(f"❌ Failed to upload file: {e}")
            return
    else:
        print(f"❌ Local file not found: {LOCAL_FACE_PATH}")
        # Fallback for testing if local file fails - usage of a placeholder or exit
        return

    try:
        # TEST: Fal.ai Flux Pro v1.1 (The "Kontext" equivalent for high-end scenes)
        # Note: Flux Pro on Fal typically uses 'image_prompts' slightly differently or strictly for img2img.
        # But for Identity, 'flux-pulid' is still the KING.
        # However, let's try calling the Pro endpoint with image prompts if supported, 
        # OR fallback to a high-step Dev generation which mimics Pro.
        
        # User specifically asked for "Kontext Pro". 
        # On Replicate this is 'black-forest-labs/flux-kontext-pro'.
        # On Fal, it's often mapped to 'fal-ai/flux-pro/v1.1' or similar high-end endpoints.
        
        print("Testing: Fal.ai Flux Pro v1.1 (Ultra Scenery)...")
        handler = await fal_client.submit_async(
            "fal-ai/flux-pro/v1.1",  # High-end scaffolding
            arguments={
                "prompt": PROMPT,
                # Flux Pro v1.1 doesn't always support direct ID injection like PuLID.
                # If this fails to capture ID, we know why (it's a trade-off).
                # But let's try standard image_prompts if the API allows.
                # Use 'safety_tolerance' to allow more creative freedom.
                "safety_tolerance": "2",
                "image_prompts": [
                    {
                        "image_url": TEST_FACE_URL,
                        "weight": 1.0 # Attempting soft injection
                    }
                ]
            },
        )
        result = await handler.get()
        if result and "images" in result and len(result["images"]) > 0:
            url = result['images'][0]['url']
            print(f"[SUCCESS] Result (Flux Pro 1.1): {url}")
            with open("final_results.txt", "a") as f:
                f.write(f"KONTEXT_SCENE: {url}\n")
        else:
            print("[FAIL] Result Failed")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("Note: Flux Pro v1.1 might not support 'image_prompts' strictly for identity.")

if __name__ == "__main__":
    asyncio.run(generate_kontext_test())
