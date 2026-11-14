# Source notes

This is locally authored guidance informed by the following pinned sources, inspected on 2026-10-15. No upstream scripts, profiles, hooks, or agent definitions are bundled. These are design influences, not evidence of improved model performance.

| Source | Adopted idea | Bounds |
| --- | --- | --- |
| [Code Polish, Fixed Scope and Simplify](https://github.com/PaulRBerg/agent-skills/blob/c7685ecb63f89453955e72fc5d98a5caedb6cb7b/skills/code-polish/SKILL.md) | Scoped, behavior-preserving cleanup with a valid no-op outcome. | Use task-owned hunks; omit the fallback to all dirty files, review-and-fix mode, automatic profiles, report template, and assumed risk acceptance. |
| [Anthropic Code Simplifier](https://github.com/anthropics/claude-plugins-official/blob/8f814f49002ff824e8a9ba43cf96112dc7f5948d/plugins/code-simplifier/agents/code-simplifier.md) | Favor readability and local conventions over code golf. | Omit model assignment, proactive always-on use, and fixed JavaScript/React conventions. |
| [Sentry Code Simplifier](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/skills/code-simplifier/SKILL.md) | Recent-change scope and preserving useful abstractions. | This derives from Anthropic's guidance; it is not independent effectiveness evidence. |
| [Ponytail, The smallest complete change](https://github.com/DietrichGebert/ponytail/blob/84740e3d344b69b4a133201fa519eb37a62a2b2a/skills/ponytail/SKILL.md) | Reuse established facilities and finish all required propagation. | Optimize maintenance cost, not LOC; omit sticky modes, personas, hooks, and categorical dependency rules. |

Local additions separate actor cleanup from independent review, preserve concurrent edits, restrict staged use to implementation, and allow uncertain optional cleanup to be skipped without blocking the underlying task. The objective distinction and helper-reuse, test-duplication, repair-accretion, and boundary-inspection guidance are local additions, not evidence of effectiveness. Behavioral evaluation is recorded separately under `evaluations/diff-simplification` in the source repository.
