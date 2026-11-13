"""Synthetic rate-limit header module before either contributor's changes."""


def format_rate_limit(remaining, window_seconds=60):
    return f"{int(remaining)};w={window_seconds}"


def parse_forwarded_for(header_value):
    return header_value
