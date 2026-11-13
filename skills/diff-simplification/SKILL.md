---
name: diff-simplification
description: Simplify an implemented change while preserving behavior and task-owned edit boundaries. Use when asked to simplify a completed diff or when post-implementation inspection reveals concrete avoidable complexity; not for planning, unfinished implementation, or read-only code review.
---

# Diff simplification

Reduce the maintenance cost of a working change while keeping its behavior identical. Run after implementation and initial checks pass. Returning a no-op is a normal, valid result when every part of the diff earns its keep; line-deletion count is never the goal.

Use this pass only when source edits are permitted on an implemented change. Stay inactive during planning or read-only review, and do not spawn separate review passes.

## Establish edit ownership and baseline

1. Compare the implemented diff with the original request and repository conventions to identify task-owned hunks, including authorized new files.
2. Record a pre-simplification snapshot or diff so you can compare the cleanup against both the working baseline and the original requirements.
3. Read callers, tests, and contracts outside the edit scope before removing anything. Leave unrelated uncommitted hunks in dirty files untouched, and regenerate rather than hand-editing generated or vendored files. Skip any hunk whose ownership is uncertain.

## Evaluate candidates

Look for avoidable complexity introduced or stranded by the change: forwarding wrappers with no contract of their own, round-trip conversions between equivalent internal types, dead compatibility shims, speculative options with no current caller need, duplicate checks of invariants already established at every entry point, or verbose branching replaceable by an existing repository or standard-library operation.

For each candidate, name the maintenance burden removed and verify that observable behavior stays identical across inputs, outputs, public signatures, error types and messages, side effects, telemetry, resource lifetimes, ordering, cancellation, and retry state. Leave any candidate with uncertain equivalence unchanged; optional cleanup never blocks completion, and real defects belong in implementation or review rather than disguised as refactoring.

## Where equivalence breaks

- Touching uncommitted functions or hunks outside the task's scope overwrites another contributor's or tool's work in a shared working tree.
- Replacing an explicit `is None` check with truthiness (`if value:` or `value or default`) changes behavior on falsy values such as `0`, `0.0`, `False`, `""`, and empty containers; adding `.strip()` changes behavior on intentional whitespace strings.
- Inlining a local variable referenced more than once repeats side effects, iterator consumption, allocations, or telemetry; reordering conditions changes short-circuit error behavior.
- Inlining a single-caller wrapper or `try` block that holds a lock across cancellation, closes a resource, translates boundary errors, or persists an idempotency receipt removes a real runtime guarantee.
- Removing validation inside an internal function because one HTTP or CLI handler already validates leaves other callers (background jobs, scripts, direct callers) unguarded.
- Merging two short code blocks that happen to look alike today couples distinct domain rules behind flags, and dense one-liners raise reading cost even when line count shrinks.

## Verify and hand back

Compare the cleanup delta against the pre-simplification snapshot and compare the full final diff against the original request. Re-run relevant checks on the simplified candidate; test results from an earlier revision do not cover later edits. State any check that could not be executed in the current environment.

Summarize the simplifications applied (or report a clean no-op), the checks run on the final candidate, and any remaining caveats. When handing off to an independent reviewer, supply the complete final candidate and original requirements rather than only the cleanup delta.

See [source notes](references/sources.md) for provenance.
