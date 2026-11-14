"""Synthetic shared duration facilities with deliberately different contracts."""

import re


class DurationError(ValueError):
    pass


def parse_timeout(raw):
    """Return nonnegative integer milliseconds; do not normalize input text."""
    text = str(raw)
    match = re.fullmatch(r"(0|[1-9][0-9]*)(ms|s)", text)
    if match is None:
        raise DurationError(f"invalid timeout: {text!r}")
    amount, unit = match.groups()
    return int(amount) * (1000 if unit == "s" else 1)


def parse_seconds(raw):
    """Legacy display input: whitespace, fractions and negatives are supported."""
    return round(float(str(raw).strip().removesuffix("s")), 1)
