"""
Quick script to check pixel dimensions of all filler images in R2.
Run this to see which images have inconsistent sizes.
"""

import asyncio
from PIL import Image
from io import BytesIO
import httpx

# R2 public URL
R2_PUBLIC_URL = "https://pub-ef61e5ccef7c48e48b8f9e9f537aba6e.r2.dev"

# Theme to check
THEME = "enchanted_forest"
STYLE = "photorealistic"

async def check_image_dimensions(url: str, name: str):
    """Download image and check dimensions."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            width, height = image.size

            print(f"✓ {name:20s} → {width}×{height}px")
            return (name, width, height)
    except Exception as e:
        print(f"✗ {name:20s} → ERROR: {str(e)}")
        return (name, None, None)

async def main():
    print("=" * 60)
    print(f"Checking filler images for: {THEME} / {STYLE}")
    print("=" * 60)

    # List of filler images to check
    images_to_check = [
        ("dedication.png", "Dedication Page"),
        ("intro1.png", "Intro Page 1"),
        ("intro2.png", "Intro Page 2"),
        ("text1.png", "Text Page 1"),
        ("text2.png", "Text Page 2"),
        ("text3.png", "Text Page 3"),
        ("text4.png", "Text Page 4"),
        ("text5.png", "Text Page 5"),
        ("text6.png", "Text Page 6"),
        ("text7.png", "Text Page 7"),
        ("text8.png", "Text Page 8"),
        ("text9.png", "Text Page 9"),
        ("text10.png", "Text Page 10"),
        ("end.png", "End Page"),
        ("back.png", "Back Cover"),
    ]

    results = []
    for filename, label in images_to_check:
        url = f"{R2_PUBLIC_URL}/filler_images/{THEME}/{STYLE}/{filename}"
        result = await check_image_dimensions(url, label)
        results.append(result)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Check for inconsistencies
    dimensions = [(w, h) for (_, w, h) in results if w is not None]
    if dimensions:
        unique_dims = set(dimensions)
        if len(unique_dims) == 1:
            print(f"✓ All images are consistent: {dimensions[0][0]}×{dimensions[0][1]}px")
        else:
            print("⚠ INCONSISTENT DIMENSIONS FOUND:")
            for name, w, h in results:
                if w is not None:
                    print(f"  - {name}: {w}×{h}px")
            print("\nRECOMMENDATION: Resize all to 3000×3000px for consistency")

    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
