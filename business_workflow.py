from dataclasses import dataclass


PACKAGES = {
    "Starter": {"posters": 5, "revisions": 1, "price": 499},
    "Growth": {"posters": 15, "revisions": 2, "price": 999},
    "Pro": {"posters": 30, "revisions": 3, "price": 1999},
}


@dataclass(frozen=True)
class Quote:
    client: str
    business: str
    package: str
    subtotal: float
    discount: float
    total: float
    turnaround: str


def package_quote(package: str, client: str, business: str, discount_percent: float = 0.0, turnaround: str = "48 hours") -> Quote:
    if package not in PACKAGES:
        raise ValueError(f"Unknown package: {package}")
    if not client.strip() or not business.strip():
        raise ValueError("Client and business names are required")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    subtotal = float(PACKAGES[package]["price"])
    discount = round(subtotal * discount_percent / 100, 2)
    return Quote(client.strip(), business.strip(), package, subtotal, discount, round(subtotal - discount, 2), turnaround)


def quote_text(quote: Quote) -> str:
    spec = PACKAGES[quote.package]
    return (f"QUOTE FOR {quote.business.upper()}\n\n"
            f"Client: {quote.client}\n"
            f"Package: {quote.package}\n"
            f"Deliverables: {spec['posters']} posters\n"
            f"Revisions: {spec['revisions']}\n"
            f"Turnaround: {quote.turnaround}\n\n"
            f"Subtotal: ₹{quote.subtotal:,.2f}\n"
            f"Discount: ₹{quote.discount:,.2f}\n"
            f"TOTAL: ₹{quote.total:,.2f}")


def sales_message(quote: Quote) -> str:
    spec = PACKAGES[quote.package]
    return (f"Hi {quote.client}, I can create {spec['posters']} promotional posters for {quote.business} "
            f"with {spec['revisions']} revision{'s' if spec['revisions'] != 1 else ''}. "
            f"The {quote.package} package is ₹{quote.total:,.0f} and delivery is within {quote.turnaround}. "
            "If you'd like to proceed, send your product photos, prices and logo.")


def delivery_checklist() -> list[str]:
    return [
        "Collect product photos",
        "Confirm product names and prices",
        "Confirm logo and brand colors",
        "Generate posters",
        "Review spelling and prices",
        "Send final PNG files",
        "Ask for testimonial/referral",
    ]
