# Long sessions, compaction, and memory

Compaction trims older turns so the active conversation fits the context window; memory carries stable project or user facts across sessions. Both discard detail, so durable designs persist important constraints, decisions, and task status to readable files early rather than relying on chat history alone.

## Checklist

Inspect the compaction and memory code paths and configuration. Score each item `pass`, `fail`, or `unknown` with file/line, config, or runtime evidence.

| # | Item | Question |
| --- | --- | --- |
| 1 | Clearing before summarizing | Are bulky old tool outputs pruned or offloaded to files before falling back to lossy full-history summarization? |
| 2 | Call/result pairing | When pruning tool outputs, are `tool_use` and `tool_result` blocks kept or removed together according to the provider's pairing rules (verified against provider docs)? |
| 3 | Durable state in files | Are active constraints, plans, and progress written to files on disk rather than held only in chat turns? |
| 4 | Guided manual compaction | Can the user specify what constraints or next steps to preserve when triggering compaction manually? |
| 5 | Trigger headroom & fallback | Does auto-compaction fire early enough to fit both the current response and the summary prompt, and degrade gracefully if the summarization call fails? |
| 6 | Prefix-cache preservation | Does the compaction call reuse the existing cached prefix, and is compaction infrequent enough that the new prefix amortizes rebuild cost? |
| 7 | User-visible history & budgets | Does compaction rewrite only the model-facing prompt while keeping the user's UI transcript intact and excluding internal summary calls from user step quotas? |
| 8 | Model continuation cue | Is the model informed that context is managed automatically so it does not prematurely stop work to "save tokens"? |
| 9 | Concise project instructions | Are always-loaded instruction files (such as `AGENTS.md`) kept short and restricted to stable repo rules? |
| 10 | Memory scoping | Are session scratchpads, project conventions, and user preferences separated so ephemeral to-dos never pollute long-term memory? |
| 11 | Visible truncation | When memory files exceed their token cap, are high-priority sections loaded first and is truncation surfaced explicitly? |
| 12 | Human inspectability & hard gates | Can users view, edit, or disable memory files directly, while non-negotiable safety rules live in deterministic hooks or checks? |

## Diagnosing drift

Repeatedly broken constraints, re-asked questions, or resumed work heading in an abandoned direction after compaction all point to state that lived only in summarized turns. Trace which checklist item above dropped that state before proposing a larger context window or subagent split.
