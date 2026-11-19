import time
import unittest

from bucket import TokenBucket


class TokenBucketTests(unittest.TestCase):
    def test_refill_after_wait(self):
        bucket = TokenBucket(capacity=2, refill_per_second=10)
        self.assertTrue(bucket.take(2))
        time.sleep(0.1)
        self.assertTrue(bucket.take(1))

    def test_tokens_after_take(self):
        bucket = TokenBucket(capacity=5, refill_per_second=1)
        bucket.take(3)
        expected = min(bucket.capacity, 5 - 3)
        self.assertAlmostEqual(bucket.tokens, expected, places=2)

    def test_rejects_when_empty(self):
        bucket = TokenBucket(capacity=1, refill_per_second=0.001)
        self.assertTrue(bucket.take())
        self.assertFalse(bucket.take())


if __name__ == "__main__":
    unittest.main()
