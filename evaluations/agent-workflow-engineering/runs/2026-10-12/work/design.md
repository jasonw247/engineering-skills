# Shipment workflow recovery design

Keep the existing application and transactional database. Ordinary code owns the workflow, approval validation, provider calls, and recovery. The model drafts the request only. This is a design and failure walkthrough; no shipment or integration test was executed.

The provider's 24-hour deduplication window cannot guarantee recovery of an uncertain shipment after a 72-hour outage. An `ABSENT` lookup after that interval means the record is unavailable, not that the shipment never occurred. Preserve that distinction in durable state and stop automatic submission until independent reconciliation establishes the outcome. A new workflow framework cannot remove this remote/local transaction gap.

## Durable ownership and identities

Store one workflow row plus an append-only event/attempt ledger in the current database. A transactional outbox (or an equivalent database-backed due-work table) makes committed transitions discoverable to existing workers; duplicate delivery is expected.

Persist these fields before any provider mutation:

- `workflow_id` and a random `operation_key` allocated for this logical shipment intention, with a database uniqueness constraint. Separate legitimate intentions receive separate keys even if their payloads are identical. A payload hash detects changes; it is not the deduplication identity.
- Canonical payload and its schema/version/hash: customer, fully validated address, item and quantity, plus any other shipping fields approved by the human. Freeze the approved payload. Preserve sensitive fields under existing access/retention controls; logs may use IDs and hashes.
- Approval event ID, approver identity/authority, workflow/action identity, exact payload version/hash, approved-at timestamp, and any application-defined validity limit. Enforce authorization in code. A duplicate event ID is a no-op; a second event approving the same action/version cannot create another operation.
- State, state-version for compare-and-set updates, due time, worker claim/lease and generation, cancellation request metadata, first possible submit time, attempt records, retry counters, elapsed-time budget, and last provider observation. Keep outcome knowledge independent from the cancellation flag.
- Provider receipt, receipt ID and matching key/payload evidence when available; reconciliation evidence; terminal reason; workflow/schema version and safe migration metadata.

The database is authoritative for intended action, approval, progress, and cancellation requests. The provider receipt and independent reconciliation establish external shipment facts. Conversation history, a model's confidence, and worker memory are never authoritative. A successful response must be durably saved; if that write fails, recovery must still be possible from the preexisting operation record.

## State transitions

| State | Meaning and permitted transitions |
| --- | --- |
| `DRAFTING` | One bounded model call proposes a typed payload. Code validates it. Valid draft → `AWAITING_APPROVAL`; invalid/exhausted drafting → `REJECTED` or request correction. |
| `AWAITING_APPROVAL` | Human approval must match the current action and exact canonical payload version. Valid approval + code validation → `READY`; rejection → `REJECTED`; cancellation → `CANCELLED_NO_EFFECT`; expired unsent request → `EXPIRED_NO_EFFECT`. |
| `READY` | Approved immutable intent and durable dispatch work exist; no provider attempt has been authorized. Worker revalidates authority, payload, cancellation, and deadline, then atomically claims the row and records `ATTEMPTING` before calling the provider. Cancellation/expiry wins if committed first, resulting in a no-effect terminal state. |
| `ATTEMPTING` | An attempt may execute or already have executed. Receipt → `SUCCEEDED`; a documented rejection proving no effect → `REJECTED` or bounded safe retry as applicable; lost/ambiguous response, crash, or lease loss → `OUTCOME_UNKNOWN`. Cancellation records a flag and forbids additional submits; it cannot claim no effect. |
| `OUTCOME_UNKNOWN` | Reconcile with `lookup(operation_key)`. Matching receipt → `SUCCEEDED`; `UNKNOWN` → remain unknown with bounded lookup retry; `ABSENT` → retain uncertainty unless a stronger contract proves non-execution and no old attempt can still execute. When automatic reconciliation budget ends, retention expires, or safety cannot be established → `RECONCILIATION_REQUIRED`. |
| `RECONCILIATION_REQUIRED` | Terminal for automated dispatch, externally unresolved. Durable work item for operator/provider investigation. Verified shipment receipt → `SUCCEEDED`; proof of non-execution plus no possible late execution → `CANCELLED_NO_EFFECT`, `EXPIRED_NO_EFFECT`, or `READY` depending on current cancellation, deadline, and authorization. Absence of proof leaves this state in place. |
| `SUCCEEDED` | Verified shipment outcome and receipt saved. Terminal for shipment creation. If cancellation was requested, expose “shipment created; cancellation requested” and any unresolved follow-up need. Never relabel a known created shipment as cancelled with no effect. |
| `REJECTED`, `CANCELLED_NO_EFFECT`, `EXPIRED_NO_EFFECT` | Terminal only when a provider effect is known not to have happened and no attempt can still create it. Late/duplicate events cannot restart dispatch. |

A business deadline can end willingness to ship, but cannot turn an unknown outcome into “failed with no shipment.” Use the cancellation/deadline reason alongside `RECONCILIATION_REQUIRED` where appropriate. Completion requires a validated, durably stored receipt; exhausted retries are not success.

Only application transition code changes these states. Workers use short database transactions, uniqueness constraints, compare-and-set state versions, and an atomic row claim. Do not hold a database transaction open across a network call. A stale worker may report a genuine receipt through an idempotent reconciliation handler, but may not overwrite a newer state or payload. An expired lease alone never authorizes another submit of an uncertain operation.

## Typed provider boundary and submission contract

Expose ordinary-code adapters, not a general model-controlled shipping tool:

- `submit(operation_key, approved_payload) -> Receipt | KnownNoEffectRejection | UncertainOutcome`.
- `lookup(operation_key) -> Receipt | ABSENT | UNKNOWN`.

Validate provider responses, associate receipts with the intended key and shipment, and classify malformed responses as uncertain. Persist the key, frozen payload, approval binding, and an attempt-start record before submitting. The state transition and dispatch work insertion must be one database transaction. Never submit a changed payload under an existing key, including after the provider's retention window. A changed requested action requires a new approved version and logical identity; if the previous action is uncertain, resolve it before treating a replacement as a retry.

Transactionally moving `READY` to `ATTEMPTING` closes the local duplicate-dispatch race, not the remote effect/receipt gap. A paused old worker may still have sent or later send a request. Database fencing prevents stale local writes; it does not fence the provider. The design therefore does not let lease expiry or lookup absence alone create a new sender. Check the cancellation/deadline fence immediately before I/O, and treat any already-authorized/in-flight request as potentially effective even if cancellation races with that check.

Compute a conservative provider retry horizon from the earliest persisted time a submit could have reached the provider, not the latest retry or worker restart. Do not assume retries refresh retention. The given contract only guarantees deduplication for matching key and payload during 24 hours; key scope, retention start, concurrency behavior, and processing deadlines need confirmation from the provider contract before enabling uncertain-submit retries. Retain local identity/attempt records beyond the 72-hour outage and reconciliation lifetime; provider expiry must never cause local rekeying of the same unresolved intention.

## Retry rules and concrete bounds

These are proposed application settings, not measured operating limits. Persist counters and deadlines so a crash does not reset them. The single workflow layer owns retries; disable unaccounted SDK retries.

| Operation/failure | Policy |
| --- | --- |
| Draft model call | At most one call per draft version, with a 30-second request deadline, 2,000 output-token cap, and a configured monetary admission ceiling. Invalid output is rejected; human correction creates an explicit new draft version. The model does not loop or call shipping. |
| Validation, approval mismatch, access failure | Permanent for that version; no retry loop. Existing human authorization is reused only for its exact still-valid payload. Do not introduce another blanket approval step. |
| `READY` work before any attempt | Retry local claim/transaction work with bounded backoff. No remote effect is possible until `ATTEMPTING` commits. Revalidate approval/deadline before the first submit. |
| Submit failure proven to precede all network transmission | Same operation key and frozen payload may be retried, at most three submit attempts total and at most 10 minutes from the first attempt, while authority/deadline remain valid. “Proven” requires a local pre-send failure classification, not an HTTP timeout or connection loss after sending. |
| Lost acknowledgment, timeout, ambiguous provider error | Mark `OUTCOME_UNKNOWN`; lookup first. Default for the supplied contract is lookup-only recovery, because the contract does not establish a bound on when delayed requests can execute. No automatic resubmit based merely on lack of a receipt. |
| Optional uncertain-submit retry | Enable only after verifying that all retries/old requests will be processed within the same guaranteed provider deduplication interval, with adequate clock/transport margin, no cancellation, unchanged authorization/payload, and no possible late request beyond that horizon. Reuse the identical key. Keep the same three-attempt/10-minute cap. A client timeout alone does not establish a server processing deadline. Without this stronger contract, keep the lookup-only default. |
| Receipt received but local write fails | Retry only the idempotent receipt/database write while receipt is available; never resubmit shipping to repair a database error. If worker memory is lost, use lookup and reconcile. |
| Lookup `UNKNOWN` | Up to eight calls over 30 minutes in an automatic reconciliation episode, using backoff with jitter; suggested delays 0, 5, 15, 45, 120, 300, 600, 600 seconds. Persist attempt count and an absolute episode deadline. Retries do not resubmit. |
| Lookup `ABSENT` | Record the observation/time. It is not durable proof of non-execution or absence of an in-flight request. Repeated reads may find a late receipt within the lookup budget; otherwise move to reconciliation required. After possible retention expiry, stop automatic dispatch immediately. |
| Database/provider outage or budget exhaustion | Release no new effect. Preserve due-work/unknown outcome in the database when available; reconciliation resumes from durable state. If the database is unavailable before `ATTEMPTING` commits, do not call the provider. Persisted expired budgets move to the appropriate terminal or reconciliation state on recovery. |

Automatic reconciliation may stop without determining the external result. An operator can authorize a new bounded read-only investigation episode without authorizing a new shipment. Lookup is safe after 72 hours and can still recover a retained receipt; an absent record leaves the outcome unresolved. No repeated no-progress model actions are possible because the model drafts once; provider retry limits supply explicit no-progress termination for the deterministic control flow.

Approval validity and the business shipping deadline are not specified in the request. Preserve existing application policy and store its values; do not invent an expiry that silently revokes user authorization. If the application requires a validity window, choose it before implementation. Expiry before a known-unsent first attempt stops submission; expiry while uncertain stops new attempts but continues reconciliation.

## Required failure walkthroughs

| Failure/event | Durable evidence and recovery | External effect conclusion |
| --- | --- | --- |
| Crash before submit while still `READY` | No `ATTEMPTING` transition exists and code cannot call before it. A new worker can claim and submit after revalidation. | No previous call was authorized; first submission is safe. |
| Crash after recording `ATTEMPTING` but physically before calling | Recovery cannot generally distinguish this from a sent request. Move to unknown, then lookup/reconcile. Only trustworthy proof of no send permits the known-unsent path. | Do not infer “not sent” solely from a missing receipt. Availability may be sacrificed to avoid an unproven duplicate. |
| Submit succeeds; acknowledgment lost | Intent/key/payload and possible-start time survive. Mark unknown; lookup. Found receipt is saved idempotently and completes workflow. Unknown/absent observations follow bounded reconciliation. | A shipment may already exist; never allocate another key to retry it. |
| Submit succeeds; local receipt write fails | If response survives, retry database receipt recording only. After crash, lookup using persisted key. Found receipt completes without another submit. | The external shipment is not rolled back by a local database failure. |
| Recover after 72 hours; lookup `ABSENT` | Past guaranteed retention. Record expired-retention uncertainty and move to `RECONCILIATION_REQUIRED`; no submit. Investigate with provider/customer/fulfillment records via authorized operational processes. | Could be one shipment or none. The supplied APIs cannot resolve this case reliably. Do not call it a failed shipment or manufacture exactly-once recovery. |
| Duplicate approval events | Inbox uniqueness and action/version state transition consume approval once. Repeated approval for the same action does not create another operation or duplicate outbox intent. Distinct later shipment intentions use distinct keys. | One logical action is scheduled; identical payloads for distinct intentions remain legitimate distinct actions. |
| Cancellation while outcome is `UNKNOWN` | Persist cancellation requested, stop all new submits, continue bounded lookup. A found receipt yields succeeded-with-cancellation-requested; absent/unknown yields unresolved reconciliation. | Cancellation does not establish that the provider stopped or never shipped. |

The provider exposes no cancellation or compensation API in these requirements. Do not invent one. If a created shipment needs interception or return, it becomes a separately authorized operational action with its own durable identity and fallible outcome once a supported process is known. Do not compensate a shipment whose existence has not been established.

## Restarts, late events, and validation

Pin in-flight rows to their workflow/schema version. Migrate explicitly without changing the operation key, canonical payload, approval binding, first possible attempt time, or counters; otherwise drain old handlers. Restart scans due/unknown rows and reconstructs state from durable records. Deduplicate approval and receipt events by event/receipt identity and correlate them to the current action version. Reject stale approvals for changed or terminal actions. Accept a late verified receipt as external truth even after an automatic-recovery deadline or cancellation request; record an auditable correction rather than ignore the real effect.

Use fake provider and database fault injection before integration: crash on both sides of the `ATTEMPTING` commit, before send, after provider acceptance, before/after receipt write; duplicate/reordered approvals; concurrent workers and a delayed stale worker; 23-hour and 72-hour recovery; `FOUND`/`ABSENT`/`UNKNOWN`; cancellation at each boundary; payload mutation; distinct identical-payload intentions; exhausted counters; and malformed or mismatched receipts. Assert the database state and the fake provider's actual effect count separately. Expected invariant: no new automatic submit occurs for unresolved outcomes after retention expiry, and no terminal no-effect state is asserted while an old attempt could still execute. The design's walkthrough is not an executed fault-injection result.

This design meets recovery needs by preserving certainty where available and making unresolved outcomes explicit. It does not provide an unconditional exactly-once effect guarantee. If the business requires automatic definitive completion after a 72-hour outage, the stated provider contract is insufficient: it needs durable receipt lookup or a deduplication/processing contract covering the maximum outage and delayed requests, or another independently reliable reconciliation mechanism. The existing transactional stack can implement the proposed state machine without selecting a new framework.
