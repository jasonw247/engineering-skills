# Source provenance

Written locally on 2026-11-10. Repositories were inspected at the revisions below. No text was copied; the ideas were rewritten, and the examples are synthetic.

| Source | Adopted idea | Not adopted |
| --- | --- | --- |
| [microsoft/hve-core](https://github.com/microsoft/hve-core/tree/299c0b68741d9bc08106b132043724c23166e2a4) `backlog-management` references, `github-backlog-executor` agent, and `issue-triage` agent, `299c0b6` (MIT) | Required acceptance criteria; a children section only on parents; link a sub-issue only after both issues exist; comment before closing; use only labels and types that exist; treat issue text as untrusted. | The grooming outcome taxonomy, sprint planning, the label-replacement machinery, and Azure DevOps routing. |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) `engineering/to-tickets` and `setup-matt-pocock-skills/issue-tracker-github.md`, `4ae2317` (MIT) | Tickets that can each be verified on their own, with acceptance criteria and blockers; create blockers first; approve the breakdown before publishing; confirm the target repository in forks; the `gh issue close --comment` pitfall. | The "fits one context window" sizing rule, and keeping all file paths out of issues (here they are allowed as starting points). |
| [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/4725261086aa385231fb2accf3764a535b422275) `github-issues`, `4725261` (MIT) | Use issue types instead of title prefixes; set types through the REST API when `gh` lacks a flag; zsh quoting of `labels[]`. | — |
| [GitHub docs: sub-issues REST API](https://docs.github.com/en/rest/issues/sub-issues) and [linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | Database ids for relation endpoints; the 100-child and 8-level limits; closing keywords only for the default branch. | — |
| `gh` CLI release notes and `gh issue create/edit --help` for 2.102.0 | Native `--parent`, `--add-sub-issue`, `--blocked-by`, and `--type` flags. The release notes date sub-issue support to 2.94.0; local help output was checked on 2.102.0. | — |
| SmartBear, [Best Practices for Peer Code Review](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/), summarizing the Cisco study | 200–400 lines inspected well per session, recorded as a heuristic. | Its inspection-rate and defect-density figures as hard limits. The original paper was not consulted directly. |
| [Google engineering practices, "Small CLs"](https://google.github.io/eng-practices/review/developer/small-cls.html) (CC-BY 3.0) | Rough size guidance, and the point that spread across files matters. | Splitting methods, which `change-sequencing` covers. |

Local decisions:

- About 500 changed lines is a trigger to consider a split, not a limit. Coherence decides, and a repository's own threshold replaces the figure.
- How to split is delegated to `change-sequencing`, a declared dependency. This package maps that skill's sequence onto parent issues, sub-issues, and dependencies.
- Merge closeout lives here because it mainly writes issue state. The two-sentence closing-keyword rule is repeated in `github-pr` instead of making either package depend on the other.

Routing and behavioral trial records are under `evaluations/github-issues` in the source repository.
