"""V4 batch/business poster generation utilities."""

from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from typing import Iterable

from PIL import Image, ImageDraw

from poster_engine import image_to_png_bytes, render_poster


@dataclass(frozen=True)
class ProductRow:
    name: str
    mrp: float
    sale_price: float
    image_name: str


def parse_product_csv(text: str) -> list[ProductRow]:
    """Parse CSV with columns: name,mrp,sale_price,image_name."""
    import csv
    import io as _io

    rows = list(csv.DictReader(_io.StringIO(text)))
    if not rows:
        raise ValueError("CSV is empty or missing a header row.")

    required = {"name", "mrp", "sale_price", "image_name"}
    fields = set(rows[0].keys())
    missing = required - fields
    if missing:
        raise ValueError("CSV is missing columns: " + ", ".join(sorted(missing)))

    products: list[ProductRow] = []
    for number, row in enumerate(rows, start=2):
        try:
            name = (row.get("name") or "").strip()
            image_name = (row.get("image_name") or "").strip()
            mrp = float(row.get("mrp") or 0)
            sale_price = float(row.get("sale_price") or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid numeric value on CSV row {number}.") from exc
        if not name or not image_name:
            raise ValueError(f"Missing name or image_name on CSV row {number}.")
        if mrp <= 0 or sale_price < 0 or sale_price > mrp:
            raise ValueError(f"Invalid prices on CSV row {number}.")
        products.append(ProductRow(name, mrp, sale_price, image_name))
    return products


def apply_branding(image: Image.Image, brand_name: str, brand_color: str, logo: Image.Image | None = None) -> Image.Image:
    """Add a small branded header without changing the poster's dimensions."""
    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    bar_height = max(64, height // 16)
    try:
        color = brand_color.strip() or "#111111"
        if not color.startswith("#") or len(color) not in (4, 7):
            raise ValueError
    except ValueError:
        color = "#111111"

    draw.rectangle((0, 0, width, bar_height), fill=color)
    text = (brand_name or "Your Store").strip()[:40]
    draw.text((24, max(10, bar_height // 2 - 12)), text, fill="white")

    if logo is not None:
        mark = logo.convert("RGBA").copy()
        mark.thumbnail((bar_height - 16, bar_height - 16), Image.Resampling.LANCZOS)
        x = width - mark.width - 16
        y = (bar_height - mark.height) // 2
        canvas.paste(mark, (x, y), mark)

    return canvas


def build_batch_posters(
    products: Iterable[tuple[ProductRow, Image.Image]],
    template: str,
    brand_name: str,
    brand_color: str,
    logo: Image.Image | None = None,
) -> list[tuple[str, Image.Image]]:
    """Render and brand a batch of product posters."""
    results: list[tuple[str, Image.Image]] = []
    for product, product_image in products:
        poster = render_poster(product_image, product.name, product.mrp, product.sale_price, template)
        poster = apply_branding(poster, brand_name, brand_color, logo)
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in product.name).strip("_") or "product"
        results.append((f"{safe_name}.png", poster))
    return results


def posters_to_zip(posters: Iterable[tuple[str, Image.Image]]) -> bytes:
    """Package poster PNGs into a downloadable ZIP."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for filename, image in posters:
            archive.writestr(filename, image_to_png_bytes(image))
    return buffer.getvalue()
