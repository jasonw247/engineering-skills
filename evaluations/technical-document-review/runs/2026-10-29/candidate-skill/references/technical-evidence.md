# Technical evidence checks

Select checks that affect the requested review. This is not a requirement to audit every source whenever a document contains a number.

## Claims and comparisons

- Attach quantitative claims to their units, denominators, population, dataset, baseline, and relevant conditions. Distinguish relative percentages from percentage points.
- Preserve the distinction between an author's reported measurement and an independent reproduction. A proposed design or illustrative table is not an observed result.
- Verify the cited source and edition for a changed or doubtful claim within the agreed verification depth. A working URL or a matching topic does not establish support.
- Resolve citation placeholders to identifiable sources before relying on them. For version-sensitive claims, identify the relevant source date, software version, and deployed context; a dated survey is not verification of current SDK behavior. If supplied-only review cannot resolve these, report the missing evidence.
- Treat a framework ranking as an editorial recommendation until its criteria, workload, comparison date, and supporting evidence are available. Do not rewrite it as a universal measured result.
- Attribute a gain to the combination tested when data, model, training, or compute changed together. A component-specific claim needs a comparison that isolates that component.
- Preserve uncertainty, associations, limitations, and applicable conditions when shortening a sentence. Do not manufacture a causal explanation from a correlation.

## Examples and procedures

Check prerequisites, order of operations, expected outputs, and relevant failure handling. Inspect variable definitions and measurement boundaries. Successful code execution does not prove that the experiment measures its label: a timer after warmup does not establish cold-start cost.

For resource claims, distinguish active operations, created tasks, queued work, and retained outputs. A semaphore can limit active work while a loop creates a task for every input. Structured task lifetime does not itself establish bounded admission or memory. Review the behavior promised by the example, without imposing a new service architecture.

For proposed experiments, look for a usable baseline, changed component, comparison budget, metric definition, data split, and decision criterion. Missing information is a planning gap; it is not a failed experimental result. Calculate material arithmetic when practical and distinguish calculated values from assumptions.

Identify what a planning utility actually verifies. A passing schema check establishes the checked configuration's structure; a rendered plot establishes that the plotting code handled its supplied data. Neither establishes that the planned retrieval pipeline ran, produced supported answers, or improved a benchmark. Run a minimal isolated example only when useful and authorized, and report its result at that scope.

## Evidence and evaluation

Keep these separate when the document discusses them:

| Target | What it establishes |
| --- | --- |
| Relevance | A source relates to the question. |
| Sufficiency | The provided sources establish the facts and conditions needed for an answer. |
| Citation support | The cited source set supports the attached claim. |
| Answer correctness | The answer satisfies the question and its applicable conditions. |
| Execution validity | The computation actually ran as specified. |
| Analytical validity | The population, joins, units, assumptions, and method make the computed answer meaningful. |

Accept alternative sufficient source sets. A self-contained exception can establish an applicable limit without also citing a general rule. Do not convert an example's optional context into a universal evidence requirement.

A model's confidence or verification verdict is a prediction being evaluated, not ground truth. Empty outputs and abstentions should not acquire a perfect score merely because they contain no unsupported claims.

## Reporting limits

State what was read, what was checked against sources or executed, and what could not be established. Keep checks proportionate. A structurally valid document can still have unsupported claims or an incomprehensible argument.
