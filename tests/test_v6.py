from app_utils import safe_filename


def test_safe_filename_removes_unsafe_characters():
    assert safe_filename("Men's Shirt / 50% OFF!") == "Men-s-Shirt-50-OFF"


def test_safe_filename_limits_length():
    assert len(safe_filename("x" * 200)) <= 80


def test_safe_filename_has_default_for_empty_input():
    assert safe_filename("...___") == "poster"
