import hashlib
import hmac


def deliver_webhook(payload_bytes, secret_bytes, send_fn, max_attempts):
    digest = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
    headers = {"X-Signature": digest}
    last_status = None
    for _ in range(max_attempts):
        status, resp_headers = send_fn(payload_bytes, headers)
        if 200 <= status < 300:
            return ("delivered", status)
        if 400 <= status < 500 and status != 429:
            return ("permanent_error", status)
        last_status = status
    return ("exhausted", last_status)
