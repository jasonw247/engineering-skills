# Commit message examples

Each pair shows the same change described badly and well. Each "Better" message uses Conventional Commits (the fallback convention) unless the example says the repository has another convention.

## Subject that says nothing

Weak:

```
Update files
```

Better:

```
fix(sync): stop retrying requests after the retry budget is spent
```

The subject names the behavior that changed. "Update", "Fix bug", "WIP", and "Address review comments" tell a later reader nothing.

## Body that narrates the session

Weak:

```
feat(sync): add retry budget

I first tried a per-request counter but that didn't work, so I moved
it to the client. Changed client.py, config.py, and test_client.py.
Also fixed a typo.
```

Better:

```
feat(sync): cap retries with a per-client budget

Retries were unbounded per request, so an outage made every caller
retry at once and slowed recovery. Each client now shares a budget
of retries that refills over time; once it is spent, requests fail
fast with RetryBudgetExceeded.

The budget defaults to 10 retries per minute and is configurable
with sync.retry_budget.

Refs: #41
```

The body gives the problem, the approach, and what a caller sees. It leaves out the files, the dead ends, and the unrelated typo fix; the typo fix belongs in its own commit.

## Breaking change

```
feat(api)!: return 404 instead of empty 200 for unknown projects

Clients that treated an empty body as "not found" must now handle
404.

BREAKING CHANGE: GET /projects/{id} returns 404 for unknown ids.
```

## Repository with its own convention

Recent history in this repository reads:

```
Add retry budget to the sync client
Document cache invalidation for plugin authors
Remove the legacy v1 export path
```

That history is a convention, so follow it rather than imposing Conventional Commits:

```
Stop retrying sync requests after the budget is spent
```

## Squash merge

When pull requests are squash-merged, the PR title usually becomes the commit subject and GitHub appends the PR number. That depends on the repository's squash setting: under GitHub's default, a PR with a single commit uses that commit's title and message instead. Write the PR title as the subject you want in history, and keep a single commit's subject consistent with it. The squashed body should summarize the PR, not concatenate its commit messages:

```
feat(sync): cap retries with a per-client budget (#57)

Retries are now limited per client and fail fast once the budget is
spent, so outages no longer cause retry storms.

Closes #41
```

## Sign-off without attribution

A repository that requires DCO sign-off:

```
docs: explain cache invalidation for plugin authors

Signed-off-by: Ana Ruiz <ana@example.com>
```

Do not add tool attribution next to the sign-off:

```
Co-Authored-By: Some Model <noreply@example.com>
```

`Signed-off-by` certifies the human committer's right to submit the change. A tool or model is not a co-author.
