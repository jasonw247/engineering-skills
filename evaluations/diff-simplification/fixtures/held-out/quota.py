"""Synthetic rate-limit module with two contributors' pending changes."""


class _QuotaFormatter:
    def __init__(self, window_seconds):
        self.window_seconds = window_seconds

    def render(self, count):
        return f"{count};w={self.window_seconds}"


def _coerce_non_negative(raw_value):
    numeric = int(raw_value)
    if numeric < 0:
        raise ValueError("remaining quota cannot be negative")
    return numeric


def format_rate_limit(remaining, window_seconds=60):
    if remaining is None:
        header = "unlimited"
    else:
        formatter = _QuotaFormatter(window_seconds)
        checked = _coerce_non_negative(remaining)
        header = formatter.render(checked)
    return header


def parse_forwarded_for(header_value):
    parts = [item.strip() for item in header_value.split(",") if item.strip()]
    if parts:
        return parts[0]
    return "unknown"
