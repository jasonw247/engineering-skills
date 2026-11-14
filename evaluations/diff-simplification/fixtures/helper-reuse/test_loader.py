"""Supplied smoke tests for a synthetic completed change."""

import unittest

from durations import DurationError, parse_seconds, parse_timeout
from loader import build_timeouts


class LoaderTests(unittest.TestCase):
    def test_order_and_duplicates(self):
        audit = []
        expected = [("api", 2000), ("db", 0), ("api", 15)]
        self.assertEqual(build_timeouts([("api", "2s"), ("db", "0ms"), ("api", "15ms")], audit), expected)
        self.assertEqual(audit, expected)

    def test_direct_timeout_caller(self):
        with self.assertRaises(DurationError):
            parse_timeout(" 1s")

    def test_legacy_display_caller(self):
        self.assertEqual(parse_seconds(" -1.25s "), -1.2)


if __name__ == "__main__":
    unittest.main()
