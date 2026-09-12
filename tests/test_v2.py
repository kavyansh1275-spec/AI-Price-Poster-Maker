from PIL import Image

from ai_copy import generate_copy
from formats import FORMATS, render_social
from smart_image import smart_product_canvas, trim_background


def test_copy_fallback_is_offline():
    copy = generate_copy("Running Shoes", 30, use_ollama=False)
    assert set(copy) == {"headline", "subheadline", "cta"}
    assert all(copy.values())


def test_formats_render():
    base = Image.new("RGB", (1080, 1350), "white")
    for size in FORMATS.values():
        image = render_social(base, "Sale", "Limited offer", "SHOP NOW", 799, 999, 20, size)
        assert image.size == size
        assert image.mode == "RGB"


def test_plain_background_cleanup_returns_rgba():
    source = Image.new("RGB", (200, 200), "white")
    source.paste((20, 20, 20), (70, 70, 130, 130))
    cleaned = trim_background(source)
    assert cleaned.mode == "RGBA"
    assert cleaned.getbbox() is not None


def test_smart_canvas_size():
    source = Image.new("RGB", (400, 300), "white")
    output = smart_product_canvas(source, (600, 500))
    assert output.size == (600, 500)
    assert output.mode == "RGBA"
