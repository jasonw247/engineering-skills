# Retrieval upgrade proposal

## Pilot result

In an internal pilot using 100 answerable questions, Configuration A answered 70 correctly (70% accuracy), while Configuration B answered 75 correctly (75% accuracy), a five-percentage-point increase. Configuration A used reader Small and a 2,000-token context cap. Configuration B used reader Large, a 4,000-token context cap, and a reranker.

Because several components changed together, the pilot does not isolate the reranker's contribution. It did not estimate statistical uncertainty or measure latency. The result alone does not establish an improvement in production answers or justify immediately replacing the baseline.

## Next experiment

A future paired study proposes testing parent expansion against a fixed pipeline. No study has run. A five-percentage-point gain is the proposed decision threshold, not a measured result. The source note does not specify an evaluation date.

## Source interpretation

Procedure P-17 revision B, §7 sets a maximum operating pressure of 8 MPa for connector K-42 above 60 °C. Since 70 °C meets that condition, the maximum operating pressure at 70 °C is 8 MPa. The passage identifies the connector, revision, condition, and limit, so no additional passage is needed to establish this limit.

## Runtime check

The following times an invocation after warmup. It does not measure process startup or model loading:

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

No numerical timing result is supplied.

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
