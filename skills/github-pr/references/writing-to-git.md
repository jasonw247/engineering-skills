# Writing to Git and GitHub

Read this only when you have Git or GitHub tools and were asked to commit, push, or open or update a pull request. Each write needs a request: being asked to commit does not authorize a push, and being asked to push does not authorize opening a pull request.

## Before writing

- Inspect the state: `git status`, `git diff --staged`, `git diff`, and the current branch.
- Confirm the repository and its default branch with `gh repo view --json nameWithOwner,defaultBranchRef`. In a fork, `gh` may default to the upstream repository, so pass `--repo` when it matters.
- If a merge, cherry-pick, or revert is in progress, finish it with that operation's own command rather than writing a new commit: `GIT_EDITOR=true git merge --continue`, `GIT_EDITOR=true git cherry-pick --continue`, or `GIT_EDITOR=true git revert --continue`. A plain `git commit` in the middle of a multi-commit cherry-pick or revert leaves the remaining commits unapplied. Each `--continue` opens an editor for the prepared message. `GIT_EDITOR=true` accepts that message without one and, unlike `-c core.editor=true`, still applies when the environment already sets `GIT_EDITOR`.

## Commit

- Stage files by explicit path, for example `git add -- path/one path/two`. Do not use `git add -A` or `git add .` unless asked. Do not use `git add -p`, because it waits for interactive input.
- Before committing, check the staged file names for secrets, credentials, and large generated files.
- Do not unstage or restage work that the user staged earlier unless asked.
- Write the message to a temporary file and commit with `git commit -F <file>`. Add `-s` when the repository requires sign-off.
- Never use `--no-verify`. If a hook fails, fix the cause, restage, and create the commit again.
- Do not amend, rebase, or force-push unless asked.
- Afterwards, read the result with `git log -1 --format=%B`. If something added a trailer that the repository's rules exclude, report it. Do not amend without agreement.

## Push

- Push only when asked: `git push -u origin HEAD`.
- Never force-push to a shared branch. If the push is rejected, report the divergence instead of overwriting it.

## Pull request

- Check whether the branch already has a pull request: `gh pr view --json number,url,state,baseRefName`. Update it only when `state` is `OPEN`. A reused branch name can return a merged or closed PR; in that case open a new one rather than editing the old one.
- Write the body to a temporary file and pass it with `--body-file`, which avoids shell escaping problems.
- Create: `gh pr create --draft --base <base> --title "<title>" --body-file <file>`. Open it as a draft unless asked otherwise.
- Update: `gh pr edit <number> --title "<title>" --body-file <file>`, describing the net diff against the base.
- After writing, confirm the linked issues GitHub recognized: `gh pr view <number> --json closingIssuesReferences`. The list stays empty when the base is not the default branch.

## Report

Report the commit hashes, the pushed branch, and the pull request URL. List any write that was skipped because it was not requested.
