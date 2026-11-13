"""Small tools for numeric intervals."""

from typing import Union

__all__ = ["clip"]

Number = Union[int, float]


def clip(value: Number, lower: Number, upper: Number) -> Number:
    """Return value constrained to [lower, upper].

    Inputs are ordinary integers or finite floats. An inverted interval raises
    ValueError, including when value would otherwise fall outside that interval.
    """
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value
