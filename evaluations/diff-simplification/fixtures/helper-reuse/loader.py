"""Synthetic completed timeout batch addition."""

import re

from durations import DurationError


def build_timeouts(entries, audit):
    output = []
    for name, raw in entries:
        text = str(raw)
        parsed = False
        match = re.fullmatch(r"(0|[1-9][0-9]*)(ms|s)", text)
        if match is None:
            raise DurationError(f"invalid timeout: {text!r}")
        amount, unit = match.groups()
        milliseconds = int(amount) * (1000 if unit == "s" else 1)
        parsed = True
        if parsed:
            audit.append((name, milliseconds))
            output.append((name, milliseconds))
    return output


def describe_metadata(metadata):
    # Another contributor owns this function, including its insertion order.
    return ", ".join(f"{key}={value}" for key, value in metadata.items())
