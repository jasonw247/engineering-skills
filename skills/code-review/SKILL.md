---
name: code-review
description: Review a proposed code change for demonstrated defects, compatibility breaks, and material avoidable cost. Use when asked to review code, a diff, or a pull request; stay read-only unless fixes are requested. Not for implementing new features from scratch.
---

# Code review

Establish the requirements, changed files or revision range, compatibility guarantees, and checks already run. Read relevant repository instructions alongside callers, callees, and tests outside the diff so cross-file contract breaks are visible. When no diff is supplied, state the bounded review surface inferred from the request.

Compare the complete current candidate against the original request rather than relying on the author's summary, plan, or latest cleanup commit. Stay read-only unless the user asks for fixes.

## Trace behavior and cost

Follow concrete inputs and failure paths through the change, focusing on:

- Wrong outputs, unmet requirements, or broken caller, schema, and ordering guarantees.
- Swallowed or misclassified errors, non-idempotent retries, unpropagated cancellation, concurrency races, and leaked connections, locks, or file handles.
- Untrusted input crossing an authentication, authorization, path, query, or deserialization boundary with a concrete failure or exploit path.
- Material runtime or memory regressions under realistic workloads, or duplicated logic, dead shims, and unnecessary indirection that a specific behavior-preserving simplification removes.

Consult [finding criteria](references/finding-criteria.md) for category thresholds, test-evidence checks, and code patterns worth tracing. When practical within the authorized workspace, reproduce a suspected bug with a small isolated calculation or scratch check, separating observed results from inferred consequences. Do not install dependencies, run expensive suites, mutate external systems, or execute destructive tests without explicit scope and authorization.

## Watch for common review mistakes

- Reading only changed diff lines misses unmigrated callers, sibling entry points that bypass a new guard, and return-value conventions broken across module boundaries.
- Before reporting two bugs along one execution path, check whether an earlier defect makes the downstream branch unreachable; trace what executes today, and re-evaluate downstream branches once the upstream bug is fixed.
- Distinguish pre-existing technical debt or runtime cost from regressions introduced or worsened by the patch. Report pre-existing problems only when they fall within the requested scope or materially affect the change, and label their origin accurately.
- Verify that cited test runs ran against the final candidate without a filter that skipped affected suites, and check whether author-written tests share the implementation's blind spot.
- One caller, one implementation, function length, or an unenabled lint rule is not a defect on its own; demonstrate a broken contract or a concrete behavior-preserving simplification that removes real cost.

## Format qualifying findings

Report only demonstrated defects, compatibility breaks, or material avoidable costs, ordered by impact. For each finding give:

1. Identifier, severity, and category (using repository conventions when present).
2. Exact file and line location with a plain description of the failure or cost.
3. Concrete evidence: reachable input and path, contract mismatch, reproduction, or behavior-preserving simplification.
4. Smallest corrective direction and any missing fact that conditions confidence.

If nothing meets the threshold, report zero findings plainly and note material untested behavior separately without framing it as a defect.

## Re-review after author responses

Inspect the complete revised candidate against the requirements again rather than checking only the author's reply. Keep every prior finding's original ID (never drop, renumber, or silently downgrade an item) and assign an explicit status:

- **Resolved:** the current candidate no longer has the problem.
- **Withdrawn:** counterevidence or contract scope shows the earlier finding was mistaken.
- **Open:** the problem remains in the current candidate; explain why the fix or rebuttal does not hold.

Re-check earlier rebuttals against the repaired code: fixing one defect can make a previously unreachable path reachable and invalidate an earlier rebuttal. Report defects introduced by the repair under new IDs.

## Finish within the authorized mode

In assessment mode, leave source files untouched and return findings with the scope and checks performed. When fixes are requested, edit only confirmed issues within scope, preserve public contracts and unrelated hunks, run relevant repository checks, and summarize the changes and results. Do not launch other agents, choose model families, or impose a multi-reviewer workflow from this skill.

See [sources](references/sources.md) for provenance and limits.
