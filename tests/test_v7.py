import pytest

from business_workflow import PACKAGES, delivery_checklist, package_quote, quote_text, sales_message


def test_all_packages_have_valid_pricing():
    assert set(PACKAGES) == {"Starter", "Growth", "Pro"}
    assert all(item["price"] > 0 and item["posters"] > 0 for item in PACKAGES.values())


def test_quote_discount():
    quote = package_quote("Growth", "Asha", "Asha Boutique", 10)
    assert quote.subtotal == 999
    assert quote.discount == 99.9
    assert quote.total == 899.1


def test_quote_rejects_bad_input():
    with pytest.raises(ValueError):
        package_quote("Unknown", "A", "B")
    with pytest.raises(ValueError):
        package_quote("Starter", "", "B")
    with pytest.raises(ValueError):
        package_quote("Starter", "A", "B", 101)


def test_generated_sales_assets():
    quote = package_quote("Starter", "Client", "Local Shop")
    assert "LOCAL SHOP" in quote_text(quote)
    assert "Client" in sales_message(quote)
    assert len(delivery_checklist()) >= 5
