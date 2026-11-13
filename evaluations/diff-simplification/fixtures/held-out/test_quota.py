"""Unit tests shipped with the synthetic quota task."""

import unittest

from quota import format_rate_limit


class QuotaTests(unittest.TestCase):
    def test_unlimited_and_positive(self):
        self.assertEqual(format_rate_limit(None), "unlimited")
        self.assertEqual(format_rate_limit(25, window_seconds=30), "25;w=30")

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            format_rate_limit(-1)


if __name__ == "__main__":
    unittest.main()
