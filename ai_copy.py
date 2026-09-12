from __future__ import annotations

import json
import urllib.error
import urllib.request


def _fallback_copy(name: str, discount: int) -> dict[str, str]:
    product = name.strip() or "your product"
    if discount >= 50:
        hook = f"Flat {discount}% OFF on {product}"
        sub = "Limited-time deal — grab it before it’s gone."
    elif discount >= 20:
        hook = f"Special Deal on {product}"
        sub = f"Save {discount}% today. Great value, limited time."
    else:
        hook = f"Special Price: {product}"
        sub = "A great offer for your customers today."
    return {"headline": hook, "subheadline": sub, "cta": "SHOP NOW"}


def generate_copy(name: str, discount: int, use_ollama: bool = True) -> dict[str, str]:
    fallback = _fallback_copy(name, discount)
    if not use_ollama:
        return fallback

    prompt = (
        "Create short sale-poster copy for a local shop. "
        "Return ONLY JSON with headline, subheadline, cta. "
        f"Product: {name}. Discount: {discount}%."
    )
    payload = json.dumps({"model": "qwen2.5:3b", "prompt": prompt, "stream": False}).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            result = json.loads(response.read().decode())
        parsed = json.loads(result.get("response", "{}"))
        if all(isinstance(parsed.get(k), str) and parsed[k].strip() for k in ("headline", "subheadline", "cta")):
            return parsed
    except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass
    return fallback
