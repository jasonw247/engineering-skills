"""Self-check the independent synthetic acceptance checks, without model calls."""

from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import unittest

from maintenance_acceptance import FIXTURES, check_helper, check_tests


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def copy(self, family):
        target = self.root / family
        shutil.copytree(FIXTURES / family, target)
        return target

    def test_completed_candidates_are_behaviorally_valid(self):
        check_helper(self.copy("helper-reuse"))
        report = check_tests(self.copy("test-setup"))
        self.assertEqual(len(report["mutants"]), 9)

    def test_equivalent_reuse_and_local_test_helper_are_accepted(self):
        root = self.copy("helper-reuse")
        path = root / "loader.py"
        source = path.read_text()
        end = source.index("def describe_metadata")
        path.write_text('from durations import parse_timeout\n\n\n' + '''def build_timeouts(entries, audit):
    output = []
    for name, raw in entries:
        item = (name, parse_timeout(raw))
        audit.append(item)
        output.append(item)
    return output


''' + source[end:])
        check_helper(root)
        root = self.copy("test-setup")
        path = root / "test_retry.py"
        source = path.read_text()
        setup = '''        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])'''
        source = source.replace(setup, '        transport, clock = self.make_pair(responses, events)')
        source = source.replace('class RetryTests(unittest.TestCase):', '''class RetryTests(unittest.TestCase):
    def make_pair(self, responses, events):
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        return transport, clock
''')
        path.write_text(source)
        check_tests(root)

    def test_retained_trial_snapshots_match_their_evidence(self):
        run = Path(__file__).parent / "runs/2026-11-14-maintenance"
        record = json.loads((run / "results.json").read_text())
        repository = Path(__file__).resolve().parents[2]
        # Historical skill/checker hashes are evidence, not locks preventing
        # future guidance updates. Raw replay fixtures must still match.
        for name, expected in record["input_sha256"].items():
            if name.startswith("evaluations/"):
                self.assertEqual(hashlib.sha256((repository / name).read_bytes()).hexdigest(), expected, name)
        for case in record["cases"]:
            output = run / case["output"]
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), case["output_sha256"])
            family = output.parent.name
            candidate = self.copy(family)
            shutil.copy2(output, candidate / output.name)
            (check_helper if family == "helper-reuse" else check_tests)(candidate)

    def test_contract_drift_is_rejected(self):
        root = self.copy("helper-reuse")
        path = root / "loader.py"
        path.write_text(path.read_text().replace('text = str(raw)', 'text = str(raw).strip()'))
        with self.assertRaises(AssertionError):
            check_helper(root)

    def test_ownership_violation_is_rejected(self):
        root = self.copy("helper-reuse")
        path = root / "durations.py"
        path.write_text(path.read_text() + '\n# unauthorized\n')
        with self.assertRaisesRegex(AssertionError, 'protected input'):
            check_helper(root)

    def test_lost_negative_scenario_is_rejected(self):
        root = self.copy("test-setup")
        path = root / "test_retry.py"
        source = path.read_text()
        start = source.index('    def test_cancel_closes_transport')
        end = source.index('    def test_invalid_attempts')
        path.write_text(source[:start] + source[end:])
        with self.assertRaisesRegex(AssertionError, 'cancel_leaks_transport'):
            check_tests(root)

    def test_empty_suite_is_rejected(self):
        root = self.copy("test-setup")
        (root / "test_retry.py").write_text('')
        with self.assertRaisesRegex(AssertionError, 'no tests'):
            check_tests(root)


if __name__ == '__main__':
    unittest.main()
