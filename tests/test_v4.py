import io
import zipfile

from PIL import Image

from batch_engine import ProductRow, apply_branding, build_batch_posters, parse_product_csv, posters_to_zip


def test_parse_product_csv():
    text = "name,mrp,sale_price,image_name\nShoes,2000,1499,shoes.jpg\nBag,1500,999,bag.png\n"
    rows = parse_product_csv(text)
    assert rows == [
        ProductRow("Shoes", 2000.0, 1499.0, "shoes.jpg"),
        ProductRow("Bag", 1500.0, 999.0, "bag.png"),
    ]


def test_parse_product_csv_rejects_bad_prices():
    text = "name,mrp,sale_price,image_name\nBad,100,120,bad.jpg\n"
    try:
        parse_product_csv(text)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Invalid prices" in str(exc)


def test_branding_preserves_dimensions():
    image = Image.new("RGB", (1080, 1350), "white")
    branded = apply_branding(image, "Kav Store", "#123456")
    assert branded.size == image.size
    assert branded.mode == "RGB"


def test_batch_and_zip():
    product = ProductRow("Test Product", 1000, 799, "test.png")
    image = Image.new("RGB", (400, 400), "white")
    posters = build_batch_posters([(product, image)], "Minimal", "Kav Store", "#123456")
    assert len(posters) == 1
    assert posters[0][0] == "Test_Product.png"
    assert posters[0][1].size == (1080, 1350)

    archive = posters_to_zip(posters)
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        assert zf.namelist() == ["Test_Product.png"]
        assert zf.read("Test_Product.png").startswith(b"\x89PNG")
