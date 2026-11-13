# Retrieval upgrade proposal

## Pilot result

On the same 100 answerable questions, configuration A produced 70 correct answers and configuration B produced 75: an increase from 70% to 75%, or 5 percentage points. A used reader Small and a 2,000-token context cap. B used reader Large, a 4,000-token cap, and a reranker. Because these components changed together, the pilot does not isolate the reranker's contribution. Statistical uncertainty and latency were not measured. This pilot alone does not establish whether B should replace A in production.

## Next experiment

A planned paired study will compare parent expansion against a fixed pipeline. A five-percentage-point gain is a proposed decision threshold, not a measured outcome. The study has not run.

## Source interpretation

At 70 °C, connector K-42's limit under P-17 revision B is 8 MPa, as stated in §7. That exception supplies the applicable condition and limit directly.

## Runtime check

The following times one invocation after warmup. It excludes process startup and model loading; it does not measure cold-start latency.

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
