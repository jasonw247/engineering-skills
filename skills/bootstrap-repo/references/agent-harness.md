# Agent-harness profile

This profile covers maintaining a repository that builds a coding-agent harness, as well as building locked skill catalogs read by a harness at runtime. Each harness remains authoritative over its own stages, tool permissions, schemas, budgets, and publication controls.

## Default selection

| Skill | Purpose |
| --- | --- |
| `writing-for-agents` | Draft or review stage prompts, reviewer rubrics, and `AGENTS.md`; remove LLM-isms and tighten prose. |
| `retro` | Trace session failures to their earliest wrong step and turn recurring friction into deterministic checks (`writing-for-agents` dependency). |
| `handoff` | Save workspace-verified continuation state to `<git-common-dir>/handoffs/` without leaking secrets or restricted transcripts. |
| `diagnosing-bugs` | Isolate non-obvious state, concurrency, process, and verification bugs via red-capable reproductions. |
| `codebase-design` | Evaluate module depth, pass-through layers, and testability using the repository's own vocabulary. |

Optional additions (`--skill <name>`): `tdd` (`codebase-design` dependency), `verification-harness`, `domain-modeling`, `code-review`, `diff-simplification`, `agent-workflow-engineering`, `agent-harness-audit`, `technical-document-review`, `change-sequencing`, and `tui-best-practices` (when the harness ships an interactive terminal UI).

## Implementation and independent review

When a harness separates actor implementation from independent review, combine packages as follows:

| Component | Role and boundary |
| --- | --- |
| Host implementation prompt | Actor baseline: reuse repository facilities, finish propagation, justify new boundaries, and run checks. Merge only missing rules from the [compact contract](implementation-quality.md). |
| `diff-simplification` | Optional `actor` pass after implementation and initial checks pass; never run during read-only assessment or planning stages. |
| `code-review` | Independent read-only `reviewer`: evaluate the complete final candidate against the original request and actual check outputs. |
| `codebase-design`, `diagnosing-bugs`, `tdd`, domain skills | Selected on demand when a task involves interface design, hard debugging, test-first slices, or domain rules. |
| `verification-harness` | Used when setting up or strengthening the checks the host runs on candidates, not during each implementation turn. |

A harness without per-task selection injects every configured actor skill into every turn. Leave technique skills such as `tdd` out of that set unless a matched comparison on the host's own tasks shows a gain: in one published series of agent evaluations, test-first prompting underperformed the other testing conditions in both rounds, and the same testing skill has helped with one model and hurt with the next ([Luu, 2026](https://danluu.com/astra-testing/); small samples on spec-implementation tasks). Put verification effort into checks the host runs on every candidate instead, and rerun any skill comparison after a model or effort change.

Run order: implement, optional `diff-simplification`, final checks on the simplified candidate, then independent `code-review`. Pass the reviewer the original user request, the complete final diff, and verified check outputs while withholding the implementer's internal plan, reasoning, and self-assessment so blind spots do not carry over. On re-review loops, keep stable finding IDs (`Resolved`, `Withdrawn`, `Open`).

Lock `roles` (`actor`, `reviewer`) in the [lock format](lock-format.md) are advisory selection hints rather than permission gates: if a host exposes `actor` skills during a read-only planning turn, the host's stage boundary still forbids edits. Check each host's package-count cap (counting transitive dependencies such as `tdd -> codebase-design` and `retro -> writing-for-agents`) when configuring auto-selection.

## Updating pinned catalogs

Project catalogs (`<repo>/.agents/`) take precedence over host catalogs (`--host`) for any matching skill name, even when the host copy is newer. Refresh each project catalog explicitly when rolling out skill updates:

1. Inspect `.agents/skills.lock.json` first so previously added optional skills are included alongside `--profile` flags.
2. Include any legacy lock entries explicitly via `--skill <name>`; the installer rejects partial upgrades that leave invalid retained records, local edits, or broken dependency closures.
3. Frozen in-flight runs keep the skill snapshot captured when the run started.

## Host stage and retention boundaries

Portable skills in `engineering-skills` avoid hardcoding any single harness's stage names or transcript storage rules. Enforce those host-specific contracts in the harness integration layer:

| Stage or policy | How portable skills map onto a bounded harness |
| --- | --- |
| Planning | Keep read-only; extract domain vocabulary, small interfaces, and testable acceptance criteria without running `diff-simplification` or creating unapproved repository files. |
| Artifact-only or toolless stages | When a stage cannot run shell commands or edit files directly, `tdd` and `diagnosing-bugs` emit proposed tests, reproduction commands, and exact edits as structured artifacts while marking execution pending; `github-pr/SKILL.md` stays command-free so publication stages can load it without Git tools. |
| Transcript and artifact retention | When a host prohibits reading or copying raw session logs after completion, configure `retro` and `handoff` runs to read only retained git history, check outputs, and permitted workspace artifacts, and block raw transcript paths in publication gates. |
| Independent review | Run `code-review` (correctness, architecture, and test-evidence thresholds) in read-only mode; return structured findings for the harness's bounded repair loop rather than spawning subagents from inside the skill. |

Never copy interactive instructions that prompt the human, spawn subagents, or push to Git remotes into unattended JSON-only stages.
