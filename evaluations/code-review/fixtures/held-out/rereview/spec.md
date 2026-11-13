# Outbound webhook delivery contract

`deliver_webhook(payload_bytes, secret_bytes, send_fn, max_attempts)` signs `payload_bytes` with HMAC-SHA256 (`X-Signature` lowercase hex digest) and calls `send_fn(payload_bytes, headers)`, which returns `(status_code, response_headers)`.

- Compute the HMAC digest over the exact `payload_bytes` sent on the wire.
- `2xx` statuses return `("delivered", status_code)` immediately.
- On `429`, if `response_headers` includes an integer `Retry-After` value, return `("rate_limited", int(retry_after))` immediately so the external scheduler re-enqueues after the cooldown instead of retrying in-process.
- Retry `502`, `503`, `504`, or `429` without `Retry-After` up to `max_attempts`, then return `("exhausted", status_code)`.
- Other `4xx` statuses (`400`, `401`, `404`, etc.) return `("permanent_error", status_code)` without retrying.
- `max_attempts` is validated at configuration load to be an integer in `1..5`. Do not edit during review.
