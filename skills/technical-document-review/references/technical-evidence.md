# Technical evidence checks

Apply the checks below that match the claims in the document under review.

## Numbers, baselines, and causal claims

- Pair each metric with its unit, denominator, dataset slice, and comparison baseline, and verify the arithmetic directly.
- Separate reported measurements from freshly run reproductions and from planned or hypothetical projections.
- Check whether an attributed gain isolates one factor. When model, hardware, concurrency, cache state, or budget changed together, credit the full configuration and note what control would isolate the factor of interest.
- Preserve conditional qualifiers (`may`, `under steady load`) when tightening prose so hedged observations do not turn into unconditional guarantees.
- Treat comparative rankings as opinion unless workload, versions, evaluation date, and reproducible criteria are provided.

## Code examples, benchmarks, and helper scripts

- Trace resource and concurrency claims against the code as written: concurrent in-flight operations, total spawned tasks or threads, queued inputs, and retained outputs have distinct bounds.
- Verify what benchmark timers actually bracket, separating setup, warmup, and teardown from steady-state or cold measurements, and keeping medians (`p50`) separate from tail latencies (`p95`, `p99`).
- Distinguish support tooling (such as config validators, data formatters, or plotting scripts) from end-to-end execution of the system being evaluated.
- For experiment plans, verify that baseline, varied parameter, budget parity, split hygiene, metric denominators, and decision rules are specified; report missing elements as planning gaps rather than negative results.

## Retrieval and evaluation terminology

When a document reports search, RAG, or model evaluation metrics, check that these concepts stay separate:

| Term | Meaning |
| --- | --- |
| Relevance | Retrieved material addresses the topic. |
| Sufficiency | Delivered material contains every fact, unit, and condition needed to answer. |
| Citation support | Cited sources entail the specific claim attached to them; a valid source ID alone does not prove support. |
| Answer correctness | The final output answers the question accurately under all stated conditions. |
| Execution vs semantic validity | A query or script ran without error versus its joins, filters, and population match the question asked. |

Score refusals and empty responses separately from claim precision so refusing every prompt cannot appear as perfect accuracy, and never treat a model's own confidence score or uncalibrated judge output as ground truth.
