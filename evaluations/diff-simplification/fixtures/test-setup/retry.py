"""Synthetic synchronous retry API; no network or real clock."""


class FetchError(Exception):
    pass


class Cancelled(Exception):
    pass


def fetch(transport, clock, attempts=3):
    if attempts < 1:
        raise ValueError("attempts must be positive")
    try:
        for attempt in range(attempts):
            status, payload = transport.receive()
            if status == 200:
                return payload
            if status not in (429, 503):
                raise FetchError(f"status {status}")
            if attempt + 1 == attempts:
                raise FetchError("retry exhausted")
            clock.sleep(attempt + 1)
    finally:
        transport.close()
