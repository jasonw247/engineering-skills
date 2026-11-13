# Retrieval upgrade proposal

## Pilot result

On the same 100 answerable questions, configuration A produced 70 correct answers and configuration B produced 75: an increase of 5 percentage points. A used reader Small and a 2,000-token context cap; B used reader Large, a 4,000-token cap, and a reranker. The pilot does not isolate the reranker's contribution. Uncertainty and latency were not measured, so the pilot alone does not establish a production promotion decision.

## Next experiment

A planned paired study will compare parent expansion with a fixed pipeline. A five-percentage-point gain is a proposed decision threshold. No result is available yet.

## Source interpretation

At 70 °C, connector K-42's limit under P-17 revision B is 8 MPa, as stated in §7. That exception supplies the applicable condition and limit directly.

## Runtime check

The following times one invocation after warmup. It excludes process startup and model loading; it is not a cold-start measurement.

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
