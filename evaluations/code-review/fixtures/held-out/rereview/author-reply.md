# Author reply

RV-1 fixed: `webhook_v2.py` now computes the HMAC digest directly over `payload_bytes`.

RV-2 rejected: in `webhook_v1.py`, `if 400 <= status < 500:` returned early before the loop continued, so `429` never retried in-process.

RV-3 rejected: `spec.md` guarantees `max_attempts` is validated at configuration load to `1..5`, so `<= 0` is outside the function contract.
