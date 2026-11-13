# Unresolved issues

These issues remain after editing report.md against source-note.md. Verification was limited to the supplied materials; no experiment or timing example was executed.

- **Pilot result:** The reranker's individual effect, statistical uncertainty, latency, and performance on production questions remain unknown. The supplied results cannot resolve these questions; additional evaluation is needed before a production replacement decision.
- **Next experiment — design:** The proposed paired study has not run. The source specifies a fixed pipeline and a five-percentage-point decision threshold but does not define the pipeline, evaluation metric, question set or data split, sample size, comparison budget, or uncertainty analysis. These details are needed to make the study plan executable and interpretable.
- **Next experiment — schedule:** The source does not confirm the report's claim that the evaluation will run next month. That commitment was removed; the schedule remains unconfirmed.
- **Runtime check:** No numerical latency result is available. The supplied example measures a post-warmup invocation; a separate measurement that includes startup and model loading would be needed to establish cold-start latency.
