# Source provenance

Written locally on 2026-11-10. Repositories were inspected at the revisions below. No text was copied; the ideas were rewritten, and the examples are synthetic.

| Source | Adopted idea | Not adopted |
| --- | --- | --- |
| [microsoft/hve-core](https://github.com/microsoft/hve-core/tree/299c0b68741d9bc08106b132043724c23166e2a4) `git-commit` and `pull-request` skills, `299c0b6` (MIT) | Message rules shared by several write flows; stage only selected paths; PR description that opens with a plain-language summary, groups changes by reviewer concern, and avoids file inventories and commit transcripts; closing references only with evidence; verification lists only checks that actually ran; keep the repository's template. | The generated-by emoji footer, the CI gate and repair-commit procedure, Azure DevOps routing, PowerShell helpers, and its byte limits. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) `engineering/pr`, `4ae2317` (MIT) | "Merge danger" (one-way or two-way door, blast radius) as the basis for the Impact section. | Mandatory diagrams and before/after evidence sections. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/4725261086aa385231fb2accf3764a535b422275) `git-commit`, `4725261` (MIT) | Repository rules first (commitlint, CONTRIBUTING, history); `Token: value` footers; one logical change per commit; no `add -p`, `--no-verify`, or amend; fix a failed hook and commit again; finish an in-progress operation instead of starting a new commit. | The `conventional-commit` skill's commit without confirmation. Its `git commit --no-edit` for in-progress cherry-picks and reverts, which leaves a multi-commit sequence half applied; the operation's `--continue` is used instead, with `GIT_EDITOR=true` so it does not wait for an editor. |
| [openai/skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) `yeet`, `49f948f` (Apache-2.0) | Update an existing pull request instead of opening a duplicate; open drafts; `--body-file`; describe the net diff. | `git add -A`. |
| [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) `finishing-a-development-branch`, `22f0b46` (MIT) | Never assume that the user wants a push or a merge. | Its branch-completion menu. |
| [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | Header form, `!` and the `BREAKING CHANGE:` footer, splitting a change that fits several types. | The specification sets no header length; 72 characters comes from Git practice. |
| [How to Write a Git Commit Message](https://cbea.ms/git-commit/) | Imperative subject, the "If applied, this commit will" test, a body that explains what and why. | The capitalized subject and the 50-character limit, which conflict with lowercase Conventional descriptions; repository convention decides. |
| [Google engineering practices: CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) (CC-BY 3.0) | A first line that stands alone; a body that covers the problem, the approach, and its shortcomings. | Its review-process guidance. |
| [GitHub docs: linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | Closing keywords take effect only when the PR targets the default branch; one keyword per issue. | — |

Local decisions:

- Consistent history counts as a convention, ahead of the Conventional Commits fallback.
- Tool and model attribution is excluded unless the repository requires it. DCO sign-off is kept, because it is the human committer's certification.
- The main file contains no tool or write instructions, so a bounded stage that returns structured text can load it alone. Git and GitHub writes live in a reference that is read only when those tools are available and a write was requested.
- A review of the first draft corrected four points: a partially resolved issue stays open; a stacked change's issue closes only once the change reaches the default branch or meets the release convention; only an `OPEN` pull request is updated; and the squash-merge subject is qualified by repository settings, since under GitHub's default a single-commit PR uses that commit's message ([GitHub docs: configuring commit squashing](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)).
- Splitting a large change is left to `change-sequencing`, and issue work to `github-issues`. Each package states the closing-keyword rule in two sentences instead of depending on the other.

Routing and behavioral trial records are under `evaluations/github-pr` in the source repository; they ran on the hashes recorded there, before the review corrections above.
