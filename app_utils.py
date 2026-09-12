import re


def safe_filename(name: str, default: str = "poster") -> str:
    """Return a filesystem-safe filename stem for downloads."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", str(name).strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip(".-_")
    return cleaned[:80] or default
