from __future__ import annotations

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

POSTER_SIZE = (1080, 1350)


def calculate_discount(mrp: float, sale_price: float) -> int:
    if mrp <= 0 or sale_price < 0 or sale_price > mrp:
        return 0
    return round((mrp - sale_price) / mrp * 100)


def _font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def _fit_product(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = box
    target = (right - left, bottom - top)
    fitted = ImageOps.contain(image.convert("RGB"), target)
    canvas = Image.new("RGB", target, "white")
    x = (target[0] - fitted.width) // 2
    y = (target[1] - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def _center_text(draw, text, y, font, fill, width=1080):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)


def render_poster(product_image: Image.Image, name: str, mrp: float, sale_price: float, template: str) -> Image.Image:
    discount = calculate_discount(mrp, sale_price)
    poster = Image.new("RGB", POSTER_SIZE, "white")
    draw = ImageDraw.Draw(poster)

    if template == "Bold Sale":
        draw.rectangle((0, 0, 1080, 300), fill=(20, 20, 20))
        draw.rectangle((0, 300, 1080, 1350), fill=(255, 245, 230))
        _center_text(draw, "BIG SALE", 55, _font(112, True), "white")
        _center_text(draw, f"SAVE {discount}%", 190, _font(58, True), (255, 205, 60))
        product = _fit_product(product_image, (100, 350, 980, 900))
        poster.paste(product, (100, 350))
        _center_text(draw, name[:32], 930, _font(54, True), (25, 25, 25))
        _center_text(draw, f"₹{sale_price:,.0f}", 1005, _font(100, True), (190, 35, 35))
        _center_text(draw, f"MRP ₹{mrp:,.0f}", 1125, _font(38), (100, 100, 100))

    elif template == "Minimal":
        draw.rectangle((0, 0, 1080, 1350), fill=(248, 248, 248))
        draw.rectangle((55, 55, 1025, 1295), outline=(30, 30, 30), width=4)
        _center_text(draw, name[:30], 95, _font(58, True), (25, 25, 25))
        product = _fit_product(product_image, (130, 220, 950, 830))
        poster.paste(product, (130, 220))
        _center_text(draw, "SPECIAL PRICE", 885, _font(38, True), (80, 80, 80))
        _center_text(draw, f"₹{sale_price:,.0f}", 930, _font(110, True), (20, 20, 20))
        _center_text(draw, f"MRP ₹{mrp:,.0f}  •  {discount}% OFF", 1070, _font(36), (100, 100, 100))
        _center_text(draw, "LIMITED TIME OFFER", 1160, _font(42, True), (190, 35, 35))

    else:  # Shop Offer
        draw.rectangle((0, 0, 1080, 1350), fill=(235, 245, 255))
        draw.rectangle((0, 0, 1080, 250), fill=(35, 90, 170))
        _center_text(draw, "SHOP OFFER", 55, _font(90, True), "white")
        product = _fit_product(product_image, (90, 285, 990, 850))
        poster.paste(product, (90, 285))
        draw.rounded_rectangle((70, 885, 1010, 1230), radius=35, fill="white", outline=(35, 90, 170), width=5)
        draw.text((115, 920), name[:26], font=_font(48, True), fill=(25, 25, 25))
        draw.text((115, 995), f"₹{sale_price:,.0f}", font=_font(105, True), fill=(35, 90, 170))
        draw.text((115, 1120), f"MRP ₹{mrp:,.0f}   |   {discount}% OFF", font=_font(34), fill=(90, 90, 90))

    return poster


def image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()
