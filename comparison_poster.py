"""Render a clean price-comparison social poster."""

from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from comparison_engine import compare_prices, PriceEntry

SIZE = (1080, 1350)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates += [
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates += [
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def render_comparison_poster(
    product_name: str,
    entries: list[PriceEntry],
    product_image: Image.Image | None = None,
) -> Image.Image:
    """Create a 1080x1350 comparison poster."""
    result = compare_prices(entries)
    image = Image.new("RGB", SIZE, "white")
    draw = ImageDraw.Draw(image)

    title_font = _font(68, True)
    sub_font = _font(34, False)
    price_font = _font(48, True)
    small_font = _font(28, False)

    draw.text((70, 60), "PRICE COMPARISON", font=title_font, fill="black")
    draw.text((70, 145), product_name.strip() or "Product", font=sub_font, fill="#444444")

    if product_image is not None:
        thumb = product_image.convert("RGB").copy()
        thumb.thumbnail((260, 260), Image.Resampling.LANCZOS)
        x = 1080 - thumb.width - 70
        image.paste(thumb, (x, 55))

    y = 260
    row_h = 120
    left = 70
    right = 1010

    for index, entry in enumerate(result["entries"], start=1):
        is_best = entry == result["cheapest"]
        fill = "#eeeeee" if index % 2 == 0 else "#f8f8f8"
        draw.rounded_rectangle((left, y, right, y + row_h - 12), radius=18, fill=fill)
        label = f"{index}. {entry.store}"
        if is_best:
            label += "  • BEST DEAL"
        draw.text((95, y + 25), label, font=sub_font, fill="black")
        price_text = f"₹{entry.price:,.2f}" if entry.price % 1 else f"₹{entry.price:,.0f}"
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        draw.text((right - 30 - (bbox[2] - bbox[0]), y + 20), price_text, font=price_font, fill="black")
        y += row_h

    summary_y = min(y + 30, 1060)
    draw.text((70, summary_y), f"Save up to ₹{result['savings']:,.2f}", font=title_font, fill="black")
    draw.text(
        (70, summary_y + 90),
        f"{result['savings_percent']:.2f}% cheaper than the highest listed price",
        font=sub_font,
        fill="#444444",
    )
    draw.text((70, 1265), "Prices entered by the user • Verify before purchasing", font=small_font, fill="#666666")
    return image


def image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
