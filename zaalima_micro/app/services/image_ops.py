from PIL import Image
from app.core.config import settings

def compress_and_resize_image(input_path: str, output_path: str) -> bool:
    """Resizes and compresses an image, converting it to JPEG."""
    try:
        with Image.open(input_path) as img:
            # Maintain aspect ratio while resizing to max bounds
            img.thumbnail(settings.IMAGE_MAX_RESOLUTION)
            # Ensure compatibility (strip alpha channels for JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(output_path, "JPEG", optimize=True, quality=settings.IMAGE_QUALITY_PERCENT)
        return True
    except Exception as e:
        print(f"Image Processing Error: {e}")
        return False
