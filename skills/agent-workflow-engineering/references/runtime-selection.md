# Runtime selection criteria

Consult this reference only when asked to choose an execution runtime or when the existing stack cannot satisfy a demonstrated durability or state requirement.

| Workload shape | Required runtime capability |
| --- | --- |
| Single bounded model call or fixed call chain | Plain application code with schema validation, timeouts, and structured tracing. |
| Inspectable multi-step branching loop | Explicit state transitions, step/token caps, and state serialization (lightweight state machine or graph). |
| Resumable human-in-the-loop sessions | Persistent state checkpoints, versioned approval/resume tokens, and idempotent tool boundaries. |
| Multi-day workflows across deploys and outages | Durable execution log/event history, timers and external signals, deterministic replay or step journaling, and schema-evolution rules. |
| Scheduled corpus/data materializations | Partition-aware data-pipeline scheduler with asset lineage and backfill tracking. |

## What durable runtimes do and do not solve

- Restoring a workflow checkpoint or replaying an event log recovers **orchestrator position**, not remote API atomicity: external mutations still require provider idempotency keys or reconciliation lookups.
- Verify the installed runtime version's exact rules for deterministic replay, non-deterministic activity boundaries, payload size limits, in-flight workflow versioning, operational footprint, and tracing export rather than relying on marketing claims. Keep a working adopted stack unless a concrete gap justifies migration.
