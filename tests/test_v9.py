import pytest

from brand_engine import BrandKit, load_brand_kit, make_brand_kit, save_brand_kit


def test_make_brand_kit_normalizes_colors():
    kit = make_brand_kit(" Kav Store ", "#112233", "#ffffff", "#Aa0000", "Best deals")
    assert isinstance(kit, BrandKit)
    assert kit.name == "Kav Store"
    assert kit.primary == "#112233"
    assert kit.secondary == "#FFFFFF"
    assert kit.accent == "#AA0000"
    assert kit.tagline == "Best deals"


def test_brand_kit_round_trip():
    original = make_brand_kit("Demo Shop", "#123456", "#ABCDEF", "#FEDCBA", "Fresh offers")
    restored = load_brand_kit(save_brand_kit(original))
    assert restored == original


@pytest.mark.parametrize("color", ["red", "#123", "123456", "#GGGGGG"])
def test_invalid_color_rejected(color):
    with pytest.raises(ValueError):
        make_brand_kit("Shop", color, "#FFFFFF", "#000000")


def test_empty_brand_name_rejected():
    with pytest.raises(ValueError):
        make_brand_kit("  ", "#000000", "#FFFFFF", "#FF0000")
