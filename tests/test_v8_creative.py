from PIL import Image

from v8_creative import generate_enhanced_variations


def test_generate_enhanced_variations():
    image = Image.new("RGB", (320, 240), "white")
    result = generate_enhanced_variations(image, "Shoes", 2000, 1500, 25, "Big Deal", "Shop Now")
    assert set(result) == {"Flash Sale", "Weekend Deal", "Premium Offer"}
    for poster in result.values():
        assert poster.size == (1080, 1350)
