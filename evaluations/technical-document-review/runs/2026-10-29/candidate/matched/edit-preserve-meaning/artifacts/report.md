# Retrieval upgrade proposal

## Pilot result

In an internal pilot using the same 100 answerable questions, configuration A answered 70 correctly (70% accuracy) with reader Small and a 2,000-token context cap. Configuration B answered 75 correctly (75% accuracy) with reader Large, a 4,000-token cap, and a reranker.

Configuration B's accuracy was five percentage points higher. Because the reader, context cap, and reranker changed together, the pilot does not isolate the reranker's effect. Statistical uncertainty and latency were not measured. These results do not establish an improvement in production answers or justify immediately replacing the baseline.

## Next experiment

A future paired study proposes testing parent expansion against a fixed pipeline. No study has run. A five-percentage-point gain is the proposed decision threshold, not a measured result.

## Source interpretation

Procedure P-17 revision B, §7, sets a maximum operating pressure of 8 MPa for connector K-42 above 60 °C. The limit therefore applies at 70 °C. This passage identifies the connector, revision, temperature condition, and pressure limit, so it establishes the applicable limit without another passage.

## Runtime check

The following times one invocation after warmup. Process startup, model loading, and warmup occur outside the timed interval, so it does not measure cold-start latency. No numerical timing result is supplied.

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
