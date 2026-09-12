from PIL import Image

from creative_engine import VARIATIONS, generate_variations


def test_all_variations_render():
    source = Image.new("RGB", (400, 400), "white")
    result = generate_variations(source, "Test Product", 1000, 800, 20, "Great Deal", "Shop Now")
    assert set(result) == set(VARIATIONS)
    for poster in result.values():
        assert poster.size == (1080, 1350)
        assert poster.mode == "RGB"


def test_unknown_variation_rejected():
    from creative_engine import render_variation
    source = Image.new("RGB", (100, 100), "white")
    try:
        render_variation(source, "Test", 100, 80, 20, "Unknown", "Deal", "Buy")
    except ValueError:
        return
    raise AssertionError("Unknown variation should raise ValueError")
