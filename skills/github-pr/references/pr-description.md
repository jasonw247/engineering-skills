# Pull request description examples

## Template when the repository has none

```markdown
## Summary
Two to four sentences: what changes for users or maintainers, and why.

## Changes
- Behavior or concern, described in terms a reader can follow without the code.
- Another material change. Name a file only when it helps navigation.

## Impact
Who or what is affected; compatibility or migration; risk and blast radius; how to revert.

## Rationale
Why this approach; alternatives considered and why they were rejected.

## Verification
- `command actually run`: result
- Not verified: what remains and why

## Linked issues
Closes #41

## Follow-ups
- Deferred scope, with an issue link if one exists
```

Leave out sections that would be empty. A small fix may need only Summary, Verification, and Linked issues.

## File inventory and its rewrite

Weak:

```markdown
## Summary
Add retry budget

## Changes
5 files changed:
- `src/sync/client.py` (M)
- `src/sync/config.py` (M)
- `src/sync/errors.py` (M)
- `tests/test_client.py` (M)
- `docs/configuration.md` (M)

## Verification
- tests: passed
```

The summary repeats the title. The file list is already in the diff view and does not say what changed or why. "tests: passed" does not say which tests ran or on what.

Better:

```markdown
## Summary
During an outage every sync request retried independently, so clients
hammered the recovering service and slowed recovery. This adds a
per-client retry budget: retries draw from a shared allowance that
refills over time, and once it is empty requests fail fast.

## Changes
- Retries now draw from a budget shared by all requests on a client
  (10 per minute by default).
- When the budget is empty, requests raise `RetryBudgetExceeded`
  immediately instead of sleeping and retrying.
- The budget is configurable with `sync.retry_budget` and documented
  in the configuration guide.

## Impact
Callers that retried forever during outages now see an error sooner
and must handle `RetryBudgetExceeded`; in-tree callers already handle
the base `SyncError`. No data or schema changes. To revert, set the
budget very high or revert this PR.

## Rationale
A per-request retry cap would still let many concurrent requests
retry at once. A budget per client bounds the total load a client
generates. A shared budget across processes would need coordination
storage and was not needed for the current deployment.

## Verification
- `pytest tests/test_client.py`: 14 passed, including budget
  exhaustion and refill.
- Not verified: behavior under a real outage; the refill timing is
  tested with a fake clock.

## Linked issues
Closes #41
```

## Linking issues

| Situation | Write |
| --- | --- |
| PR targets the default branch and fully resolves the issue | `Closes #41` |
| PR targets another branch, such as a stacked PR or a release branch | `Refs #41`; close after the change reaches the default branch |
| PR delivers part of the issue | `Part of #41` |
| Several issues | One keyword each: `Closes #41, closes #42` |
| Issue in another repository | `Closes owner/repo#41` |

Only link issues that the request, branch, commits, or the user identify. Do not guess from similar titles.
