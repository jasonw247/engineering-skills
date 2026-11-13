# Metrics and reporting

Declare the scored unit, eligible population, numerator, denominator, and missing-label rule before computing percentages. Always report `numerator / denominator` alongside rates. Mark `0 / 0` denominators (such as claim-support rate on an abstained response) as `not applicable` rather than `100%`.

| Metric | Definition |
| --- | --- |
| **Retrieval recall @ k** | Judged relevant documents or spans surfaced within cutoff `k` over answerable queries. |
| **ANN neighbor recall @ k** | Overlap with exact brute-force top-`k` over the *same* vectors, metric, filter, and corpus; measures index approximation, not passage relevance. |
| **Complete-evidence rate** | Answerable queries whose delivered context establishes every required fact and condition (accepting any valid source set, including standalone exceptions) divided by answerable queries. |
| **Answer completeness** | Required rubric facts stated accurately divided by total required rubric facts. |
| **Answer correctness** | Queries answered accurately for the target entity, revision, unit, and condition divided by answerable queries. |
| **Supported-claim rate** | Factual claims in the answer entailed by delivered passages (or verified calculations) divided by total factual claims emitted. |
| **Citation support** | Cited claims entailed by their attached citation set (under matching scope/revision) divided by total cited claims. |
| **Citation coverage** | Factual claims carrying citations divided by claims requiring attribution. Citation presence alone never proves support. |
| **Abstention accuracy & answered rate** | Correct refusals over unanswerable/insufficient-evidence queries, paired with the answered fraction on answerable queries so blanket refusal cannot mask errors. |

## Accounting rules

- **Scope-aware support:** Verify entity, effective date/revision, unit, and exception clauses when judging sufficiency and citation support; multiple aliases or copies of the same document count as one source rather than independent corroboration.
- **Calculations:** Verify population completeness, deduplication, join keys, and units independently; top-k text chunks never establish an exact corpus count.
- **Failures and timeouts:** Keep every errored or timed-out query in the denominator under a declared outcome bucket (such as failed completion); never silently filter failures out of aggregate tables.
- **Cost and latency:** Report p50/p95 latency, concurrency, cache warmth, and full work per query (retrieval hops, reranked passages, input/output tokens, retries), plus corpus build/refresh overhead when comparing architectures. Never report synthetic or mocked sleeps as measured latency.
