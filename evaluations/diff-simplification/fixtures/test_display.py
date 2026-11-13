"""Public behavior of the synthetic display module."""

import unittest

from display import display_value


class DisplayTests(unittest.TestCase):
    def test_missing_values(self):
        self.assertEqual(display_value(None), "—")
        self.assertEqual(display_value(""), "—")

    def test_present_values(self):
        self.assertEqual(display_value(12), "12")
        self.assertEqual(display_value("ready"), "ready")


if __name__ == "__main__":
    unittest.main()
