from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageOps


VARIATIONS = {
    "Flash Sale": {"accent": (235, 55, 65), "label": "FLASH SALE"},
    "Weekend Deal": {"accent": (35, 115, 220), "label": "WEEKEND DEAL"},
    "Premium Offer": {"accent": (190, 150, 55), "label": "PREMIUM OFFER"},
}


def _font(size: int, bold: bool = False):
    candidates = [
        r"C:\\Windows\\Fonts\\arialbd.ttf" if bold else r"C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def _fit(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    x1, y1, x2, y2 = box
    return ImageOps.contain(image.convert("RGB"), (x2 - x1, y2 - y1), method=Image.Resampling.LANCZOS)


def render_variation(
    product_image: Image.Image,
    product_name: str,
    mrp: float,
    sale_price: float,
    discount: int,
    variation: str,
    headline: str,
    cta: str,
    size: tuple[int, int] = (1080, 1350),
) -> Image.Image:
    if variation not in VARIATIONS:
        raise ValueError(f"Unknown variation: {variation}")
    if mrp <= 0 or sale_price < 0 or sale_price > mrp:
        raise ValueError("Invalid price values")

    width, height = size
    spec = VARIATIONS[variation]
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)

    accent = spec["accent"]
    draw.rectangle((0, 0, width, int(height * 0.14)), fill=accent)
    draw.text((55, 35), spec["label"], font=_font(58, True), fill="white")

    title_font = _font(68, True)
    title = headline[:32]
    draw.text((55, int(height * 0.17)), title, font=title_font, fill="black")

    fitted = _fit(product_image, (70, int(height * 0.29), width - 70, int(height * 0.67)))
    x = (width - fitted.width) // 2
    y = int(height * 0.31) + (int(height * 0.35) - fitted.height) // 2
    image.paste(fitted, (x, y))

    draw.rounded_rectangle((55, int(height * 0.70), width - 55, int(height * 0.91)), radius=28, fill=(245, 245, 245), outline=accent, width=5)
    draw.text((85, int(height * 0.735)), product_name[:28], font=_font(40, True), fill="black")
    draw.text((85, int(height * 0.795)), f"₹{sale_price:,.0f}", font=_font(72, True), fill=accent)
    draw.text((width - 300, int(height * 0.81)), f"{discount}% OFF", font=_font(42, True), fill=accent)

    draw.text((55, int(height * 0.925)), cta[:40], font=_font(38, True), fill="black")
    draw.text((width - 300, int(height * 0.925)), f"MRP ₹{mrp:,.0f}", font=_font(28), fill=(90, 90, 90))
    return image


def generate_variations(product_image, product_name, mrp, sale_price, discount, headline, cta):
    return {
        name: render_variation(product_image, product_name, mrp, sale_price, discount, name, headline, cta)
        for name in VARIATIONS
    }
