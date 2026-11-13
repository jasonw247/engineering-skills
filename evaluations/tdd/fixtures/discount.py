"""Synthetic fixture for tdd evaluation."""


def subtotal_cents(items: list[dict]) -> int:
    """Return subtotal in integer cents for [{'price_cents': int, 'qty': int}]."""
    return sum(item["price_cents"] * item["qty"] for item in items)
