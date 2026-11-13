# PR #57 closeout proposal

Nothing has been written to GitHub. This is a proposal. Each write below needs your approval first.

## What merged

- PR: https://github.com/example/sync-service/pull/57, `state: MERGED` at 2026-11-09T18:22:04Z.
- **Base branch: `stack/retry-budget`, not the default branch `main`.** The snapshot reports `stack/retry-budget` as "not yet merged into main".
- `closingIssuesReferences` is empty. The body says `Closes #41`, but a closing keyword only fires when the base is the default branch, so it did not close #41. The body also says `Part of #40`, which never closes anything. The branch `feat/retry-budget-client-41` also points to #41. Neither commit message references an issue.
- So the retry-budget change exists on the stack branch. It is not on `main` yet, and it has not reached users of `main`.

## Proposed actions

| Issue | Current state | Proposed action | Evidence |
| --- | --- | --- | --- |
| #41 Sync clients cause retry storms during outages | Open (child of #40) | **Leave it open and add a comment.** Do not close it yet. Close it as completed once `stack/retry-budget` merges into `main`, or sooner if the repository's release convention counts stack-branch merges as done. Draft comment: "The fix merged in #57 (per-client retry budget) into `stack/retry-budget`. Because that isn't the default branch, `Closes #41` didn't fire. This closes once `stack/retry-budget` lands on `main`. Deferred follow-ups: #A, #B, #C, #D." | Base is `stack/retry-budget`, stack not merged into `main`, and `closingIssuesReferences: []`. The snapshot doesn't include #41's body or acceptance criteria, so before closing I'd run `gh issue view 41` to confirm #57 meets all of them. |
| #40 Make sync resilient to upstream outages | Open, sub-issues 1/2 completed | **No action now.** #41 looks like its last open child. When #41 closes, check #40's "done when" criteria before proposing to close it. If you approve the follow-ups below as sub-issues of #40, #40 stays open until they close too. | `subIssuesSummary: {total: 2, completed: 1}`, `Part of #40` in the PR body, #41's parent is 40. |
| #44 Add jitter to sync backoff | Open | **Optional comment, no state change.** Draft: "#57 added a placeholder for this at `src/sync/client.py:31` (`# TODO: jitter the backoff`). That's the place to start." #57 didn't reference this issue, so I'd only comment if you want the link recorded. | The added TODO duplicates this issue, so no new follow-up is drafted for it. |

## Follow-up issues (drafts)

These come from #57's Follow-ups section and its review threads. The jitter TODO is skipped because #44 already covers it. The snapshot lists no other open issues on these topics, so none of these duplicate an existing issue. I'd run a quick `gh issue list --search` before filing to confirm.

These are deferred parts of #40's work, so each one is drafted as a sub-issue of #40. For B, it's your call whether the gateway client belongs under #40 or should be a standalone issue. Size estimates are rough guesses: the snapshot has no diff, so they're based only on the scope described.

### A. Export the remaining sync retry budget as a metric

```markdown
Part of #40

## Context
#57 added a per-client retry budget to the sync client so outages stop causing retry storms
(https://github.com/example/sync-service/pull/57). Right now nothing shows how much budget is
left, so nobody can tell a client is about to run out until its retries start getting rejected.

## Outcome
Each sync client's remaining retry budget is exported as a metric that can be alerted on.

## Acceptance criteria
- [ ] A metric reports each client's remaining retry budget
- [ ] The metric updates when budget is spent and when it refills
- [ ] A test using the fake clock from #57 checks the reported value across spending and refilling

## Out of scope
- Writing the alert rules themselves

## Notes
Starting point: the budget added in #57 (`src/sync/client.py`).
Size: about 80-150 changed lines (estimate).
Related #57
```

### B. Cap gateway client retries with a retry budget

```markdown
Part of #40

## Context
#57 capped sync retries with a per-client budget (https://github.com/example/sync-service/pull/57).
The gateway client has the same unbounded retry loop, which #57 left alone, so it can still cause
retry storms during an upstream outage.

## Outcome
Gateway client retries are bounded by a retry budget, the same way sync client retries are after #57.

## Acceptance criteria
- [ ] During a sustained upstream failure, gateway client retries stop once the budget runs out
- [ ] The budget refills over time, and a fake-clock test covers that
- [ ] The budget mechanism from #57 is reused or shared rather than copied, or the issue says why not

## Out of scope
- Changing retry behavior of the sync client (done in #57)

## Notes
Size: about 150-300 changed lines (estimate), more if the budget gets pulled out into a shared module.
Related #57
```

### C. Make the retry budget configurable per environment

```markdown
Part of #40

## Context
In #57's review, someone asked whether the retry budget should be configurable per environment.
The author answered "later, tracked in follow-ups", but #57's Follow-ups section doesn't list it,
so it's recorded here (https://github.com/example/sync-service/pull/57).

## Outcome
Each deployment environment can set its own retry budget size and refill rate without a code change.

## Acceptance criteria
- [ ] Budget size and refill rate can be set per environment through the service's existing configuration
- [ ] When they aren't set, the defaults match what #57 shipped
- [ ] Invalid values are rejected at startup with a clear error

## Notes
Open question: does this apply to the gateway client budget too (see the gateway follow-up)?
Size: about 60-120 changed lines (estimate).
Related #57
```

### D. Chain the last transport error onto RetryBudgetExceeded

```markdown
Part of #40

## Context
A review thread on #57 that is still unresolved points out that `RetryBudgetExceeded` drops the last
transport error, so whoever handles the exception can't see why the retries were failing
(https://github.com/example/sync-service/pull/57).

## Outcome
When the retry budget runs out, the raised `RetryBudgetExceeded` carries the last transport error
as its cause.

## Acceptance criteria
- [ ] `RetryBudgetExceeded` is chained to the last transport error (for example `raise ... from err`)
- [ ] A test checks that the cause is the last transport error

## Notes
Starting point: `src/sync/client.py`.
Size: about 20-40 changed lines (estimate).
Related #57
```

## If approved, the write order

1. Create follow-ups A-D, then link each one as a sub-issue of #40.
2. Post the comment on #41 (with the new issue numbers filled in). Leave #41 open.
3. Optionally comment on #44.
4. Later, once `stack/retry-budget` merges into `main`: comment on #41 and close it as completed, then check #40's "done when" criteria.

Nothing else gets closed, relabeled, or edited.
