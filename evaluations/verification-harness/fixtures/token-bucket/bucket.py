"""Synthetic fixture: a token-bucket rate limiter."""

import time


class TokenBucket:
    def __init__(self, capacity, refill_per_second):
        if capacity <= 0 or refill_per_second <= 0:
            raise ValueError("capacity and refill rate must be positive")
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self.tokens = float(capacity)
        self.updated = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.updated
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_second)
        self.updated = now

    def take(self, count=1):
        """Consume `count` tokens if available and report whether it succeeded."""
        if count <= 0:
            raise ValueError("count must be positive")
        self._refill()
        if self.tokens >= count:
            self.tokens -= count
            return True
        return False
