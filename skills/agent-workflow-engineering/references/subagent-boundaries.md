# Subagent boundaries

Start with a single agent loop loading instructions and tools on demand. Split work into a subagent when context isolation requires it, rather than mirroring team org charts or topic labels.

## When a subagent earns its cost

Introduce a separate subagent only when at least one condition holds *and* the caller needs only a compact conclusion rather than the raw intermediate trace:

1. **Measured context degradation:** Task pass rates drop as single-loop context grows on representative evaluations.
2. **Parallel disposable fan-out:** Independent subtasks can run concurrently in clean contexts whose intermediate tool outputs can be discarded once summarized.
3. **Unresolved tool or prompt interference:** The main loop still misroutes tools or instructions *after* merging overlapping tools, deferring rare tools, and moving reference docs on demand.

Avoid splitting steps whose downstream consumer needs full raw evidence; multi-hop summary chains drop caveats and inflate confidence at every handoff.

## Try single-loop fixes first

- **Tool confusion or bloat:** Group and merge API-shaped tools by user intent, sharpen descriptions, and defer seldom-used tools.
- **Oversized system prompt:** Move task-specific playbooks into on-demand files or skills.
- **State loss across long runs:** Persist plans, constraints, and findings to workspace files so compaction or restarts stay lossless.

## Designing clean handoffs

- Expose subagents to the coordinator as typed tools returning structured verdicts or concise findings while keeping user conversation ownership in one place.
- Pass primary source paths or IDs alongside summaries whenever a downstream step must verify or build on the evidence.
- Specify each subagent's allowed write scope, tool subset, budget, and completion criteria explicitly.

## Consolidating over-split multi-agent pipelines

1. Stand up a small end-to-end task suite before changing topology.
2. Merge back-to-back coupled agents (those passing large context back and forth) first, wrapping remaining agents as tools for a clean baseline.
3. Fold one subagent at a time into on-demand instructions and tools on the main loop, comparing multi-run per-task pass rates and inspecting every pass/fail flip. Keep a split only where the merged loop performs measurably worse.
