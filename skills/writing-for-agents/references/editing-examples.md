# Editing examples

Use these as demonstrations of decisions, not replacement templates. The examples are synthetic.

## State the point directly

Before: “This isn't about adding more documentation. It's about fostering a robust ecosystem of shared understanding.”

After: “Document the retry rules so callers know when a failed request can be repeated.”

This revision assumes the surrounding source establishes that purpose. Without that context, use a narrower revision such as “The documentation should build shared understanding”; do not invent retry behavior to make the sentence concrete.

## Unpack technical prose

Before: “The orchestration layer leverages durable receipt persistence to facilitate post-timeout reconciliation of externally materialized side effects.”

After: “The coordinator saves a receipt so it can check whether the external write succeeded after a timeout.”

Retain the domain's name for the coordinator if that name matters. For an expert audience, “durable receipt” may be useful terminology; explain what it records rather than replacing every technical term.

## Repair structure before shortening

Before: “The worker hands the batch to the coordinator after it records the receipt, which retries it if needed.”

The sentence leaves the owner of the receipt and the object of the retry unclear. If the source establishes both, write: “The worker records the receipt, then sends the batch to the coordinator. The coordinator retries the batch if needed.” Otherwise, flag the missing relationship. A fluent guess would change the specification.

## Keep the caveat that affects the decision

Before: “It is important to note that, while this may potentially be useful in some cases, the benchmark is synthetic and therefore may not necessarily reflect real production behavior.”

After: “The benchmark uses synthetic data; production performance remains unmeasured.”

Before: “Do not retry payments after a timeout until the provider confirms whether the charge succeeded.”

After: Keep it. The prohibition and condition prevent a duplicate charge. Removing defensive phrasing does not mean removing operating constraints.

## Preserve a useful distinction

Before: “The timeout stops waiting for a response; it does not cancel the remote write.”

After: Keep it. This contrast explains behavior that affects recovery. A blanket ban on negative phrasing would make the guidance less precise.

## Remove ceremony without weakening evidence

Before: “In conclusion, these results clearly demonstrate a groundbreaking improvement: median latency fell from 90 ms to 70 ms across 20 synthetic requests.”

After: “Median latency fell from 90 ms to 70 ms across 20 synthetic requests.”

Keep the sample size, units, and synthetic setting. Do not generalize the result to production or add an explanation the evidence does not establish.
