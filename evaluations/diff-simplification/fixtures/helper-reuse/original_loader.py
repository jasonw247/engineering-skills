"""Synthetic loader before the task-owned timeout batch addition."""


def describe_metadata(metadata):
    # Another contributor owns this function, including its insertion order.
    return ", ".join(f"{key}={value}" for key, value in metadata.items())
