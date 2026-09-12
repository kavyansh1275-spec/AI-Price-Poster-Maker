"""Price comparison logic for V3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PriceEntry:
    store: str
    price: float


def clean_entries(entries: Iterable[PriceEntry]) -> list[PriceEntry]:
    """Normalize entries and discard blank/invalid rows."""
    cleaned: list[PriceEntry] = []
    for entry in entries:
        store = str(entry.store).strip()
        try:
            price = float(entry.price)
        except (TypeError, ValueError):
            continue
        if store and price >= 0:
            cleaned.append(PriceEntry(store, price))
    return cleaned


def compare_prices(entries: Iterable[PriceEntry]) -> dict:
    """Return cheapest, highest, savings and sorted entries."""
    cleaned = clean_entries(entries)
    if not cleaned:
        raise ValueError("At least one valid store and price is required.")

    ordered = sorted(cleaned, key=lambda item: (item.price, item.store.lower()))
    cheapest = ordered[0]
    highest = max(cleaned, key=lambda item: item.price)
    savings = round(highest.price - cheapest.price, 2)
    savings_percent = round((savings / highest.price) * 100, 2) if highest.price else 0.0

    return {
        "entries": ordered,
        "cheapest": cheapest,
        "highest": highest,
        "savings": savings,
        "savings_percent": savings_percent,
    }


def parse_csv_text(text: str) -> list[PriceEntry]:
    """Parse a simple CSV with store and price columns."""
    import csv
    import io

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV must contain a header row.")

    fields = {field.strip().lower(): field for field in reader.fieldnames if field}
    store_key = fields.get("store") or fields.get("vendor") or fields.get("shop")
    price_key = fields.get("price")
    if not store_key or not price_key:
        raise ValueError("CSV needs store/vendor/shop and price columns.")

    return clean_entries(
        PriceEntry(row.get(store_key, ""), row.get(price_key, ""))
        for row in reader
    )
