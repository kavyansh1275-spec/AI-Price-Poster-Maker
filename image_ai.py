from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter


def prepare_product_image(image: Image.Image, *, enhance: bool = True, upscale: int = 1) -> Image.Image:
    """Prepare a product image for creative layouts using lightweight local processing.

    This intentionally does not claim to be generative AI or perfect background removal.
    """
    image = image.convert("RGBA")
    if upscale > 1:
        image = image.resize((image.width * upscale, image.height * upscale), Image.Resampling.LANCZOS)
    if enhance:
        rgb = image.convert("RGB")
        rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
        rgb = ImageEnhance.Color(rgb).enhance(1.04)
        rgb = rgb.filter(ImageFilter.SHARPEN)
        image = rgb.convert("RGBA")
    return image


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=fmt)
    return buffer.getvalue()
