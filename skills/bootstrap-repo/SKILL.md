---
name: bootstrap-repo
description: Select and install curated skills from engineering-skills into a target repository or host catalog. Use when setting up repository skills, choosing a skill profile, or updating a previously bootstrapped selection; not for authoring new skills or modifying target application code.
---

# Bootstrap a repository

Copy complete, hash-locked skill packages from a local `engineering-skills` checkout into a target repository's `.agents/skills/` directory, retaining bundled references, metadata, and licenses.

## 1. Inspect and choose packages

1. Identify `--source` (the `engineering-skills` checkout; pass `--source` explicitly whenever running `bootstrap.py` from an installed copy outside `engineering-skills`) and `--target` (the destination repository), asking only if either path is ambiguous.
2. Read the target's `AGENTS.md`, README, existing `.agents/skills/` folders, and globally enabled plugins so local conventions stay intact and skills are not installed twice.
3. Read [the registry](references/registry.json) to pick the smallest profile or `--skill` list addressing the task; dependencies are included automatically. When setting up an agent harness or locked catalog, also read [the integration profile](references/agent-harness.md).
4. If the user asked only for a recommendation, stop after presenting the selection and preview output. When a profile, skill list, or setup was requested, proceed from preview to `--apply` without asking a second time.

## 2. Preview, then apply

Run the standard-library installer (Python 3.9+):

```sh
# 1. Preview planned actions and conflicts (writes nothing)
python3 <bootstrap-skill>/scripts/bootstrap.py --source <engineering-skills> --target <target-repo> --profile agent-harness

# 2. Apply once preview reports no conflicts
python3 <bootstrap-skill>/scripts/bootstrap.py --source <engineering-skills> --target <target-repo> --profile agent-harness --apply
```

Flags:
- `--list`: print registered skills and profiles without needing `--target`.
- `--skill <name>` (repeatable): select individual skills, or add optional skills on top of `--profile`.
- `--host <dir>`: write a host-level catalog (`<dir>/skills/` and `<dir>/skills.lock.json`) instead of `<target>/.agents/`.

## Safety and catalog upgrade rules

- `--apply` writes only the selected folders and `.agents/skills.lock.json` ([format](references/lock-format.md)), replacing a legacy `skill-repo.lock.json` automatically when only the old name exists. Unselected installed skills, `AGENTS.md`, and Git history stay untouched, with no network calls or commits.
- The installer stops before writing if any destination is a symlink, an unmanaged folder with the same skill name, or a managed copy with local edits. Preserve local edits and resolve conflicts with the user.
- Reapplying a profile updates only the packages in that selection. When retained lock records lack current metadata, or when earlier optional skills also need refreshing, pass those packages explicitly with `--skill <name>` so every upgraded package gets current files and hashes.
- Project copies in `<repo>/.agents/skills/` override same-name host copies (`--host`), so refresh `--target` catalogs explicitly even after updating `--host`.

## 3. Verify and report

Confirm the JSON output reports `"verified": true`. Keep the target's `AGENTS.md` focused on repository-specific commands and rules, adding a short pointer only if the host requires one and never pasting skill bodies into `AGENTS.md`. Check host discovery directly (such as `/skills` in Codex, restarting if needed) rather than inferring discovery from file presence alone.

Report the installed or updated paths, optional skills left out, checks performed, and any remaining integration steps.
