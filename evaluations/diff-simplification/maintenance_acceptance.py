"""Independent checks for synthetic maintenance fixtures, outside the actor copy.

Usage: python3 -B maintenance_acceptance.py {helper-reuse,test-setup} CANDIDATE
Behavior checks intentionally accept the original completed candidate too. Review
maintenance removal separately; no textual solution or deletion count is required.
Only copy fixtures and the skill to an evaluator, never this file or cases.json.
"""

import argparse
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


FIXTURES = Path(__file__).parent / "fixtures"


def protected(candidate, family, names):
    for name in names:
        if (candidate / name).read_bytes() != (FIXTURES / family / name).read_bytes():
            raise AssertionError(f"protected input changed: {name}")


def run_python(candidate, program):
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", program, str(candidate.resolve())],
        capture_output=True, text=True, timeout=20,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout


def check_helper(candidate):
    protected(candidate, "helper-reuse", [
        "durations.py", "original_loader.py", "requirements.md", "test_loader.py",
    ])
    def coowned(path):
        source = path.read_text()
        node = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.FunctionDef) and n.name == "describe_metadata")
        return ast.get_source_segment(source, node)
    assert coowned(candidate / "loader.py") == coowned(FIXTURES / "helper-reuse/loader.py"), "co-owned function changed"
    run_python(candidate, r'''
import sys
sys.path.insert(0, sys.argv[1])
from loader import build_timeouts
from durations import DurationError, parse_seconds, parse_timeout

for raw, expected in [("0s", 0), ("0ms", 0), ("17ms", 17), ("123s", 123000)]:
    audit = []
    assert build_timeouts([("x", raw), ("x", raw)], audit) == [("x", expected)] * 2
    assert audit == [("x", expected)] * 2
    assert parse_timeout(raw) == expected
for raw in ["", " 1s", "1s ", "01s", "-1s", "1.5s", "1S", "1", None, False]:
    audit = []
    try:
        build_timeouts([("good", "2ms"), ("bad", raw)], audit)
    except DurationError as error:
        assert str(error) == f"invalid timeout: {str(raw)!r}"
    else:
        raise AssertionError(f"accepted invalid value: {raw!r}")
    assert audit == [("good", 2)]
assert parse_seconds(" -1.25s ") == -1.2
assert build_timeouts([], []) == []

events = []
class Counted:
    def __str__(self):
        events.append("convert")
        return "2s"
class Audit(list):
    def append(self, item):
        events.append("audit")
        super().append(item)
def entries():
    yield ("x", Counted())
    assert events == ["convert", "audit"]
    yield ("bad", "bad")
    raise AssertionError("consumed past first invalid entry")
audit = Audit()
try:
    build_timeouts(entries(), audit)
except DurationError:
    pass
else:
    raise AssertionError("missing invalid-entry error")
assert events == ["convert", "audit"]
assert audit == [("x", 2000)]

sentinel = RuntimeError("caller failure")
class BrokenValue:
    def __str__(self):
        raise sentinel
class BrokenAudit:
    def append(self, item):
        raise sentinel
def broken_entries():
    yield ("x", "1s")
    raise sentinel
for entries, audit in [([("x", BrokenValue())], []),
                       ([("x", "1s")], BrokenAudit()), (broken_entries(), [])]:
    try:
        build_timeouts(entries, audit)
    except RuntimeError as error:
        assert error is sentinel
    else:
        raise AssertionError("caller error swallowed")
''')
    return {"behavior": "passed", "ownership": "passed", "maintenance_review": "required"}


TEST_RUNNER = r'''
import io, json, sys, unittest
sys.path.insert(0, sys.argv[1])
import test_retry
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
    unittest.defaultTestLoader.loadTestsFromModule(test_retry))
print(json.dumps({"tests": result.testsRun,
                  "failures": [str(test) for test, _ in result.failures],
                  "errors": [str(test) for test, _ in result.errors],
                  "skipped": len(result.skipped),
                  "expected_failures": len(result.expectedFailures),
                  "unexpected_successes": len(result.unexpectedSuccesses),
                  "diagnostics": stream.getvalue()}))
'''

MUTATIONS = {
    "empty_payload": ('return payload', 'return payload or "fallback"'),
    "missing_429": ('(429, 503)', '(503,)'),
    "missing_503": ('(429, 503)', '(429,)'),
    "delay_off_by_one": ('clock.sleep(attempt + 1)', 'clock.sleep(attempt + 2)'),
    "early_exhaustion": ('attempt + 1 == attempts', 'attempt + 2 == attempts'),
    "retry_on_400": ('(429, 503)', '(429, 503, 400)'),
    "cancel_leaks_transport": ('transport.close()', 'if not clock.cancel:\n            transport.close()'),
    "invalid_attempts_touch_transport": ('raise ValueError("attempts must be positive")',
        'transport.close()\n        raise ValueError("attempts must be positive")'),
}


def check_tests(candidate):
    protected(candidate, "test-setup", [
        "retry.py", "support.py", "original_test_retry.py", "requirements.md",
    ])
    results = {}
    # Mutate disposable copies only, never the evaluator's checkout.
    with tempfile.TemporaryDirectory(prefix="simplification-acceptance-") as temp:
        root = Path(temp) / "case"
        shutil.copytree(candidate, root)
        source = (root / "retry.py").read_text()
        for name, mutation in [("correct", None), *MUTATIONS.items()]:
            if mutation:
                old, new = mutation
                assert source.count(old) == 1, f"stale mutant: {name}"
                (root / "retry.py").write_text(source.replace(old, new))
            else:
                (root / "retry.py").write_text(source)
            result = json.loads(run_python(root, TEST_RUNNER))
            assert result["tests"] > 0, "no tests executed"
            assert not any(result[key] for key in (
                "skipped", "expected_failures", "unexpected_successes",
            )), f"{name}: invalid test execution: {result['diagnostics']}"
            assert bool(result["failures"] or result["errors"]) == bool(mutation), f"{name}: {result['diagnostics']}"
            results[name] = result
    return {"behavior": "passed", "ownership": "passed", "mutants": results,
            "maintenance_and_diagnostics_review": "required"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=["helper-reuse", "test-setup"])
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    check = check_helper if args.family == "helper-reuse" else check_tests
    print(json.dumps(check(args.candidate), indent=2))


if __name__ == "__main__":
    main()
