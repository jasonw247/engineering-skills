# Routing check, 2026-11-10

One fresh evaluator saw only the name and description of all 23 catalog skills and the 27 requests from the github-pr, github-issues, and change-sequencing suites, with opaque ids, and chose the skills it would load. Expected outcomes were not shown.

| Case | Expected for its suite | Selected | Result |
| --- | --- | --- | --- |
| github-pr/commit-staged-diff | activate | github-pr | pass |
| github-pr/pr-default-branch-closes | activate | github-pr | pass |
| github-pr/stacked-pr-refs | activate | github-pr | pass |
| github-pr/rewrite-file-list | activate | github-pr | pass |
| github-pr/repo-rules-win | activate | github-pr | pass |
| github-pr/history-convention | activate | github-pr | pass |
| github-pr/dco-signoff | activate | github-pr | pass |
| github-pr/toolless-stage | activate | github-pr | pass |
| github-pr/neighbor-review | not activate | code-review | pass |
| github-pr/neighbor-handoff | not activate | handoff | pass |
| github-pr/neighbor-split-pr | not activate | change-sequencing | pass |
| github-issues/split-large-feature | activate | github-issues | pass |
| github-issues/coherent-stays-whole | activate | github-issues | pass |
| github-issues/repo-threshold | activate | github-issues | pass |
| github-issues/old-gh-fallback | activate | github-issues | pass |
| github-issues/closeout-non-default-base | activate | github-issues | pass |
| github-issues/closeout-draft-only | activate | github-issues | pass |
| github-issues/neighbor-implement | not activate | none | pass |
| github-issues/neighbor-split-pr | not activate | change-sequencing | pass |
| github-issues/neighbor-pr-description | not activate | github-pr | pass |
| change-sequencing/billing-plan-migration | activate | change-sequencing | pass |
| change-sequencing/refactor-then-feature | activate | change-sequencing | pass |
| change-sequencing/already-small | activate | none | miss |
| change-sequencing/neighbor-pr-description | not activate | github-pr | pass |
| change-sequencing/neighbor-review | not activate | code-review | pass |
| change-sequencing/neighbor-file-issues | not activate | github-issues | pass |
| change-sequencing/neighbor-closeout | not activate | github-issues | pass |

26 of 27 matched. All new cases and both reverse change-sequencing neighbors matched. The miss is the existing `change-sequencing/already-small` case: the evaluator read that skill's boundary ("Not for ... an edit that is already one self-contained change") as excluding a question about whether to split a small change. That description was not changed here.
