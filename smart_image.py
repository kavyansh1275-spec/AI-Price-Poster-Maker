from __future__ import annotations

from PIL import Image, ImageChops, ImageFilter, ImageOps


def trim_background(image: Image.Image, tolerance: int = 18) -> Image.Image:
    """Remove a near-uniform background using the top-left pixel as the reference.

    This is intentionally lightweight and dependency-free. It works best for product
    photos shot against a plain white/light background; complex backgrounds are kept.
    """
    rgba = image.convert("RGBA")
    bg = Image.new("RGBA", rgba.size, rgba.getpixel((0, 0)))
    diff = ImageChops.difference(rgba, bg).convert("L")
    mask = diff.point(lambda p: 0 if p <= tolerance else 255)
    bbox = mask.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    # Soften the hard edge slightly without destroying the product.
    alpha = cropped.getchannel("A")
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.4))
    cropped.putalpha(alpha)
    return cropped


def smart_product_canvas(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    cleaned = trim_background(image)
    fitted = ImageOps.contain(cleaned, (int(size[0] * 0.82), int(size[1] * 0.72)))
    canvas = Image.new("RGBA", size, (255, 255, 255, 0))
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    return canvas
