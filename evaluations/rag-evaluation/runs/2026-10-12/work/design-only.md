# Design only: parent expansion versus the current RAG baseline

Decision: determine whether parent expansion improves complete, revision-applicable evidence and supported answers for procedures sufficiently to justify its extra reads and operating cost. No runner or reviewed labels are available, so this deliverable is a protocol and interface contract. There are no measured results, estimated production gains, or promotion recommendation.

## Comparison and controls

Start by freezing a corpus snapshot with immutable procedure, revision, section/span, parent/reference, effective-date, and permission identifiers. Preserve text, units, headings, and table relationships. Record parsing/index/model/prompt versions and parent-construction rules. A parent span must belong to the applicable revision and access scope; never expand to a newer revision just because it is the latest.

For the primary component comparison, run the existing baseline retrieval once per query and retain its ordered candidate IDs and scores. Feed that identical pool into (A) existing packing and (B) bounded parent expansion plus packing. Keep the reader, reader prompt, output settings, corpus, initial candidates, final evidence-token cap, and any unrelated ranking logic fixed. Declare expansion order, maximum parent/reference reads, deduplication, truncation, and stop conditions before the confirmation run. Caps are limits, not instructions to fill a prompt. Expansion should stop as soon as the necessary facts and conditions are present; a self-contained exception can suffice alone.

The candidate may inspect additional parent text; that is the intervention being tested and its work must be counted. Record separately the initial candidate set, every read/expanded span, and final delivered evidence. No credit for descendants that are merely represented by a retrieved parent summary. Reapply permissions and revision constraints at every expansion and cache read. Deduplicate aliases without discarding contradictions or meaningful revision differences. Prefer raw parent text; adding generated summaries would introduce a separate representation change requiring its own ablation.

Use a secondary end-to-end comparison under the workload's total cost/latency limits if extra reads materially change operating cost. An optional matched-total-work comparison may give the baseline extra passage reads under the same allowance, but report that as a separate control. Final prompt size alone is not an end-to-end cost comparison.

## Questions, labels, and splits

Assemble reviewed workload cases for direct rules, exceptions, cross-section conditions, revision changes, requested historical revisions, effective dates, near-identical IDs, wrong-version decoys, missing conditions, unavailable procedures, and denied sources. Include narrow and long parent sections and exceptions far from the highest-ranked passage. Separate factual unanswerability from a retrieval/packing failure on an answerable case.

Each query label must contain requested entity/procedure, revision/date, relevant user scope, required claims and conditions, allowed units, answerability, expected answer or abstention rubric, and alternative sufficient immutable span sets. Label all facts required together, including applicability and exceptions. Allow an exception that independently establishes the answer to be sufficient alone. Do not force optional general context or a preferred citation list. Reviewers should inspect full applicable source context and record unresolved interpretation and disagreement.

When a run discovers an unlisted but potentially valid source set, reviewers adjudicate it blind to variant identity, version the label, and rescore both outputs. Do not automatically mark novel valid evidence wrong or silently revise labels to favor a candidate. Calibrate any semantic judge against independently reviewed outputs; keep judge version, rubric, order controls, and disagreement records. Use deterministic checks for revision, permission, IDs, units, and exact fixture-like claims where feasible.

Use development cases for debugging expansion and rubric calibration. Reserve confirmation before tuning. Keep near-duplicate questions and related procedure/entity revisions in the same grouped split when testing unseen-family generalization. If future-revision performance is the deployment target, use a temporal cutoff, prohibit training/tuning on future content, and group dependent families during uncertainty analysis. A separate known-source held-out-question track can answer a different deployment question. State which track is actually used rather than mixing their interpretations.

## Required runner interface and records

A runnable adapter should accept `query`, `corpus_snapshot`, `variant_config`, a fixed `initial_candidates` list, and a total-work budget. It must return raw answer/abstention, claim-to-citation mapping, candidates/ranks, inspected spans, delivered spans with immutable locations and applicability metadata, elapsed timings by stage, token/model/search/read/retry counts, and any errors/timeouts. Retain a row for every assigned query, including failures. Store seed/model parameters and repeats for stochastic readers, worker concurrency, hardware, service boundaries, and cache conditions. Record input and configuration hashes.

Use the same paired query schedule for both variants; randomize or counterbalance execution order if caching/load can matter. Establish an execution deadline and cost ceiling before starting. Record build, parent-map refresh, invalidation, and deletion propagation costs over a stated deployment horizon. Expired or inaccessible evidence must not survive through cached parent expansions.

## Measures and decision rule

Primary quality measures: complete-evidence rate over all assessed answerable queries; required-fact answer correctness/completeness; supported claims and semantic citation support over emitted claims; citation coverage; appropriate unanswerable abstention; and answered fraction. Report candidate availability, inspected evidence, and final delivered sufficiency separately. Empty claim denominators are not applicable. Failures count as unsuccessful completion, remain in assigned-query denominators, and are reported separately from deliberate abstention.

Report paired improvements/regressions and important revision, exception, access, and parent-size slices. Measure end-to-end latency and tail latency at the specified concurrency/cache conditions; count all intermediate reads/tokens and build/refresh costs. Treat permission violations and wrong-revision answers as explicit critical outcomes, not merely one more averaged error.

Before confirmation, the workload owner must set minimum useful quality gain `delta`, allowable regressions per important slice, and operational ceilings for latency, cost, refresh lag, and access enforcement. Use development variability and procedure-family dependence to choose the confirmation sample size; no universal case count or token budget is prescribed. Estimate paired uncertainty by resampling independent procedure/entity families when that matches the sample structure, with model repeats nested within queries rather than treated as independent cases.

Recommend promotion only if the predeclared useful-gain rule is met, important slices remain within their allowed regressions, and measured operating/safety constraints are satisfied. For example, if the agreed rule uses an interval, its lower bound must exceed the agreed useful effect, not merely zero. If no safety violations are observed, claim only that none occurred in the evaluated sample. Inconclusive intervals, unresolved labels, or missing operating measures leave promotion unresolved. A deployment recommendation also needs a staged rollout, scope/latency monitoring, and a rollback trigger tied to the same contracts.

## Missing prerequisites

Obtain the actual baseline adapter/configuration, authorized snapshot and access context, reviewed development and confirmation labels, parent-expansion implementation/configuration, reader and service access, execution budget, and workload-specific decision limits. Without those, no comparison has run and no threshold or sample size is validated. The supplied synthetic trial elsewhere in this work directory does not supply these production prerequisites.
