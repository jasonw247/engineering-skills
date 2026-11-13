# gh commands

Check what the installed `gh` supports with `gh --version` and `gh issue create --help`. Native sub-issue and dependency flags arrived in `gh` 2.94.0. Use the REST fallbacks on older versions.

## Repository and metadata

```sh
gh repo view --json nameWithOwner,defaultBranchRef   # confirm the target before any write
gh label list --limit 200 --json name,description
gh issue list --state all --search "retry budget in:title" --json number,title,state
gh pr list --state merged --limit 50 --json number,title,additions,deletions,changedFiles
gh issue view 40 --json state,issueType,parent,subIssues,subIssuesSummary,blockedBy
```

Issue templates and forms live in `.github/ISSUE_TEMPLATE/`. Pass `--repo owner/name` on every write when working in a fork or from outside the checkout.

## Create and link

Write each body to a file first, then create the issue:

```sh
gh issue create --repo O/R --title "Cap sync retries with a per-client budget" \
  --body-file issue.md --label enhancement
gh issue create --repo O/R --title "..." --body-file child.md --parent 40 --blocked-by 41
gh issue edit 40 --add-sub-issue 42,43
gh issue edit 43 --add-blocked-by 42
```

Recent versions set the issue type with `--type Bug` (present in 2.102.0). If `gh issue create --help` does not list `--type`, use the REST API instead: `gh api repos/O/R/issues -f title=... -F body=@issue.md -f type=Bug`. `-F` reads `@file`; `-f` sends the text literally. Use only types the repository defines.

## REST fallback for relations

The sub-issue and dependency endpoints take the issue's database id, not its number:

```sh
id=$(gh api repos/O/R/issues/43 --jq .id)
gh api -X POST repos/O/R/issues/40/sub_issues -F sub_issue_id="$id"
gh api -X POST repos/O/R/issues/43/dependencies/blocked_by -F issue_id="$(gh api repos/O/R/issues/42 --jq .id)"
gh api repos/O/R/issues/43/parent                  # read a child's parent
gh api repos/O/R/issues/40/sub_issues              # list children
```

- A parent can have up to 100 sub-issues, and nesting can go up to 8 levels deep.
- The parent and the child must belong to the same owner.
- Pace bulk writes to avoid secondary rate limits.

## Comment and close

```sh
gh issue comment 41 --body-file closeout.md
gh issue close 41 --reason completed          # or: --reason "not planned"
```

Post the comment with its own command before closing. Do not rely on `gh issue close --comment`, which can silently drop the comment when the issue is already closed.

## Shell quoting

In zsh, quote array fields such as `-f 'labels[]=bug'`, because `[]` is a glob pattern.
