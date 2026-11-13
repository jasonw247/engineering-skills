# Merge closeout

Reconcile a merged pull request's issues with what actually merged. Propose every write first, and write only what is approved.

## Gather

```sh
gh pr view 57 --json state,mergedAt,baseRefName,headRefName,url,body,commits,closingIssuesReferences
gh repo view --json defaultBranchRef
```

- Stop if `state` is not `MERGED`. A closed but unmerged pull request delivers nothing, so its issues stay as they are.
- Collect the referenced issues from these places:
  - `closingIssuesReferences`;
  - closing keywords, `Refs`, and `Part of` in the pull request body and in commit messages;
  - the source issue named by the branch, when the repository follows that convention.
- For each issue, read its current state, body, parent, and which pull requests closed it: `gh issue view N --json state,stateReason,title,body,parent,subIssuesSummary,closedByPullRequestsReferences`. On older `gh`, use the REST parent endpoint in [gh commands](gh-commands.md).

## Decide

| Situation | Proposed action |
| --- | --- |
| Closed by a keyword on merge | Nothing, except updating the parent if this was its last open child |
| Open; the PR fully delivers it, but no keyword fired (missing keyword or non-default base) | Close as completed, with a comment linking the PR. For a non-default base, propose closing only once the change has reached the default branch, or under the repository's release convention |
| Open; partly delivered | Comment with what landed and what remains. Tick acceptance criteria only with approval |
| Closed by a keyword, but the PR did not deliver it | Comment and propose reopening, with the evidence |
| Parent whose children are all closed | Check its "done when" criteria, then propose closing it |

## Follow-ups

Look for deferred scope in these places:

- the pull request's Follow-ups section;
- review threads that were resolved as "later" or left unresolved;
- TODO or FIXME comments that the diff added;
- acceptance criteria the merged change did not meet.

Search for existing issues before drafting a new one. Write each follow-up in the [issue format](issue-format.md), linking the merged pull request as context. A follow-up of work under a parent becomes a sub-issue of that parent.

## Propose

Present one table, followed by the drafted follow-up issues:

| Issue | Current state | Proposed action | Evidence |
| --- | --- | --- | --- |

## Write, after approval

Run the approved writes in this order:

1. Create follow-up issues, so that closing comments can link to them.
2. Comment on each issue, then close it. The comment comes first so the explanation exists even if closing fails.
3. Link the new sub-issues and dependencies.

Report each issue's final state and the links that were created. Never close, reopen, relabel, or edit issues or comments outside the approved set.
