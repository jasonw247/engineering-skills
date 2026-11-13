# Phrasing and organization examples

Consult this reference when abstract noun stacks, ambiguous pronouns, or stock filler obscure technical meaning.

## Unpack meaning without inventing facts

Name who performs what action, under what condition, and with what result. When a sentence admits two incompatible technical readings and surrounding context does not settle which one applies, flag the ambiguity in the review note rather than guessing.

| Original passage | Revision (when context supports it) |
| --- | --- |
| "Maintain scoped evidence lineage." | "Record the source ID, version, and passage offset for each claim." (Use only if those three fields match the spec.) |
| "A computed narrative needs its population definition." | "State which records the calculation includes alongside the computed number." |
| "Only compatible reuse contributes; frequent edits shorten that horizon." | "Cached results apply only while the source version matches; frequent source edits invalidate the cache sooner." |
| "Costs may fall if volume increases." | "Costs may fall at higher volume." (Keep `may` when the source gives no guarantee.) |
| "The hierarchy enables cross-document intelligence." | Replace with the concrete mechanism described in the text (for example, "routes queries across related documents") without inventing unstated benefits. |

## Preserve precision when cutting clutter

- Retain domain terms that carry exact technical meaning in context (*idempotent*, *hermetic*, *linearizable*, *unbiased*). Cut empty throat-clearing (*"It is worth noting that"*, *"not merely X, but Y"*).
- Keep passive voice when the actor is unknown or irrelevant to the invariant (*"Audit records are retained for 30 days"*).
- Use bullet lists for independent obligations, and connected sentences when explaining cause-and-effect chains.

## Fit structure to the document's job

Keep the document's existing outline when it serves the reader. When restructuring is needed, follow how readers use that document type:

- **Design or RFC:** problem and constraints, proposed design, failure modes and alternatives, rollout and verification.
- **Runbook or procedure:** prerequisites, ordered steps with expected outputs, rollback and recovery.
- **Benchmark or study:** question and setup, controls and workload, measured results with denominators, limits and conclusion.
- **Reference:** lookup tables and exact interface contracts grouped by operation.
