---
name: handoff
description: Capture verified workspace state, key decisions, ruled-out approaches, and exact next steps in an untracked handoff document so another session or agent can resume active work cleanly. Use when pausing work, switching sessions, or handing a branch to another agent; not for writing commit messages or PR descriptions, conducting a session retrospective, or writing permanent project documentation.
---

# Session handoff

Write a concise, state-verified handoff file so a fresh agent or session can resume work cold without rediscovering context or repeating dead ends.

## Steps

1. **Verify workspace state from disk.** Run read-only checks (`git status`, `git branch --show-current`, `git log -1 --oneline`, `git diff --stat`) and inspect the latest output of tests or linters run in this session. Label any item not freshly confirmed as `unverified`.
2. **Choose a durable, untracked save path:**
   - Use the path requested by the user or the repository's documented handoff convention when one exists.
   - Inside a Git repository with no convention, write to `<git-common-dir>/handoffs/<branch-or-slug>.md`, resolving `<git-common-dir>` with `git rev-parse --git-common-dir`. Using `--git-common-dir` puts handoffs in the shared `.git` directory rather than `.git/worktrees/<name>/`, so another worktree can find the file and `git worktree remove` will not delete it, while keeping the file out of `git status` and OS `/tmp` cleanup.
   - Outside a Git repository (or when `<git-common-dir>` is read-only), write to `~/.local/state/agent-handoffs/<project>-<slug>.md` (or `%LOCALAPPDATA%\agent-handoffs\` on Windows). Use `$TMPDIR` or `/tmp` only when requested or for immediate same-machine handoffs, and warn the user that OS temp folders are cleared on reboot or periodic cleanup.
   - Update an existing handoff file for the same task in place rather than creating duplicates.
3. **Redact secrets and follow retention rules.** Replace every API key, token, password, cookie, connection string, or PII value with `<REDACTED>`. Omit raw conversation transcripts and internal reasoning, and link to existing specs, plans, issues, commits, or diffs by path or URL instead of copying their full text.
4. **Include what the next session needs** (adjusting emphasis when the user specifies the next step):
   - Goal and completion criteria: what the task delivers and what remains.
   - Verified workspace state: checkout path, branch, base branch, HEAD commit, uncommitted or untracked files, stashes, and running background tasks.
   - Checks run: exact commands executed on the current tree with pass/fail results, plus checks not yet run since the last edit.
   - Decisions and constraints: settled choices with their reasons, and boundaries the next session must keep.
   - Ruled-out approaches: dead ends already tried and why each failed.
   - Next steps in order, starting with the first concrete command or file edit to run.
   - Pointers to relevant files, issues, PRs, and local paths of installed skills suited to the remaining work.
5. **Report** the saved file path and a two-line summary of current status and next action.
