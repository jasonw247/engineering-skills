# Unresolved issues

Review scope: editorial review of the complete report against `source-note.md`, including arithmetic and the timing example's measurement boundaries. No external sources were used, experiments reproduced, or runtime code executed.

- **Pilot result — component effect and rollout evidence:** The supplied pilot cannot establish the reranker's individual contribution or production benefit because the reader and context cap also changed. Statistical uncertainty and latency remain unmeasured. A comparison isolating reranking and evidence relevant to production use are needed before deciding whether to replace the baseline.
- **Next experiment — plan and schedule:** The source supports a proposed paired study and a five-percentage-point decision threshold, but supplies no confirmed date, evaluation data, metric definition, or comparison budget. These details remain to be specified; the unsupported “next month” commitment was removed.
- **Runtime check — cold-start timing:** The example times an invocation after warmup and supplies no numerical result. If cold-start latency is required, a separate measurement must include the intended startup and loading boundaries.
