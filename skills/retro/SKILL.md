---
name: retro
description: Analyze a completed or stalled coding-agent session to turn concrete mistakes, detours, and repeated user interventions into automated checks, scripts, navigation pointers, or concise instruction updates. Use when asked for a session retrospective or post-mortem on agent friction; not for auditing an agent harness codebase, writing a session handoff, or debugging an application bug.
---

# Session retrospective

Turn concrete friction from a coding session into durable improvements to the repository's checks, commands, or instructions.

## Steps

1. **Gather allowed session evidence.** Inspect the session specified by the user (defaulting to the current one): `git log`, `git diff`, check outputs, plans, and any transcripts or telemetry permitted by repository retention rules. Never copy excluded transcripts or secrets into tracked files.
2. **Trace the timeline before proposing changes.** Reconstruct the sequence of intent, action, result, and next decision. Identify:
   - the earliest wrong assumption or detour (repeated file searches, wrong CLI flags, retries with identical inputs, ignored error output, broken constraints);
   - for a failed run, the first step where recovery became unlikely;
   - for a slow or fragile success, the step that wasted the most work or nearly broke.
   When the user had to step in repeatedly, classify each intervention using [interventions](references/interventions.md).
3. **Match each problem to the lowest-maintenance fix:**

   | Observed session problem | Preferred fix |
   | --- | --- |
   | Mechanical mistake (banned API, import cycle, formatting, missing type/lint check, file-layout rule) | Deterministic check in the repository's existing linter, type checker, test suite, pre-commit hook, or CI workflow. Inspect `package.json`, `Cargo.toml`, `pyproject.toml`, `Makefile`/`justfile`, and `.github/workflows/` first so an existing unwired script gets wired up rather than reinvented. |
   | Agent spent many turns hunting files, entry points, or non-obvious coupling | Short navigation pointer (1 to 2 lines naming the authoritative file or command) in `AGENTS.md` / `CLAUDE.md` or module docs. |
   | Judgment rule that no static check can decide (cross-module idioms, domain boundary rules, review criteria) | Scoped guidance in the repository's existing standards doc, review guide, or an on-demand skill. Read [writing-for-agents](../writing-for-agents/SKILL.md) before drafting or editing instructions. |
   | Bloated `AGENTS.md` / `CLAUDE.md` diluted constraints or carried dead rules | Delete rules that never change behavior, move task-specific procedures into skills or linked docs, and remove a stale line whenever adding a new global rule. |
   | Missing observability or token-heavy tool calls (blind retries without server logs, huge unfiltered command output) | Tee dev-server logs to a readable file, add a focused check alias, or document the compact query flag (`--json`, `-q`, path filter). |

4. **Verify proposed checks.** Before recommending or landing a new lint, script, or test check, confirm that it fails on the original bad state with an error message pointing to the fix and passes on the clean code.
5. **Present prioritized recommendations.** Order candidates by impact and recurrence. Report plainly when a clean session warrants no changes, skip one-off flukes, and ask before editing repository-wide instruction files or CI gates unless applying fixes was already requested.

## Where retrospectives go wrong

- Adding prose rules to `AGENTS.md` for invariants a linter or small script can check costs tokens on every turn and still gets missed under context pressure.
- Proposing changes for files or stages the repository does not use (creating unrequested standards docs or assuming multi-agent review pipelines exist) creates dead documentation; fit fixes into the files and CI jobs already present.
- Appending every post-mortem note to the root instruction file buries core invariants; generalize recurring patterns or prune obsolete lines alongside additions.
