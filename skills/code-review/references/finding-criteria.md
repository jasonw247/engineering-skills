# Finding criteria

## Qualifying thresholds

| Category | Required evidence | Insufficient on its own |
| --- | --- | --- |
| **Correctness** | An allowed input or state follows a reachable path to a wrong result or corrupted state. | Hypothetical inputs excluded by a documented caller contract. |
| **Compatibility** | A supported caller, wire format, or documented behavioral guarantee breaks. | Changing undocumented incidental output that no caller relies on. |
| **Security** | Untrusted input reaches a changed trust boundary and triggers a concrete bypass, injection, leak, or denial of service. | Generic advice to "sanitize all inputs" without a reachable sink. |
| **Performance** | Changed algorithmic complexity, I/O fan-out, or memory growth causes material cost at realistic scale. | Micro-optimizations on cold paths without a plausible workload. |
| **Simplification** | A specific existing operation or direct call preserves behavior while removing duplicate logic or maintenance burden. | "This helper only has one caller." |
| **Tests** | A changed requirement or high-risk failure path has no check that would fail if broken. | Coverage falling short of an arbitrary percentage target. |

## Evaluating test evidence

State what existing verification proves and what it leaves uncovered:

- A unit test proves a helper's output on chosen inputs, not that production callers pass matching shapes or units.
- Type checking proves static signatures align, not runtime parsing, SQL queries, or concurrency behavior.
- Mocked integration tests prove local wiring, not real downstream payloads or error codes.
- Author-written tests often mirror the code's assumptions (or recompute expected values with the same formula). Verify tests ran against the *final* candidate without filters that skipped affected suites.

## Code shapes worth tracing

Treat these patterns as leads to trace rather than automatic findings; report only when tracing confirms a threshold above:

| Observed shape | When it becomes a finding |
| --- | --- |
| Identical branch bodies, or conditions that are always true/false | The dead or collapsed branch drops a case required by the specification. |
| Mutating getters/predicates, or return values violating the declared signature | Callers relying on purity or declared types hit unexpected state or unhandled `None`/errors. |
| Caught exceptions discarded or re-raised without cause | Actionable failures turn into silent partial writes, wrong defaults, or undiagnosable stack traces. |
| Error convention mismatch across sibling functions (e.g., returning `None` where siblings raise) | Callers handling the established convention misinterpret the result as success. |
| Half-completed migrations or parallel old/new code paths | Callers diverge in behavior, or the leftover path retains the bug/cost the patch claims to remove. |

Guard against syntactic false positives before reporting: a method named `lock` may acquire an advisory file lock designed to span an `await`, and overwriting a dictionary key inside an `except` block may sit on a mutually exclusive path from the initial write. Unenabled linter rules are never findings by themselves.

## Writing minimal corrections

Name the exact invariant to preserve and the smallest local change that restores it. If retrying after a timeout duplicates a remote mutation, specify the idempotency key or reconciliation check needed rather than writing "handle retries carefully." When a critical invariant cannot be determined from the repository, ask a direct conditional question instead of asserting an unconditional bug.
