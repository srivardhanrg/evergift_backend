import asyncio
from PIL import Image
from io import BytesIO
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.image_processor import ImageProcessor

async def test_cover():
    print("Testing cover page generation...")
    processor = ImageProcessor()
    
    # Mock download_image
    async def mock_download(url):
        img = Image.new('RGB', (2550, 2550), color='#2D5016')
        out = BytesIO()
        img.save(out, format='PNG')
        return out.getvalue()
        
    processor.storage.download_image = mock_download
    
    # Very long name and title
    title = "The Magnificent Adventures of the Enchanted Forest"
    name = "Christopher Alexander Bartholomew"
    
    try:
        result = await processor.process_cover_page(
            cover_image_url="dummy",
            story_title=title,
            child_name=name
        )
        print(f"Success! Cover image generated. Size: {len(result)} bytes")
        
        # Save locally to check
        with open("test_cover_output.png", "wb") as f:
            f.write(result)
        print("Saved to test_cover_output.png")
    except Exception as e:
        print(f"Error: {e}")

async def test_story():
    print("Testing story page generation...")
    processor = ImageProcessor()
    
    # Mock download_image
    async def mock_download(url):
        img = Image.new('RGB', (2550, 2550), color='#F5F5DC')
        out = BytesIO()
        img.save(out, format='PNG')
        return out.getvalue()
        
    processor.storage.download_image = mock_download
    
    try:
        result = await processor.process_story_text_page(
            background_url="dummy",
            story_text="This is a test story page to ensure the 80px font wraps correctly at 70% width. It should look absolutely stunning with the drop cap and the balanced line height, spanning multiple lines elegantly.",
            theme="storygift_enchanted_forest",
            text_page_number=1
        )
        print(f"Success! Story image generated. Size: {len(result)} bytes")
        
        # Save locally to check
        with open("test_story_output.png", "wb") as f:
            f.write(result)
        print("Saved to test_story_output.png")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cover())
    asyncio.run(test_story())
