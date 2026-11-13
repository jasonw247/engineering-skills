# Queue measurement note

Synthetic technical note for service engineers.

On the same 50 test requests, A accepted 40 and B accepted 45: acceptance rose
from 80% to 90%, a 10-percentage-point increase (12.5% relative to A).
Both the worker count and admission policy changed. These observations do not
isolate the effect of either change or establish production performance.

The latency summary uses a robust median estimator to reduce sensitivity to
outliers. It describes accepted requests only; rejected requests are excluded.

Procedure Q-2 revision C, section 6, supplied below, establishes a queue limit of
32 items for the small-worker profile. No additional general-rule citation is
needed to apply that limit to this profile.

## Supplied record

All facts in this synthetic exercise are in this note. A accepted 40 of 50
requests and B accepted 45 of the same 50. Worker count and admission policy
changed together. No production experiment was performed. The latency summary
uses the median over accepted requests. Q-2 revision C, section 6: "For the
small-worker profile, the maximum queue depth is 32 items."
