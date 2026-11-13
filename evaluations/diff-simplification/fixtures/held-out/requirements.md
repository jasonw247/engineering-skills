# Synthetic completed quota-header change

The completed request updated `format_rate_limit(remaining, window_seconds=60)` in `quota.py`:

- When `remaining` is `None`, return `"unlimited"`.
- Otherwise convert `remaining` via `int(remaining)` once. Raise `ValueError("remaining quota cannot be negative")` when the resulting integer is less than zero; otherwise return `f"{count};w={window_seconds}"` (so `remaining=0` returns `"0;w=60"`).
- Background CLI maintenance jobs call `format_rate_limit` directly without going through the HTTP middleware, so negative-value validation inside `format_rate_limit` remains part of its contract.

Task-owned scope: `format_rate_limit`, `_QuotaFormatter`, and `_coerce_non_negative` in `quota.py`. Another contributor owns the pending `parse_forwarded_for` function in `quota.py`; preserve `parse_forwarded_for` byte-for-byte. `original.py`, `requirements.md`, and `test_quota.py` are read-only.
