# Source provenance

Written locally on 2026-11-10. The ideas come from two sources:

- Google Engineering Practices, ["Small CLs"](https://google.github.io/eng-practices/review/developer/small-cls.html) (CC-BY 3.0).
- `stacks/ronny/skills/engineering-small-prs` in [MiniMax-AI/mcode-stack](https://github.com/MiniMax-AI/mcode-stack/tree/d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0) at `d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0`, inspected 2026-11-10. Its `NOTICE.md` says the material adapted from Google stays under CC-BY 3.0 and the author's additions are MIT.

This package was written from the underlying ideas, which are common engineering practice: split refactors from behavior changes, slice vertically, land an interface with its first use, and expand and contract migrations. It does not copy or closely paraphrase either text, so it carries no CC-BY attribution requirement; the sources are recorded here for provenance. If text from either source is later imported, add the CC-BY attribution and, for the mcode-stack additions, the MIT notice.

Not adopted: the source's output template, PR-description and review guidance (covered by other packages or repository conventions), and its "prefer smaller than you think necessary" heuristic, replaced here by weighing the costs of splitting. No behavioral trial has been run on this package.
