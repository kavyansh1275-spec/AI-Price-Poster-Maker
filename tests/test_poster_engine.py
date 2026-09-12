from io import BytesIO

from PIL import Image

from poster_engine import calculate_discount, image_to_png_bytes, render_poster


def test_discount():
    assert calculate_discount(1000, 800) == 20
    assert calculate_discount(500, 500) == 0
    assert calculate_discount(100, 75) == 25


def test_invalid_discount_inputs():
    assert calculate_discount(0, 0) == 0
    assert calculate_discount(100, 120) == 0


def test_render_all_templates():
    source = Image.new("RGB", (400, 400), "white")
    for template in ("Bold Sale", "Minimal", "Shop Offer"):
        poster = render_poster(source, "Test Product", 1000, 800, template)
        assert poster.size == (1080, 1350)
        assert poster.mode == "RGB"


def test_png_export():
    source = Image.new("RGB", (100, 100), "white")
    poster = render_poster(source, "Test", 100, 80, "Minimal")
    data = image_to_png_bytes(poster)
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    Image.open(BytesIO(data)).verify()
