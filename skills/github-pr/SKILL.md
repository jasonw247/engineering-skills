---
name: github-pr
description: Write commit messages, pull request titles, and pull request descriptions that follow the repository's conventions, explain the change to a human reader, and carry no tool attribution. Use when committing, opening or updating a pull request, or rewriting a commit message or PR description. Not for reviewing a change, splitting it into smaller pull requests, or creating and closing issues.
---

# Commit and pull request text

Write for the person who reviews the change, merges it, or finds it in history months later. Work from the final diff and the request it serves, not from the session's chronology. This file covers the text. When you have Git or GitHub tools and were asked to commit, push, or open or update a pull request, also follow [writing to Git and GitHub](references/writing-to-git.md).

## Follow the repository's convention

Use the first of these that exists:

1. Explicit rules: commitlint or similar configuration, CONTRIBUTING, repository agent instructions, the pull request template, `.github/copilot-instructions.md`, or `.github/instructions/`.
2. A consistent history: when recent commit subjects and merged PR titles share a form, that form is the convention, even if it is not Conventional Commits.
3. Otherwise Conventional Commits: `type(scope)!: summary`, with `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`. The scope is a noun from the repository's own vocabulary.

Find out whether pull requests are squash-merged. When they are, the PR title usually becomes the commit subject on the default branch, so write it in the commit convention. Repository settings decide this: under GitHub's default, a single-commit PR uses that commit's own title and message instead, so keep the commit subject and the PR title consistent.

## Commit messages

- Subject: imperative, 72 characters or fewer, no trailing period. It should complete "If applied, this commit will …".
- Body, only when the subject does not make the reason obvious: the problem, the approach chosen, and any consequence a later reader needs. Wrap at 72 characters. Do not list files or narrate how the edit was made.
- One logical change per commit. A change that needs two types is probably two commits.
- Breaking change under Conventional Commits: add `!` and a `BREAKING CHANGE:` footer that states the migration.
- Footers use `Token: value` form, for example `Refs: #123`.

[Commit message examples](references/commit-message.md) contrast weak and strong messages.

## Attribution and sign-off

Do not add any of these to commits, PR titles, or PR descriptions unless the repository's rules require them: `Co-Authored-By` lines for tools or models, "Generated with" lines, emoji or tool footers, harness markers, or model names. A host may add attribution on its own; the host's settings control that, not this text.

Keep human Developer Certificate of Origin sign-offs separate from tool attribution. When the repository requires DCO sign-off (it says so in CONTRIBUTING, runs a DCO check, or every commit in its history has `Signed-off-by:`), preserve the human committer's sign-off. Keep `Co-authored-by` for human co-authors who actually contributed.

## Pull request title

State the net change of the whole pull request in the repository's form, not the last commit or the original plan. Revise the title when the scope changes.

## Pull request description

When the repository has a pull request template, keep its headings and checkboxes and fill them in using the guidance below. Otherwise use these sections and leave out any that would be empty:

1. **Summary**: two to four plain sentences on what changes for users or maintainers, and why.
2. **Changes**: the material changes grouped by behavior or concern, so a reader can follow them without opening the code. Name a file only when that helps a reviewer find something. Never list the changed files as an inventory.
3. **Impact**: who or what is affected, any compatibility or migration needs, the risk and blast radius, and how easy the change is to reverse.
4. **Rationale**: why this approach and which alternatives were rejected. Include it only when the choice is not obvious.
5. **Verification**: the checks actually run on this candidate and their results, and what remains unverified. Do not tick boxes that a human or CI must confirm.
6. **Linked issues**: A closing keyword (`Closes`, `Fixes`, `Resolves`) closes an issue on merge only when the pull request targets the repository's default branch. Write one keyword per issue, and use `owner/repo#N` for issues in other repositories. For a stacked PR or another non-default base, write `Refs #N`; close the issue once the change reaches the default branch or satisfies the repository's release convention. When the PR resolves only part of an issue, write `Part of #N` and leave the issue open. Never invent a link.
7. **Follow-ups**: deferred scope, if any.

Describe the net diff against the base branch. When new commits arrive, rewrite the description to match instead of appending a changelog. [Pull request description examples](references/pr-description.md) show a file inventory next to its rewrite.

## Deliver

Return the requested commit message, PR title, or PR description ready to use, together with any convention or issue link you could not confirm. When the caller expects structured output, put the text in the fields it asks for. Drafting text does not authorize committing, pushing, or publishing.

[Source provenance](references/sources.md) records the prior art and what was left out.
