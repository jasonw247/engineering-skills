# Engineering skills for coding agents

Twenty-three self-contained `SKILL.md` packages for software engineering tasks: reviewing diffs, writing Rust and async Python services, building terminal UIs, diagnosing retrieval loss, auditing agent harnesses, and preparing commits, issues, and session handoffs. Each folder under [`skills/`](skills/) works on its own: standard `SKILL.md` frontmatter, relative links only, and no runtime dependencies, so any harness that loads skill folders (for example `.agents/skills/` or `.claude/skills/`) can use it.

## What sets these skills apart

- **Focused on traps that pass naive builds.** Capable models already know language syntax and common workflows. Most `SKILL.md` files run 30 to 80 lines (loading deeper references only when relevant) and targets bugs that survive happy-path tests: `asyncio.create_task` weak references getting garbage-collected mid-`await`, `let _ = guard;` dropping a Rust guard immediately, terminal `Release` key events firing actions twice, or `Closes #N` misfiring on stacked pull requests.
- **Conservative with your repo and Git state.** Review and audit skills stay read-only unless you ask for fixes. Setup skills (`python-project-setup`, `rust-project-setup`) inspect existing package managers, linters, and compiler versions before touching configuration. GitHub skills draft text without pushing or opening PRs unasked, omit AI and tool `Co-Authored-By` trailers, and preserve human DCO sign-offs.
- **Portable folders with optional SHA-256 locking.** Copy any skill directory by hand, or use [`bootstrap.py`](skills/bootstrap-repo/scripts/bootstrap.py) (Python 3.9+ standard library) to preview changes, pull in required sibling skills, record file hashes in `skills.lock.json`, and block overwrites if a managed file has local edits.
- **Evaluation suites that report limits and null results.** Every package has routing and behavioral test cases under [`evaluations/`](evaluations/). Suites where earlier fixtures informed edits separate `training` calibration cases from uncontaminated `held-out` checks, pin run records to exact file hashes, and publish flat comparisons plainly—including [`technical-document-review` 0.1.1 matching an unassisted baseline 12/12](evaluations/technical-document-review/runs/2026-10-29/report.md) at higher token use.

## Quick start

### Install with `bootstrap.py` (locked, preview-first)

Preview an installation from a local checkout (writes nothing; Python 3.9+ stdlib only):

```sh
python3 skills/bootstrap-repo/scripts/bootstrap.py --target ../your-repository --profile engineering
```

Apply once the preview shows no conflicts:

```sh
python3 skills/bootstrap-repo/scripts/bootstrap.py --target ../your-repository --profile engineering --apply
```

Common install patterns:

- **Pick specific skills:** omit `--profile` or layer extras onto one:
  ```sh
  python3 skills/bootstrap-repo/scripts/bootstrap.py --target ../your-repository --skill code-review --skill rust-idioms --apply
  ```
- **Claude Code or shared host directories:** `--target` writes to `<repo>/.agents/` (`skills/` + `skills.lock.json`). Use `--host <dir>` to write `<dir>/skills/` and `<dir>/skills.lock.json` directly—for example `--host ../your-repository/.claude` or `--host ~/.codex`:
  ```sh
  python3 skills/bootstrap-repo/scripts/bootstrap.py --host ../your-repository/.claude --profile engineering --apply
  ```
- **Inspect available profiles and metadata:** run `python3 skills/bootstrap-repo/scripts/bootstrap.py --list` or read [`registry.json`](skills/bootstrap-repo/references/registry.json). Inside this checkout, `.agents/skills/bootstrap-repo` also exposes `$bootstrap-repo` directly. It is a Git symlink, so on Windows clones without `core.symlinks` enabled it checks out as a text file; run the script by its `skills/` path instead.

### Copy folders directly

Every package under `skills/<name>/` is a plain directory with no build step. Copy `skills/<name>/` into `.agents/skills/` or `.claude/skills/`. Only three skills depend on a sibling folder, which you must copy too: `tdd` requires `codebase-design`, `retro` requires `writing-for-agents`, and `github-issues` requires `change-sequencing`.

## Skill catalog

### Code review, testing, and design

| Skill | Use when | Key boundary |
| --- | --- | --- |
| [`code-review`](skills/code-review/SKILL.md) | Reviewing a diff or PR for demonstrated bugs, compatibility breaks, and avoidable cost, or re-reviewing fixes. | Read-only unless fixes are requested; separates pre-existing debt from patch regressions; tracks `Resolved` / `Withdrawn` / `Open` IDs. |
| [`diff-simplification`](skills/diff-simplification/SKILL.md) | Removing avoidable complexity in an implemented change's task-owned hunks while preserving behavior. | Post-implementation only (never planning or read-only review); treats no-op as valid; leaves concurrent dirty hunks alone. |
| [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md) | Isolating non-obvious bugs or performance regressions with red-capable repros and tagged probes. | Redacts credentials in captured output; strips `[DEBUG-...]` probes before finishing. |
| [`tdd`](skills/tdd/SKILL.md) | Building features or fixes in vertical red-green-refactor slices against stable behavioral seams (`codebase-design`). | Confirms the test fails for the expected reason first; avoids tautological and mock-choreography tests. |
| [`codebase-design`](skills/codebase-design/SKILL.md) | Evaluating module depth (interface complexity vs hidden behavior), pass-through layers, temporal splits, and seams. | Keeps repository terminology and justified security or resource seams; avoids false-depth mega-methods. |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Aligning ambiguous domain terms across code and glossaries, or recording architecture decision records (ADRs). | Uses existing glossary/ADR paths first and confirms before creating `GLOSSARY.md` or `docs/adr/`. |

### Languages, services, and terminal UIs

| Skill | Use when | Key boundary |
| --- | --- | --- |
| [`python-project-setup`](skills/python-project-setup/SKILL.md) | Initializing, repairing, or modernizing `pyproject.toml`, `src/` layout, PEP 735 dependency groups, and wheel checks. | Keeps existing project tools; verifies built wheels from outside the checkout; skips packaging churn on routine edits. |
| [`python-service-engineering`](skills/python-service-engineering/SKILL.md) | Implementing or diagnosing `asyncio` lifetimes, admission backpressure, `TaskGroup` cancellation, and boundary validation. | Scoped to service concurrency, resource ownership, and trust boundaries rather than pure-Python helpers or packaging. |
| [`rust-project-setup`](skills/rust-project-setup/SKILL.md) | Configuring or ratcheting `rust-toolchain.toml`, `[workspace.lints]`, `cargo-deny`, `nextest` + doctests, and CI gates. | Keeps existing tools; checks version-gated Cargo settings against installed `rustc -V` and `cargo -V`. |
| [`rust-idioms`](skills/rust-idioms/SKILL.md) | Shaping Rust parameter types, constructors, errors, `Drop` guards, `#[non_exhaustive]`, patterns, and C FFI. | Leaves mechanical lints to Clippy; flags review findings only when they carry concrete consequences. |
| [`tui-best-practices`](skills/tui-best-practices/SKILL.md) | Building or reviewing interactive terminal UIs: raw-mode panic cleanup, key-event filtering, cell widths, and piped output. | Scoped to interactive terminal apps rather than non-interactive CLI flag parsing, web apps, or desktop GUIs. |

### Git, GitHub, and session continuity

| Skill | Use when | Key boundary |
| --- | --- | --- |
| [`change-sequencing`](skills/change-sequencing/SKILL.md) | Deciding whether and how to split a feature, refactor, or expand/contract migration into stacked PRs. | Recommends a single PR when a change is already coherent; never pushes or opens PRs without approval. |
| [`github-pr`](skills/github-pr/SKILL.md) | Writing commit messages, PR titles, and PR descriptions that match repo conventions without AI attribution. | Repo rules and commit history override Conventional Commits; preserves human DCO sign-offs; drafting writes nothing. |
| [`github-issues`](skills/github-issues/SKILL.md) | Drafting, sizing, and filing issues or sub-issues, and reconciling linked issues after a PR merges (`change-sequencing`). | Treats ~500 changed lines as a split-check prompt rather than a hard cap; every GitHub write requires approval. |
| [`handoff`](skills/handoff/SKILL.md) | Writing a disk-verified continuation brief with Git state, settled decisions, ruled-out dead ends, and next steps. | Defaults inside Git repos to `<git-common-dir>/handoffs/` so worktrees share it without dirtying `git status`; redacts secrets. |
| [`retro`](skills/retro/SKILL.md) | Tracing session friction to its earliest wrong turn and converting recurring mistakes into scripts, lints, or concise docs (`writing-for-agents`). | Prefers failing-first deterministic checks over adding prose rules to `AGENTS.md`; respects log-retention rules. |

### Agents and retrieval systems

| Skill | Use when | Key boundary |
| --- | --- | --- |
| [`agent-workflow-engineering`](skills/agent-workflow-engineering/SKILL.md) | Designing agent control flow, state ownership, scoped idempotency keys, human approvals, and remote-effect crash recovery. | Uses plain functions for simple calls; never claims `exactly-once` external mutations without a cooperating provider mechanism. |
| [`agent-harness-audit`](skills/agent-harness-audit/SKILL.md) | Auditing a coding-agent harness's tool schemas, per-turn prompt overhead, prefix caching, background commands, and compaction. | Measures from source code and captured wire payloads; verifies harness changes with multi-run task experiments. |
| [`rag-engineering`](skills/rag-engineering/SKILL.md) | Building lexical/hybrid baselines, tracing stage-by-stage retrieval or packing loss, and enforcing metadata/ACL contracts. | Fixes the earliest failing pipeline stage before adding rerankers, new embeddings, or graph layers. |
| [`rag-evaluation`](skills/rag-evaluation/SKILL.md) | Designing protocols, running executable benchmarks, or auditing confounded RAG comparisons and multi-set rubrics. | Separates `Design`, `Run`, and `Assess`; keeps abstentions out of claim-precision denominators; never extrapolates toy fixtures to production. |

### Technical writing and catalog management

| Skill | Use when | Key boundary |
| --- | --- | --- |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md) | Drafting or auditing `SKILL.md` / `AGENTS.md` triggers and instructions, or stripping LLM-isms and tightening technical prose. | Preserves exact facts, units, modal strength, and prohibitions while revising prose. |
| [`technical-document-review`](skills/technical-document-review/SKILL.md) | Assessing, editing, or reassessing specs and engineering reports for factual, math, citation, and contract accuracy. | Read-only in `Assess` and `Reassess`; keeps protected sections byte-for-byte intact; saving edits never authorizes publishing. |
| [`bootstrap-repo`](skills/bootstrap-repo/SKILL.md) | Previewing, installing, or upgrading curated skill profiles and locked catalogs in a repository or host directory. | Previews before `--apply`; refuses symlinked destinations, unmanaged same-name folders, and local edits. |

## Profiles, roles, and catalog upgrades

- **Profiles:** `--profile engineering` installs seven general-purpose skills (`writing-for-agents`, `retro`, `handoff`, `diagnosing-bugs`, `codebase-design`, `tdd`, `domain-modeling`). `--profile agent-harness` installs the first five for harness development. Layer domain skills on top with `--skill <name>`.
- **Actor and reviewer separation:** `skills.lock.json` tags each package with advisory `roles` (`actor`, `reviewer`) and `cues` ([v1 lock format](skills/bootstrap-repo/references/lock-format.md)). When running separate implementation and review turns, pair `code-review` (`reviewer`, withholding the implementer's internal plan) with optional `diff-simplification` (`actor` post-implementation pass) using the [harness integration guide](skills/bootstrap-repo/references/agent-harness.md#implementation-and-independent-review) and [compact implementation contract](skills/bootstrap-repo/references/implementation-quality.md).
- **Safe upgrades:** project catalogs (`<repo>/.agents/`) take precedence over host catalogs (`--host`) for matching skill names, so refresh project catalogs explicitly when rolling out updates ([upgrade notes](skills/bootstrap-repo/references/agent-harness.md#updating-pinned-catalogs)). Legacy `skill-repo.lock.json` files migrate atomically to `skills.lock.json`.

## Evaluations and local checks

- `skills/<name>/`: deployable package (`SKILL.md`, optional `references/`, `scripts/`, `agents/openai.yaml`, `LICENSE`, `LICENSE-<upstream>`).
- `evaluations/<name>/`: `cases.json` routing and completion specifications, synthetic `fixtures/`, and retained `runs/` snapshots.

See the [evaluation procedure](evaluations/README.md) and [validation record](evaluations/validation.md). Packaging checks verify frontmatter, registry metadata, and relative link containment; forward behavioral trials record task outcomes only at their tested file hashes. Establishing a causal gain over an unassisted agent requires matched baseline comparisons on held-out tasks.

Run the installer, lock-format, and package-integrity test suite plus snapshot verification locally:

```sh
python3 -m unittest discover -s evaluations/bootstrap-repo -p 'test_*.py' -v
python3 evaluations/technical-document-review/check_results.py evaluations/technical-document-review/runs/2026-10-29
```

## Provenance and license

[MIT](LICENSE). Seven packages adapted from [`mattpocock/skills`](https://github.com/mattpocock/skills) retain their package-level `LICENSE` files and upstream copyright notices, and the two packages that restructure [`MiniMax-AI/mcode-stack`](https://github.com/MiniMax-AI/mcode-stack) checklists ship its MIT notice as `LICENSE-mcode-stack`; [UPSTREAM.md](UPSTREAM.md) documents all adapted packages and open-source prior art.
