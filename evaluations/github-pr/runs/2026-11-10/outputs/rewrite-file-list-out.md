## Summary
During the 2026-10-30 outage, every sync request retried on its own (up to
five attempts with exponential backoff). Clients with hundreds of concurrent
requests sent the recovering service several times its normal load, and
recovery took 40 minutes instead of 5. This PR caps the total retries each
client makes. All requests on a `SyncClient` now share one retry budget that
refills over time. When the budget is empty, requests fail fast with a
dedicated error.

## Changes
- **Shared retry budget per client.** Each `SyncClient` has a `RetryBudget`, a
  token bucket that starts full, refills continuously at its per-minute rate,
  and never holds more than that rate. Every retry, on any request, takes one
  token. The rate is set with the new `retry_budget` constructor argument and
  defaults to 10 retries per minute.
- **Fail fast when the budget is empty.** If a request fails and no token is
  left, the client raises `RetryBudgetExceeded` right away. It does not sleep
  and try again. `max_attempts` and the exponential backoff between attempts
  still apply as before.
- **New error type.** `RetryBudgetExceeded` subclasses `SyncError` and carries
  the failing request's id.
- **Tests.** New tests check that a client with a budget of 2 makes exactly 3
  transport calls and then raises `RetryBudgetExceeded`, and that an empty
  budget becomes usable again once enough time has passed (using a fake clock).

## Impact
- **Applies to all clients by default.** Existing clients get the
  10-per-minute budget without opting in. Under sustained failures, callers
  will see errors sooner than they did before.
- **Error raised after the last attempt has changed.** When a request uses up
  `max_attempts`, the client now raises `RetryBudgetExceeded`, even if budget
  remained. It also raises immediately after the final failure. Before, it
  slept once more and then raised `SyncError("exhausted attempts")`. Code that
  catches `SyncError` still works. Code that checks the exact type or message
  will see a different result. Reviewers may want to consider whether running
  out of attempts should keep its own error.
- **Scope of the budget.** The budget lives in memory on each client instance.
  Separate clients and separate processes do not share it, so total load still
  grows with the number of clients.
- **Reverting.** Pass a large `retry_budget` to restore close to the old retry
  volume, or revert this PR. No data, schema, or configuration-file changes.

## Verification
- Not recorded: which test suites ran on this revision, and their results. The
  earlier description said "tests: passed" without naming them. Please confirm
  before merging, for example by running `tests/test_client.py`.
- Not verified: behavior during a real outage or under concurrent load. Refill
  timing is tested only with a fake clock.

## Linked issues
Closes #41
