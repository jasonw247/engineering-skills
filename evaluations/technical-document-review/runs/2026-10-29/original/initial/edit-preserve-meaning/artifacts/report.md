# Retrieval upgrade proposal

## Pilot result

Reranking improved accuracy by 5%, from 70% to 75%, proving that the reranker improves production answers. Both runs used the same 100 answerable questions. The new system should replace the baseline immediately.

## Next experiment

Parent expansion achieved a five-percentage-point improvement. We will run its evaluation next month.

## Source interpretation

At 70 °C, connector K-42's limit under P-17 revision B is 8 MPa, as stated in §7. That exception supplies the applicable condition and limit directly.

## Runtime check

The following measures cold-start inference latency:

```python
runtime.warmup()
start = clock()
runtime.run(sample)
elapsed = clock() - start
```

## Compatibility note

The serving API remains `/v1/answer` for existing clients.
