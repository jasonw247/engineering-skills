# Executed synthetic fixture evaluation

The candidate completes all three supplied tasks correctly; the baseline completes one. This is measured deterministic fixture behavior under the supplied rubric, not evidence of production accuracy or readiness. Both variants return the same candidate lists on all three cases. The observed gains come from selecting the applicable exception for the hot case and abstaining on the missing entity; they do not establish a retrieval improvement or isolate one component's effect.

Run `python3 evaluate.py` from this directory. The standard-library runner executed the supplied implementation six times, once per variant per query, with no failures. `protocol.md` was written before execution; `results.json` retains raw outputs, scored outcomes, paired comparisons, environment details, timings, and SHA-256 hashes of the code and inputs. All three input files remained unchanged. No network or model calls occurred.

## Per-query evidence and answer outcomes

For both variants, the `hot` and `ordinary` candidate lists are `[general, exception, exception-copy]`; the `missing` candidate list is empty. Candidate availability is distinct from evidence delivered to the answer stage.

| Query | Variant | Delivered evidence / citations | Answer | Delivered sufficiency | Answer/citation outcome |
| --- | --- | --- | --- | --- | --- |
| hot: K-42, B, 70 C | baseline | general / general | 10 MPa | Insufficient: applicable temperature restriction omitted | Incorrect pressure; cited source does not establish the applicable limit |
| hot: K-42, B, 70 C | candidate | exception-copy / exception-copy | 8 MPa | Sufficient | Correct and supported; the alternative exception source alone is sufficient |
| ordinary: K-42, B, 20 C | baseline | general / general | 10 MPa | Sufficient under supplied label | Correct and supported |
| ordinary: K-42, B, 20 C | candidate | general / general | 10 MPa | Sufficient under supplied label | Correct and supported |
| missing: K-99, B, 20 C | baseline | general / general | 10 MPa | Not applicable as answerable evidence; record has wrong entity | Unsupported answer; no abstention; evidence was outside its empty candidate list |
| missing: K-99, B, 20 C | candidate | none / none | Abstains | Not applicable | Appropriate abstention; claim and citation support are not applicable, rather than perfect |

The fixture labels explicitly permit either `exception` or `exception-copy` on its own for the hot question. Requiring both, or requiring `general` as well, would incorrectly reject sufficient evidence. The copies do not count as independent corroboration. All emitted citation IDs exist, including the baseline's two unsupported answers; existence therefore does not establish semantic citation support.

## Calculated aggregates from the six executed outputs

| Measure | Baseline | Candidate |
| --- | --- | --- |
| Candidate complete evidence, answerable cases | 2/2 (100%) | 2/2 (100%) |
| Delivered complete evidence, answerable cases | 1/2 (50%) | 2/2 (100%) |
| Answerable correctness / one-fact completeness | 1/2 (50%) | 2/2 (100%) |
| Overall task correctness, including abstention | 1/3 (33.3%) | 3/3 (100%) |
| Supported emitted pressure claims | 1/3 (33.3%) | 2/2 (100%) |
| Semantically supported cited pressure claims | 1/3 (33.3%) | 2/2 (100%) |
| Citation coverage | 3/3 (100%) | 2/2 (100%) |
| Appropriate unanswerable abstention | 0/1 (0%) | 1/1 (100%) |
| Answered fraction | 3/3 (100%) | 2/3 (66.7%) |
| Delivered source scope violations | 1/3 | 0/2 |
| Delivered sources outside returned candidates | 1/3 | 0/2 |
| Execution failures | 0/3 | 0/3 |

Paired task outcomes: two improvements (`hot`, `missing`), one tie (`ordinary`), no regressions among these three cases. Overall task correctness rises by 2/3, or 66.7 percentage points. Support rates use emitted claims as their denominator and therefore change denominator when the candidate appropriately abstains; the abstention and answerable-quality measures keep that distinction visible.

## Supported decisions and limits

The supplied baseline demonstrably drops necessary temperature evidence after retrieving it and generates an out-of-scope answer for K-99. The candidate resolves these particular failures while preserving the ordinary answer. The runner can serve as a local regression check for those behaviors. It cannot justify a production release, a general winner, a model or index choice, or an isolated reranking/expansion claim: evidence selection and missing-entity behavior change together, and the candidate hard-codes an exception ID and a temperature threshold.

There are no independent reviewed production labels, held-out confirmation families, stochastic model draws, or representative operational workloads. The three cases cover only one known revision and entity plus one missing entity; they do not establish robustness to other revisions, permission boundaries, aliases, threshold boundaries, source changes, or contradictory records. No inferential interval is justified by treating these related toy cases as an independent deployment sample. New evidence or changed labels need adjudication before reuse of this closed fixture scorer.

Measured work consists of six local function calls and recorded diagnostic durations for input copying plus each call, with sequential execution and no warmup. These durations are not service latency measurements. Both variants deliver at most one source, but no token budget, production latency distribution, build/refresh cost, storage cost, model cost, or throughput has been measured. A production decision needs reviewed representative cases, declared useful-gain/regression and operating limits, and confirmation under the relevant workload and dependency structure.
