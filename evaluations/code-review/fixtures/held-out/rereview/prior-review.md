# Initial review of webhook_v1.py

RV-1 (high, correctness) - webhook_v1.py:7. HMAC was computed over re-serialized JSON rather than `payload_bytes`, invalidating signatures whenever key spacing or ordering differs. Correction: compute HMAC directly over `payload_bytes`.

RV-2 (medium, correctness) - webhook_v1.py:14-18. `429` responses carrying a `Retry-After` header are retried immediately inside the loop instead of returning `("rate_limited", seconds)` to the scheduler. Correction: check `Retry-After` on `429` and return `("rate_limited", int(retry_after))`.

RV-3 (low, correctness) - webhook_v1.py:5. Passing `max_attempts <= 0` returns `("exhausted", None)` instead of raising `ValueError`. Correction: reject non-positive `max_attempts`.
