"""Synthetic completed timeout batch addition."""

from durations import parse_timeout


def build_timeouts(entries, audit):
    output = []
    for name, raw in entries:
        milliseconds = parse_timeout(raw)
        audit.append((name, milliseconds))
        output.append((name, milliseconds))
    return output


def describe_metadata(metadata):
    # Another contributor owns this function, including its insertion order.
    return ", ".join(f"{key}={value}" for key, value in metadata.items())
