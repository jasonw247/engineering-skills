---
name: agent-workflow-engineering
description: Design, implement, or diagnose agent application control flow, state ownership, typed tools, side-effect idempotency, retries, human approvals, and crash recovery. Use when building or debugging an agent-powered application workflow; not for using a coding assistant on ordinary code or auditing a coding-agent harness's prompt cache.
---

# Agent workflow engineering

Scope the design to the workload, existing stack, authority boundaries, execution lifetime, and failure modes. Plain functions and schema validation suffice for a single request-scoped model call; introduce state machines, durable checkpoints, or multi-step recovery only where branching, resumption, or external mutations require them.

## Control flow and state ownership

Keep mandatory sequencing, permission checks, and schema validation in deterministic application code, calling models where interpretation or open-ended choice adds value. Store authoritative workflow state, transition history, and action receipts separately from chat transcripts, retrieved passages, and temporary caches. On replay-based durable runtimes, isolate model calls, clocks, random IDs, and external I/O inside recorded activities or steps so orchestrator replay remains deterministic.

Default to one agent loop with tools and instructions loaded on demand; read [subagent boundaries](references/subagent-boundaries.md) before splitting work across subagents or when consolidating an existing multi-agent pipeline.

## Typed tools, approvals, and external mutations

Validate caller identity, permissions, preconditions, and tool arguments in application code; model outputs and retrieved text never grant authority. When human approval is required, bind the approval record to the actor, logical action ID, payload digest or version, and expiration window so edited or expired actions cannot reuse stale authorization.

Every external mutation faces crashes before dispatch, after remote commit before local receipt persistence, and during recovery. Persist a stable logical operation ID and intent before calling the provider, and pair retries with provider idempotency keys, transactional outboxes, or status-lookup reconciliation. Read [side effects and recovery](references/side-effects-and-recovery.md) for uncertain outcomes, retries, approvals, and compensations.

## Failure modes to check

- Writing a local `done` flag only after a remote API call leaves a crash window where the remote mutation succeeded and recovery runs it a second time.
- Deriving idempotency keys solely from a payload hash either blocks legitimate repeat actions with identical arguments or fails to deduplicate a retry whose metadata changed; scope keys to `(workflow_id, logical_step_id)` and check payload digests separately.
- Replaying an entire multi-step workflow when step 3 fails re-executes unguarded side effects from steps 1 and 2; retry at the failed step boundary within attempt and deadline caps.
- Treating timeouts or expired deduplication windows as proof of non-execution causes duplicate side effects; record an explicit uncertain or reconciliation state when the provider outcome cannot be verified.
- Treating compensation (refunds, revocations, cancellation calls) as an infallible database rollback ignores that compensations can fail too and cannot undo physical shipments or sent messages; give each compensation its own operation ID and retry contract.

## Execution bounds and verification

Bound attempts, wall-clock deadlines, token or cost budgets, and repeated zero-progress tool loops. Correlate late or duplicate webhook and approval signals against current state, and guard concurrent workers with leases or compare-and-swap transitions. Consult [runtime selection criteria](references/runtime-selection.md) only when choosing a runtime or when the current stack fails a concrete requirement.

Test or trace each boundary: crash after intent write, crash after remote commit before receipt write, duplicate signal delivery, expired approval or deduplication window, mid-flight cancellation, and budget exhaustion. Never claim `exactly-once` external effects without naming the cooperating provider mechanism and its retention scope.

See [sources](references/sources.md) for provenance, limits, and related documentation.
