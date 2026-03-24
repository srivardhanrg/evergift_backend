"""
Check filler image dimensions using R2 credentials.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from PIL import Image
from io import BytesIO
from app.services.storage import StorageService
from app.config import get_settings

async def main():
    settings = get_settings()
    storage = StorageService()

    print("=" * 70)
    print(f"Checking filler images in R2 bucket: {settings.r2_bucket_name}")
    print("=" * 70)

    # Theme to check
    theme = "enchanted_forest"
    style = "photorealistic"

    # List of text filler images
    text_images = [f"text{i}.png" for i in range(1, 11)]

    results = []

    for filename in text_images:
        try:
            # Construct R2 key
            key = f"filler_images/{theme}/{style}/{filename}"

            # Download from R2
            image_bytes = storage.download_from_r2(key)

            # Open with PIL
            image = Image.open(BytesIO(image_bytes))
            width, height = image.size

            print(f"✓ {filename:15s} → {width:5d}×{height:5d}px")
            results.append((filename, width, height))

        except Exception as e:
            print(f"✗ {filename:15s} → ERROR: {str(e)}")
            results.append((filename, None, None))

    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)

    # Check dimensions
    valid_results = [(f, w, h) for (f, w, h) in results if w is not None]

    if not valid_results:
        print("❌ Could not read any images!")
        return

    dimensions = [(w, h) for (_, w, h) in valid_results]
    unique_dims = set(dimensions)

    if len(unique_dims) == 1:
        w, h = dimensions[0]
        print(f"✅ ALL CONSISTENT: All images are {w}×{h}px")
        if w == 3000 and h == 3000:
            print("   Perfect! This is the expected size for 300 DPI print quality.")
        else:
            print(f"   ⚠ Expected: 3000×3000px for best quality")
            print(f"   ⚠ Actual:   {w}×{h}px")
    else:
        print("❌ INCONSISTENT DIMENSIONS DETECTED!")
        print("\nDimensions by image:")
        for filename, w, h in valid_results:
            print(f"   {filename:15s} → {w}×{h}px")

        print("\n⚠ THIS IS THE ROOT CAUSE OF YOUR TEXT INCONSISTENCY!")
        print("   Different image sizes cause text to wrap differently.")
        print("\n💡 FIX: Resize all images to 3000×3000px")

    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
