---
name: change-sequencing
description: Decide whether and how to split a feature, refactor, or migration into a sequence of reviewable, independently deployable and revertible changes. Use when asked whether or how to split a pull request, plan stacked changes, or sequence a schema, API, or data migration rollout. Not for reviewing a diff, writing commit or PR text, filing GitHub issues, or implementing a change directly.
---

# Change sequencing

Aim for changes that each serve one coherent purpose a reviewer can check completely and an operator can revert cleanly. Splitting carries real costs (more review rounds, temporary compatibility code, and intermediate states to keep green), so recommend keeping a change whole whenever it is already small and self-contained or when splitting would leave fragments whose correctness cannot be judged alone.

## Establish target and repository rules

State the final outcome in one sentence. Check repository conventions for stacked PRs, feature flags, database and service deployment order, and code ownership. Work from the diff when an implementation already exists, or from the requirements and affected call sites when planning ahead.

## Find clean seams

Separate independent concerns so reviewers do not have to untangle mechanical churn from logic changes:

- Land characterization tests first when refactoring under-tested behavior.
- Move, rename, or extract without altering outputs before making a behavior change on the new shape.
- Ship vertical end-to-end slices with their tests rather than landing unused storage, service, and UI layers one horizontal tier at a time.
- Land a new shared module, trait, or adapter together with its first real caller, or with the consumer PR already open in the stack.
- Isolate formatter runs, bulk renames, and codegen updates in dedicated changes with the exact command recorded.
- Isolate large dead-code deletions when they would obscure adjacent logic changes.
- Separate runtime flag flips or rollout configuration when their revert schedule differs from binary deployments.

## Keep migrations safe across rolling deploys

Every change in a sequence must build, pass checks, and leave mixed-version deployments working even if later changes pause or roll back. Sequence schema, API, and background-job migrations with expand, backfill, cut over, and contract:

1. **Expand:** add nullable columns, non-locking defaults, new endpoints, or dual-format readers without removing existing paths. Deploy additive schema changes before application code that queries them.
2. **Backfill or dual-write:** populate new state idempotently in bounded batches with progress checkpoints and divergence checks.
3. **Cut over:** switch readers, writers, and scheduled jobs once validation passes, using an idempotency watermark or single-source boundary so side-effecting jobs never process the same record twice.
4. **Contract:** drop legacy columns, endpoints, and compatibility flags only after no running or rollback-eligible binary still reads or writes them.

For each migration step, record the deploy order, verification signal, rollback action, and precondition gating the next step.

## Sequencing pitfalls

- Dropping or renaming a column (or adding `NOT NULL` without a default) in the same release that removes its code references breaks old application instances during rolling deploys and prevents binary rollback.
- Changing retry counts, sort order, or error handling inside a commit labeled as a mechanical move or rename hides behavior changes from reviewers and couples bug rollbacks to structural moves.
- Slicing one coupled invariant across several PRs purely to match directory ownership leaves each reviewer unable to verify the contract; when a core change cannot be split safely, keep it together, state why, and pair it with stronger tests.

## Deliver

If the change is already small and coherent, recommend keeping it as one pull request and explain why. Otherwise return an ordered table (`Step | Change | Purpose | Depends on | Checks | Rollback / gate`), plus the migration plan when state moves and any unsplittable core with its mitigation. If asked to carry out the split in Git, keep each branch passing checks and do not push or open pull requests without approval.

See [source provenance](references/sources.md) for background.
