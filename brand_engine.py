from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import re
from typing import Any


@dataclass(frozen=True)
class BrandKit:
    name: str = "Your Store"
    primary: str = "#111111"
    secondary: str = "#FFFFFF"
    accent: str = "#E53935"
    tagline: str = ""
    font: str = "Arial"


def _hex(value: str) -> str:
    value = value.strip().upper()
    if not re.fullmatch(r"#[0-9A-F]{6}", value):
        raise ValueError(f"Invalid color: {value}")
    return value


def make_brand_kit(name: str, primary: str, secondary: str, accent: str, tagline: str = "", font: str = "Arial") -> BrandKit:
    name = name.strip()
    if not name:
        raise ValueError("Brand name is required")
    return BrandKit(name, _hex(primary), _hex(secondary), _hex(accent), tagline.strip(), font.strip() or "Arial")


def brand_dict(kit: BrandKit) -> dict[str, Any]:
    return asdict(kit)


def save_brand_kit(kit: BrandKit) -> str:
    return json.dumps(brand_dict(kit), ensure_ascii=False, indent=2)


def load_brand_kit(text: str) -> BrandKit:
    data = json.loads(text)
    return make_brand_kit(
        data.get("name", "Your Store"),
        data.get("primary", "#111111"),
        data.get("secondary", "#FFFFFF"),
        data.get("accent", "#E53935"),
        data.get("tagline", ""),
        data.get("font", "Arial"),
    )
