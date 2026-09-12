from io import BytesIO

import pytest
from PIL import Image

from comparison_engine import PriceEntry, compare_prices, parse_csv_text
from comparison_poster import image_to_png_bytes, render_comparison_poster


def test_compare_prices_finds_best_deal_and_savings():
    result = compare_prices([
        PriceEntry("Store B", 899),
        PriceEntry("Store A", 799),
        PriceEntry("Store C", 999),
    ])
    assert result["cheapest"] == PriceEntry("Store A", 799)
    assert result["highest"] == PriceEntry("Store C", 999)
    assert result["savings"] == 200
    assert result["savings_percent"] == pytest.approx(20.02)


def test_compare_prices_rejects_empty_input():
    with pytest.raises(ValueError):
        compare_prices([])


def test_invalid_rows_are_ignored():
    result = compare_prices([
        PriceEntry("Valid", 500),
        PriceEntry("", 300),
        PriceEntry("Bad", "not-a-price"),
        PriceEntry("Negative", -10),
    ])
    assert result["entries"] == [PriceEntry("Valid", 500)]


def test_csv_parser_accepts_store_and_price_columns():
    entries = parse_csv_text("store,price\nShop A,1200\nShop B,999\n")
    assert entries == [PriceEntry("Shop A", 1200.0), PriceEntry("Shop B", 999.0)]


def test_csv_parser_accepts_vendor_alias():
    entries = parse_csv_text("vendor,price\nAmazon,799\n")
    assert entries == [PriceEntry("Amazon", 799.0)]


def test_comparison_poster_renders_correctly():
    product = Image.new("RGB", (500, 500), "white")
    poster = render_comparison_poster(
        "Test Headphones",
        [PriceEntry("Shop A", 1499), PriceEntry("Shop B", 1199)],
        product,
    )
    assert poster.size == (1080, 1350)
    assert poster.mode == "RGB"
    data = image_to_png_bytes(poster)
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert Image.open(BytesIO(data)).size == (1080, 1350)
