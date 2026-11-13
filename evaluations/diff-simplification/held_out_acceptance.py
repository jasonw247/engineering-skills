"""Held-out synthetic acceptance checks for quota.py; pass an evaluator's output directory."""

import ast
import importlib.util
from pathlib import Path
import sys
import unittest


FIXTURES = Path(__file__).parent / "fixtures" / "held-out"
candidate = Path(sys.argv[1])
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location("candidate_quota", candidate / "quota.py")
quota = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quota)


def function_source(path, name):
    source = path.read_text()
    node = next(
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )
    return ast.get_source_segment(source, node)


class HeldOutAcceptanceTests(unittest.TestCase):
    def test_supported_values(self):
        cases = [
            ((None,), {}, "unlimited"),
            ((0,), {}, "0;w=60"),
            ((False,), {}, "0;w=60"),
            ((15,), {"window_seconds": 120}, "15;w=120"),
            (("42",), {}, "42;w=60"),
        ]
        for args, kwargs, expected in cases:
            with self.subTest(args=args, kwargs=kwargs):
                self.assertEqual(quota.format_rate_limit(*args, **kwargs), expected)

    def test_negative_quota_raises_exact_contract(self):
        for bad in (-1, "-5"):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, "remaining quota cannot be negative"):
                    quota.format_rate_limit(bad)

    def test_int_conversion_happens_once(self):
        class CountedInt:
            calls = 0

            def __int__(self):
                self.calls += 1
                return 7

        value = CountedInt()
        self.assertEqual(quota.format_rate_limit(value, window_seconds=90), "7;w=90")
        self.assertEqual(value.calls, 1)

    def test_other_contributor_preserved(self):
        self.assertEqual(
            function_source(candidate / "quota.py", "parse_forwarded_for"),
            function_source(FIXTURES / "quota.py", "parse_forwarded_for"),
        )

    def test_protected_inputs_preserved(self):
        for name in ("original.py", "requirements.md", "test_quota.py"):
            with self.subTest(name=name):
                self.assertEqual(
                    (candidate / name).read_bytes(),
                    (FIXTURES / name).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
