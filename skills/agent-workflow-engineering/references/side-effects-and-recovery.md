# Side effects and recovery

## Closing the remote-effect crash gap

External mutations typically follow `persist intent → call provider → persist receipt`. A worker can crash between any two steps, and local intent persistence alone does not create a distributed transaction with the remote API:

| State observed on recovery | Safe recovery action |
| --- | --- |
| Intent persisted, dispatch provably never started | Submit with the stored logical operation ID and approved payload. |
| Provider lookup confirms prior completion | Record the receipt locally and advance without calling the mutation again. |
| Active provider idempotency window covers the key | Retry with the identical idempotency key and payload within that contract. |
| Provider confirms non-execution within its consistency guarantees | Submit if approval and overall deadline remain valid. |
| Outcome unknown (timeout, network drop, ambiguous 5xx) | Move to an explicit `uncertain` / reconciliation state; never blindly re-run non-idempotent effects. |
| Provider deduplication window expired before recovery | Treat missing provider lookup records as inconclusive; escalate or reconcile via domain records before resubmitting. |

### Key scoping and concurrency

- Build idempotency keys from `(workflow_id, logical_action_id)` rather than raw payload hashes alone so two legitimate identical actions in separate steps can both run, while pairing the key with a payload digest to catch mutated retries.
- Guard concurrent recovery workers with optimistic version checks or bounded leases so a stalled worker waking up late cannot overwrite newer state or dispatch a second call.
- Where a third-party API offers neither idempotency keys nor deterministic lookup, state the resulting `at-least-once` or manual-reconciliation boundary explicitly rather than claiming `exactly-once` semantics.

## Retries and fallible compensations

- Retry transient transport/rate-limit errors at the failing step boundary with both attempt and deadline caps; avoid nested retry loops across SDK, activity, and workflow layers that multiply load.
- Model each compensation (refund, revoke, cancel) as a first-class action with its own operation ID, preconditions, retry policy, and failure escalation, and reconcile uncertain forward actions before attempting to compensate them.

## Bound approvals and cooperative cancellation

- Bind human approvals to `(approver, action_id, payload_digest, workflow_version, expires_at)`. Deduplicate repeated approval clicks, and invalidate or re-prompt when the underlying payload or state changes before execution.
- Separate `cancellation_requested`, `aborted_before_dispatch`, `completed_before_cancel`, and `compensation_required`: cancelling a local task or HTTP request never guarantees the remote server aborted an in-flight mutation.

## Fault-injection checks

Verify recovery with deterministic fakes or fault injection at each crash point, checking both persisted workflow state and mock provider call counts; matching final assistant text alone never proves side effects ran once.
