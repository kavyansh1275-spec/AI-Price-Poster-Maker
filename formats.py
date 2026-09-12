from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

FORMATS = {
    "Instagram Post (1:1)": (1080, 1080),
    "Instagram Portrait (4:5)": (1080, 1350),
    "Landscape (16:9)": (1280, 720),
}


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


def render_social(poster: Image.Image, headline: str, subheadline: str, cta: str, sale_price: float, mrp: float, discount: int, size: tuple[int, int]) -> Image.Image:
    w, h = size
    canvas = Image.new("RGB", size, (247, 247, 247))
    poster = poster.convert("RGB")
    # Fit the V1 poster into the requested aspect ratio while preserving all content.
    poster.thumbnail((w, int(h * 0.66)))
    x = (w - poster.width) // 2
    y = max(20, int(h * 0.04))
    canvas.paste(poster, (x, y))

    draw = ImageDraw.Draw(canvas)
    scale = w / 1080
    headline_font = _font(max(28, int(54 * scale)), True)
    sub_font = _font(max(18, int(27 * scale)))
    price_font = _font(max(34, int(60 * scale)), True)
    cta_font = _font(max(20, int(30 * scale)), True)

    bottom = min(h - 20, y + poster.height + int(35 * scale))
    draw.text((w // 2, bottom), headline[:42], font=headline_font, fill=(20, 20, 20), anchor="ma")
    draw.text((w // 2, bottom + int(65 * scale)), subheadline[:70], font=sub_font, fill=(80, 80, 80), anchor="ma")
    draw.text((w // 2, bottom + int(115 * scale)), f"₹{sale_price:,.0f}  •  {discount}% OFF", font=price_font, fill=(190, 35, 35), anchor="ma")
    draw.rounded_rectangle((w * 0.35, h - int(75 * scale), w * 0.65, h - int(22 * scale)), radius=int(16 * scale), fill=(25, 25, 25))
    draw.text((w // 2, h - int(48 * scale)), cta[:18], font=cta_font, fill="white", anchor="mm")
    return canvas
