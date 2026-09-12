from io import BytesIO
from PIL import Image

from image_ai import image_to_bytes, prepare_product_image


def test_prepare_product_image_keeps_dimensions():
    image = Image.new("RGB", (120, 80), "white")
    result = prepare_product_image(image)
    assert result.size == (120, 80)
    assert result.mode == "RGBA"


def test_prepare_product_image_upscale():
    image = Image.new("RGB", (20, 10), "white")
    result = prepare_product_image(image, upscale=2)
    assert result.size == (40, 20)


def test_image_to_bytes_is_valid_png():
    image = Image.new("RGBA", (16, 16), "white")
    data = image_to_bytes(image)
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    Image.open(BytesIO(data)).verify()
