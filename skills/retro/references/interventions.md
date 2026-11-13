# Interventions

Use when the user had to step into the agent's work repeatedly, or when deciding where a retrospective fix belongs. Respect repository retention rules and keep raw session transcripts out of tracked files.

## Classify each intervention

An intervention is an action the user had to take inside work the agent could have completed on its own. Recurring interventions mark a missing check, pointer, or trigger.

| Role | What the user did | Typical signs |
| --- | --- | --- |
| Retry | Prompted the agent to continue after a stall or recoverable error | "Try again", "keep going" |
| Judge | Evaluated output quality because no check existed | "Too verbose", "Did you run the integration test?" |
| Approve | Unblocked a routine step the agent paused on unnecessarily | "Yes, run the local tests" |
| Carry | Supplied context already present in the repo or docs | "Check the migration script in `db/`", "Use `uv run`" |
| Trigger | Manually kicked off the same recurring chore across sessions | Identical opening prompts across runs |
| Stand in | Ran a command, copied files, or inspected state the agent could reach | Pasting local command output the agent could run itself |

Record each recurring intervention with its role, a one-line summary of what happened, and its root cause.

## Pick the earliest durable exit

State the concrete outcome wanted and what deterministic signal (exit code, lint, schema check, diff size) can verify it without human grading. Then pick the first option below that holds the fix:

1. **Delete** the stale instruction or broken config that caused the stall.
2. **Update the closest existing file** (`AGENTS.md`, an existing skill, `Makefile`/`justfile`, or task prompt).
3. **Add a deterministic check** (linter rule, script, or test) that turns human judging into a runnable command.
4. **Create a skill** when the same multi-step workflow recurs across sessions (typically three or more times) and does not belong in always-loaded instructions.
5. **Automate the trigger** via a git hook, CI job, or scheduled task.
6. **Update global user instructions** only when the pattern spans multiple repositories; remove one stale global line for every line added.
7. **Adjust how the task is requested** when the gap came from an underspecified prompt (such as an unstated target branch or output constraint).

## Verify improvement

Track whether the intervention stops recurring without hurting task quality; fewer user nudges paired with worse output means the user gave up correcting rather than that the environment improved.

Adapted and reworded from `lifting-loops` in [MiniMax-AI/mcode-stack](https://github.com/MiniMax-AI/mcode-stack/tree/d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0/stacks/jiachen/skills/lifting-loops) (MIT, inspected 2026-11-10). Cross-tool transcript scanning, private ledgers, proposal files, and memory cleanup were omitted.
