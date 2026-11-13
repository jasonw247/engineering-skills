# Coding-agent TUI specialization

Apply these rules alongside [SKILL.md](../SKILL.md) when the terminal interface supervises coding agents, tool calls, approvals, or multi-agent runs.

## Activity timeline and composer

- Default conversational agents to a **scrollable timeline + persistent multiline composer + single-line status bar**, opening history search, full tool outputs, diffs, and approval modals on demand. Use a task-board layout instead when supervising many autonomous runs in parallel.
- Group routine read/search calls into collapsible summaries keyed by stable run/step IDs, while keeping file edits, failing checks, warnings, and pending approvals expanded or immediately visible. Search and filter must still match text inside collapsed tool calls.
- Render concrete execution metadata on tool steps: command, working directory, exit code, duration, and truncation markers; affected file paths on edits; actual pass/fail counts on test runs; and objective plus live status on child agents. Never mark a tool or test green from model prose alone; use controller-verified exit status.

## Control, approvals, and diff integrity

- **Match controls to real transport semantics.** Distinguish interrupting the current model turn, killing an active shell command, detaching a background daemon, and deleting a queued prompt. Label queued user messages accurately (`queued for next turn` vs `injected mid-turn`), and preserve unsent composer drafts across interrupts and cancellations.
- **Bind approvals to exact operations.** Display the immutable command or write target, effective arguments, working directory, and risk scope before asking for confirmation. Default focus to deny, bind approval to that exact payload (re-prompt if arguments change), and enforce the check in the runner. A pending approval in one subagent must not mark sibling running tasks as blocked.
- **Separate proposed diffs from applied workspace changes.** Label whether a shown diff is a pending proposal (`apply` / `reject`) or already written to disk (`inspect` / `revert`). Working-tree diffs can include manual user edits; track provenance or snapshot hashes before offering one-key revert.

## Stream and state decoupling

- Keep the agent controller authoritative for run state, permissions, and receipts; the TUI renders an event stream projection. Represent dropped or out-of-order events explicitly rather than guessing completion.
- Drain child process stdout/stderr independently of UI frame rate. Drop or coalesce intermediate progress frames under load, never terminal lifecycle or approval events, and mark truncated tool output with byte/line counts and the path to the full log if spooled to disk.
