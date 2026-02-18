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

# Local file path provided by user
LOCAL_FACE_PATH = r"C:\Users\santh\Pictures\Screenshots\Screenshot 2026-01-20 001207.png"

# Global variable for URL
TEST_FACE_URL = None 

CHILD_NAME = "Leo"
CHILD_GENDER = "boy"

# ------------------------------------------------------------------
# PAINTERLY / DIGITAL ART STYLE PROMPT (Matching Reference)
# ------------------------------------------------------------------
# "2.5D" / Digital Painting Style. 
# Soft lighting, vibrant colors, NO "shiny" 3D plastic look.
# BUT we keep "high fidelity" for facial structure.

PROMPT = f"""
A beautiful digital painting of a happy {CHILD_NAME}, a cute {CHILD_GENDER} standing in a sunny garden with a cozy house in the background.
{CHILD_NAME} is wearing a simple t-shirt and jeans, hands in pockets, smiling warmly at the camera.
The face is identical to the provided reference photo.

[Style Modifiers]
Stylized digital art, semi-realistic painting, vibrant colors, soft smooth shading, dreamlike atmosphere, detailed background, blue sky with fluffy clouds, sun rays, artstation style, concept art, high definition.
(NOT 3d render, NOT plastic, NOT shiny, NOT photorealistic)
"""

async def generate_painterly_test():
    print(f"Generating PAINTERLY/DIGITAL ART style test for {CHILD_NAME}...")
    
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
        return

    print(f"Using Face URL: {TEST_FACE_URL}")
    print("-" * 50)
    
    try:
        # TEST 1: BALANCED BLEND (Strong ID + Painterly Style)
        print("Testing: Fal.ai Flux PuLID (id_weight=1.2, fidelity)...")
        handler = await fal_client.submit_async(
            "fal-ai/flux-pulid",
            arguments={
                "prompt": PROMPT,
                "images": [{"image_url": TEST_FACE_URL}],
                "pulid_mode": "fidelity",
                "id_weight": 1.2,      # Still strong ID, but allow style to bleed in
                "guidance_scale": 3.5, # Moderate guidance for artistic freedom
                "num_inference_steps": 28,
                "enable_safety_checker": False
            },
        )
        result = await handler.get()
        if result and "images" in result and len(result["images"]) > 0:
            url = result['images'][0]['url']
            print(f"[SUCCESS] Result 1 (Painterly Style): {url}")
            with open("final_results.txt", "a") as f:
                f.write(f"PAINTERLY: {url}\n")
        else:
            print("[FAIL] Result 1 Failed")
            
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")

if __name__ == "__main__":
    # Ensure you have FAL_KEY set in your environment
    asyncio.run(generate_painterly_test())
