---
name: agent-harness-audit
description: Audit or design how a coding-agent harness manages context, prompt caching, tool catalogs, long-running shell commands, and session compaction or memory. Use when building or reviewing an agent harness, diagnosing context bloat or low cache hit rates, or fixing command hangs and lost constraints after compaction. Not for domain agent workflows, single-session retrospectives, or ordinary coding tasks.
---

# Agent harness audit

Establish the target and deliverable first: a read-only audit report, a design proposal, or an implementation change. Inspect the harness code that owns prompt assembly, tool registration, shell and background execution, compaction, and memory loading alongside captured API requests or execution traces. Check provider-specific rules (prompt-cache TTLs, minimum cacheable prefix lengths, explicit cache breakpoints, and tool-call/result pairing rules) in current provider documentation rather than guessing; mark unverified provider rules as needing documentation confirmation.

## Measure from code and real requests

Inspect source files and captured wire payloads rather than trusting README descriptions:

1. Capture both Turn 1 of a fresh session and a later turn, since per-turn injections and history rewrites only appear across turns.
2. Count tokens per section with a named tokenizer and report which tokenizer was used.
3. On representative tasks, record tool-call counts, model round trips, and tool-result sizes.
4. Record any item absent from the code or traces as `unknown` rather than estimating.

## Common harness defects to check

- Injecting second-precision timestamps, live background-task counts, or changing repository status into the system prompt or tool definitions invalidates every cached token after that byte on every turn.
- Rewriting earlier reminder blocks in place or stripping old tool results while leaving orphaned tool-call blocks breaks prefix caching and can trigger provider API errors for unpaired tool calls.
- Moving a slow foreground command to the background by killing the child process and starting a fresh process runs builds, migrations, or non-idempotent scripts twice.
- Resetting a background task's deadline every time its output is read lets hung commands run forever, and omitting completion notifications forces wasteful polling turns.
- Keeping user constraints, architectural choices, or unread background-task completions only inside chat messages drops them as soon as history is compacted.

## Load targeted checklists

Read only the reference files matching the areas under audit:

- Bloated or overlapping tool schemas, wrong tool or argument selection, or oversized tool outputs: [tool catalog](references/tool-catalog.md).
- Every-turn prompt overhead, system-prompt churn, or poor prefix-cache hit rates: [request context](references/request-context.md).
- Hanging dev servers or builds, duplicate background runs, or orphaned child processes: [long commands](references/long-commands.md).
- Constraint loss after compaction, or session memory design: [long sessions](references/long-sessions.md).

Score each applicable checklist item `pass`, `fail`, or `unknown` with file and function, config key, or request-trace evidence. Skip inapplicable items and state why.

## Order fixes by leverage

Simplify or relocate existing pieces before adding new machinery:

1. Merge, rename, or group overlapping tools before building deferred tool-search or programmatic composition layers.
2. Move volatile fields to the end of the turn (or send them only when changed) before tuning cache breakpoints.
3. Write active constraints and task state to files on disk before introducing subagent handoff layers (see `agent-workflow-engineering` when subagent topology is in scope).

For each recommendation give the checklist item, evidence, exact change, trade-off, and verification metric while keeping permission prompts, input validation, hooks, and user-visible chat history intact.

## Confirm changes experimentally

Test one harness change at a time on a pinned model, toolset, and repository snapshot across an end-to-end task suite with independent checks, running multiple trials per task. Compare per-task pass rates, tasks that flipped between pass and fail (reading the trajectory of each flip), model round trips, input and output tokens, cache hit rate, and elapsed time. Never claim a measured improvement from code inspection alone, and re-test scaffolding after model upgrades.

See [source provenance](references/sources.md) for origin and unverified provider assumptions.
