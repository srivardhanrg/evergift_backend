import os
import asyncio
import fal_client

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
# Replace with a valid image URL of a child for testing
TEST_FACE_URL = "https://storage.googleapis.com/falserverless/model_tests/flux/pulid/child_face.png" 
# Example URL, please replace with actual child photo

CHILD_NAME = "Leo"
CHILD_GENDER = "boy"

# ------------------------------------------------------------------
# IMAGITIME STYLE PROMPT (Flux Optimized)
# ------------------------------------------------------------------
# We use the "Cosmic Dreamer" Page 1 scene but enhance it for 3D/Pixar style.
PROMPT = f"""
[Subject]
A high-quality 3D render of a cute {CHILD_GENDER} named {CHILD_NAME}, approximately 5 years old, wearing comfortable pajamas.

[Scene & Action]
{CHILD_NAME} stands in a magical backyard at twilight, looking up in pure awe and excitement at a magnificent silver and blue rocket ship. The rocket has a gentle neon glow and a glass dome showing a cozy interior.

[Environment]
Fireflies are dancing in the air. A warmly lit house is visible in the background. The sky is a dreamy gradient of purple and pink sunset colors.

[Style & Quality - Imagitime/Pixar Style]
3d render, cgi, disney animation style, pixar style, cute, stylized 3d, octane render, volumetric lighting, magical atmosphere, high detail, 8k, masterpiece, shallow depth of field, soft warm lighting, subsurface scattering on skin.
"""

async def generate_imagitime_test():
    print(f"Generating Imagitime-style image for {CHILD_NAME}...")
    print(f"Using Face URL: {TEST_FACE_URL}")
    
    try:
        # Using fal-ai/flux-pulid for maximum identity preservation + Flux quality
        handler = await fal_client.submit_async(
            "fal-ai/flux-pulid",
            arguments={
                "prompt": PROMPT,
                "images": [
                    {
                        "image_url": TEST_FACE_URL
                    }
                ],
                "pulid_mode": "fidelity", # or "style" - fidelity is better for ID
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "enable_safety_checker": False
            },
        )
        
        result = await handler.get()
        
        if result and "images" in result and len(result["images"]) > 0:
            print("\n✅ Generation Successful!")
            print(f"Image URL: {result['images'][0]['url']}")
        else:
            print("\n❌ Generation Failed: No images returned.")
            print(result)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Ensure you have FAL_KEY set in your environment
    # os.environ["FAL_KEY"] = "your_key_here"
    asyncio.run(generate_imagitime_test())
