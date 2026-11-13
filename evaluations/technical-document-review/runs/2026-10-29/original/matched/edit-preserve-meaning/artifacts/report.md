# Retrieval upgrade proposal

## Pilot result

In an internal pilot using 100 answerable questions, configuration A answered 70 correctly (70%) with reader Small and a 2,000-token context cap. Configuration B answered 75 correctly (75%) with reader Large, a 4,000-token context cap, and a reranker: a five-percentage-point increase over A.

The pilot compared configurations that differed in reader, context cap, and reranking, so it did not isolate the reranker's effect. It did not estimate statistical uncertainty or measure latency. These results do not establish an improvement in production answers or justify immediately replacing the baseline. Further evaluation is needed before a rollout decision.

## Next experiment

A future paired study proposes testing parent expansion against a fixed pipeline. A five-percentage-point gain is the proposed decision threshold, not a measured result. The study has not run.

## Source interpretation

Procedure P-17 revision B, §7 sets a maximum operating pressure of 8 MPa for connector K-42 above 60 °C. At 70 °C, that condition applies, so the maximum operating pressure is 8 MPa. The passage identifies the connector, revision, condition, and limit; it is sufficient to establish this limit without another passage.

## Runtime check

The following times a post-warmup invocation. It does not measure process startup or model loading, and no numerical timing result is supplied.

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
