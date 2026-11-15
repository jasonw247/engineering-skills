# Diff simplification 0.2.0 maintenance evaluation

Two fresh raw-input-only evaluators simplified synthetic completed changes using
the exact upgraded skill. Independent acceptance passed on both outputs.
The helper trial removed duplicate parsing and repair state by reusing the
contract-compatible facility. The test trial shared repeated setup and completion
assertions while keeping seven independently named scenarios. All eight mutants
were detected, including cancellation leakage and retrying a non-retryable error.

These are development fixtures, labeled training. They do not establish a gain
over an agent without the skill or justify a Hans controller pass. Evaluation
scope was instructed, not OS-enforced; do not treat it as containment evidence.
No transcripts or reasoning are retained. Exact input/output hashes, check counts,
mutation outcomes and limits are in [results.json](results.json).

## Reproduce

From the repository root, run:

```sh
python3 -B -m unittest discover -s evaluations/bootstrap-repo -p 'test_*.py' -v
python3 -B -m unittest discover -s evaluations/diff-simplification -p 'test_*.py' -v
```

For each retained output, copy its corresponding raw fixture directory to a
fresh temporary directory, replace only `loader.py` or `test_retry.py` with the
retained file, then run:

```sh
python3 -B evaluations/diff-simplification/maintenance_acceptance.py helper-reuse /path/to/copied-helper-fixture
python3 -B evaluations/diff-simplification/maintenance_acceptance.py test-setup /path/to/copied-test-fixture
```

Only raw fixtures and the skill belong in an evaluator's permitted scope.
`cases.json`, acceptance code, retained outputs and this record are evaluator
answers and must be excluded. For a security-sensitive or live Hans campaign,
enforce that separation outside the agent-readable sandbox, not just by prompt.
Behavioral acceptance also passes the original completed fixtures by design;
maintenance removal and useful diagnostics require separate artifact review.
