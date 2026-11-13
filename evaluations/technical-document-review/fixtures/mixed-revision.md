# Batch integration note

Synthetic revised document. Contract terms use RFC 2119 and RFC 8174 meanings.

## Pilot

On the same 40 requests, configuration A succeeded on 20 and B on 24. This is a
10-percentage-point increase. The configurations used different servers, so the
pilot does not isolate the scheduler's contribution.

## Admission

A semaphore of four bounds both active operations and created tasks to four.

## Response contract

The service MAY include a receipt ID in each successful response.

## Sampling

The summary uses a robust median estimator.
