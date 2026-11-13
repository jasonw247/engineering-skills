# T1 — Transport pilot record

Synthetic primary record; revision 1, 2026-09-15; identifier T1.

## 2. Pilot

On a fixed synthetic workload, median latency fell from 100 ms to 80 ms after
both connection pooling and the server CPU allocation changed. No component
ablation was conducted. The pilot cannot isolate either change's contribution.

## 3. Delivery

The tested protocol permits duplicate delivery following a process restart.
It makes no exactly-once guarantee. Delivery correctness was not benchmarked.
