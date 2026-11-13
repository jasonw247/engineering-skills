# Sources and editorial decisions

Reviewed 2026-10-29. These are design influences, not measured evidence that this skill improves model performance. The rules and examples in [SKILL.md](../SKILL.md) and [SKILL-MECHANICS.md](../SKILL-MECHANICS.md) are locally written; no external workflow or scripts were imported. Upstream attribution for the adapted package is retained in [LICENSE](../LICENSE) (`mattpocock/skills` at [`49dd158`](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents)).

## Approaches compared

- **Plain-language guide:** [Google developer documentation style guide: Highlights](https://developers.google.com/style/highlights) and [Voice and tone](https://developers.google.com/style/tone) emphasize a clear actor, direct verbs, and concrete information. Adopted audience-aware phrasing and paragraph-level revision without importing Google-specific product or formatting rules.
- **Pattern-based cleanup:** [Humanizer](https://github.com/blader/humanizer) offers recognizable editing cues and concrete before/after examples. Adopted concrete examples and checking that rewrites preserve technical meaning, while keeping a compact table of recurring structural problems and returning revised text directly rather than multi-draft commentary.
- **Task-oriented skill design:** [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) emphasizes task-specific procedures, progressive disclosure, and verifiable outcomes. Adopted sufficiency checks and conditional reference loading, replacing unverified claims about model negation or adjective intensity with testable decisions.
- **Selection evaluation:** [Agent Skills: Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) separates trigger testing on realistic positive and neighboring requests from output grading. Adopted positive and neighboring cases; no activation rate is inferred from those authored cases.

## Scope note

Combining agent-instruction authoring and prose cleanup in one package avoids maintaining two overlapping writing guides. Revisit splitting them only if catalog routing trials show missed cleanup triggers or collisions with document-review skills.

## Retrieved source fingerprints

Hashes identify bytes retrieved for provenance; dynamic pages may change on refetch. They do not establish behavioral effectiveness.

- [Google developer documentation style guide: Highlights](https://developers.google.com/style/highlights). Retrieved 2026-10-29; SHA-256 `2330282829629dc51ba6577eadebdd208c5c9a284301343fd20e4097b264d97d`.
- [Google developer documentation style guide: Voice and tone](https://developers.google.com/style/tone). Retrieved 2026-10-29; SHA-256 `d4e007dd785d3502fab102e8f9f1153592249cfa51cea0c2e63bad59d11c2524`.
- [Humanizer SKILL.md](https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md). Retrieved 2026-10-29; SHA-256 `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad`.
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices). Retrieved 2026-10-29; SHA-256 `cc46b0e6927349331460ba33a602f816854f9fcb304589aa2499a34d19c3fdbb`.
- [Agent Skills: Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions). Retrieved 2026-10-29; SHA-256 `4e47ac998f432424cbb338351f5b8b7a046a8d2bc853de9f02e0892b8e7dfbfe`.
