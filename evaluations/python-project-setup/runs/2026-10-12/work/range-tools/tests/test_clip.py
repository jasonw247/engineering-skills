import unittest

from range_tools import clip


class ClipTests(unittest.TestCase):
    def test_integer_interval(self):
        for value, expected in [(-9, -2), (-2, -2), (0, 0), (5, 5), (9, 5)]:
            with self.subTest(value=value):
                self.assertEqual(clip(value, -2, 5), expected)

    def test_float_interval(self):
        cases = [
            (-2.5, -1.5),
            (-1.5, -1.5),
            (0.25, 0.25),
            (1.5, 1.5),
            (2.5, 1.5),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(clip(value, -1.5, 1.5), expected)

    def test_mixed_integer_and_float_inputs(self):
        self.assertEqual(clip(1.25, 0, 2), 1.25)
        self.assertEqual(clip(3, 0.5, 2.5), 2.5)

    def test_single_point_interval(self):
        for value in [-5, 2, 9]:
            with self.subTest(value=value):
                self.assertEqual(clip(value, 2, 2), 2)

    def test_inverted_interval_always_raises(self):
        for value in [-10, 0, 10]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    clip(value, 2, -2)


if __name__ == "__main__":
    unittest.main()
