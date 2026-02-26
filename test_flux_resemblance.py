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

# Global variable to hold the uploaded URL
TEST_FACE_URL = None 

CHILD_NAME = "Leo"
CHILD_GENDER = "boy"

# ------------------------------------------------------------------
# AGGRESSIVE IDENTITY PROMPT
# ------------------------------------------------------------------
# Removed almost all style words that could warp the face.
# Kept only high-quality rendering keywords.
PROMPT = f"""
A high-fidelity 3D render of {CHILD_NAME}, a {CHILD_GENDER} wearing pajamas, standing in a magical backyard.
The face is identical to the reference photo.
soft lighting, 8k, photorealistic textures, octane render, raytracing.
"""

async def generate_aggressive_identity_test():
    print(f"Generating AGGRESSIVE Identity test for {CHILD_NAME}...")
    
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
        # TEST 1: Flux PuLID with HIGH WEIGHT
        print("Testing: Fal.ai Flux PuLID (id_weight=1.0)...")
        args = {
                "prompt": PROMPT,
                "images": [{"image_url": TEST_FACE_URL}],
                # "pulid_mode": "fidelity",
                # "id_weight": 1.0,     # COMMENTED OUT FOR DEBUG
                "guidance_scale": 4.0, 
                "num_inference_steps": 30,
                "enable_safety_checker": False
            }
        print(f"DEBUG ARGS: {args}")
        
        handler = await fal_client.submit_async(
            "fal-ai/flux-pulid",
            arguments=args,
        )
        result = await handler.get()
        if result and "images" in result and len(result["images"]) > 0:
            url = result['images'][0]['url']
            print(f"[SUCCESS] Result 1 (High Weight): {url}")
            with open("final_results.txt", "a") as f:
                f.write(f"RESEMBLANCE_1: {url}\n")
        else:
            print("[FAIL] Result 1 Failed")

        print("-" * 50)
        
        # TEST 2: Flux PuLID with MAX WEIGHT & LOWER CFG
        print("Testing: Fal.ai Flux PuLID (id_weight=1.0, Low CFG)...")
        handler_2 = await fal_client.submit_async(
            "fal-ai/flux-pulid",
            arguments={
                "prompt": PROMPT,
                "images": [{"image_url": TEST_FACE_URL}],
                "pulid_mode": "fidelity",
                "id_weight": 1.0,     # MAXIMUM ALLOWED
                "guidance_scale": 2.5, # Lower guidance allows more ID influence
                "num_inference_steps": 30,
                "enable_safety_checker": False
            },
        )
        result_2 = await handler_2.get()
        if result_2 and "images" in result_2 and len(result_2["images"]) > 0:
            url = result_2['images'][0]['url']
            print(f"[SUCCESS] Result 2 (Max Weight): {url}")
            with open("final_results.txt", "a") as f:
                f.write(f"RESEMBLANCE_2: {url}\n")
        else:
            print("[FAIL] Result 2 Failed")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure you have FAL_KEY set in your environment
    # os.environ["FAL_KEY"] = "your_key_here"
    asyncio.run(generate_aggressive_identity_test())
