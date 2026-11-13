# Assessment of report.md

The proposal needs substantive corrections before an engineering reader can use it to justify replacing the baseline. The supplied evidence supports a difference between two configurations, a planned experiment, and a post-warmup timing example. Several report statements overstate those facts.

Scope: full editorial and supplied-evidence review of `report.md` against `source-note.md` only. Checks covered factual support, internal consistency, arithmetic, and the timing example's measurement boundary. No external sources were consulted and no experiments or code were executed. Neither input was edited. Line references below refer to the supplied files.

## Prioritized findings

### 1. High — The pilot does not isolate reranking or establish production benefit

**Location:** `report.md:5`, especially “proving that the reranker improves production answers” and “replace the baseline immediately.”

**Evidence and impact:** `source-note.md:5` reports 70 correct answers for configuration A with reader Small and a 2,000-token context cap, versus 75 for configuration B with reader Large, a 4,000-token cap, and a reranker. These changes occurred together, so the result cannot be attributed to the reranker alone. Using the same 100 answerable questions does not resolve that confounding. The pilot did not estimate statistical uncertainty or measure latency, and the note supplies no production evaluation. The asserted proof and immediate-replacement recommendation therefore exceed the evidence and could lead engineers to adopt a change without knowing its individual contribution or operational tradeoffs.

**Proposed correction:** Describe the tested configurations and qualify the recommendation: “On the same 100 answerable questions, configuration A (reader Small, 2,000-token context cap) produced 70 correct answers; configuration B (reader Large, 4,000-token cap, and reranker) produced 75. This comparison does not isolate the reranker's contribution. Statistical uncertainty and latency were not evaluated. The pilot alone does not establish that the baseline should be replaced immediately.”

**Remaining uncertainty:** The reranker's individual effect, uncertainty around the observed difference, and production performance remain unestablished. Further evaluation is a recommendation, not a completed result.

### 2. High — A future decision threshold is presented as an achieved result

**Location:** `report.md:9`, “Parent expansion achieved a five-percentage-point improvement.”

**Evidence and impact:** `source-note.md:7` says no study has run. Five percentage points is a proposed decision threshold for a future paired comparison against a fixed pipeline. The report converts that threshold into a measurement and contradicts its own statement that evaluation is still upcoming. Readers could mistake a planned criterion for evidence supporting parent expansion.

**Proposed correction:** “A future paired study proposes testing parent expansion against a fixed pipeline. A five-percentage-point gain is the proposed decision threshold; no study has run.” The source note does not establish the “next month” schedule; omit it or identify it as a separate planning assumption requiring confirmation.

**Remaining uncertainty:** No measured effect of parent expansion is available, and the evaluation date is not established by the supplied evidence.

### 3. Medium — The pilot gain confuses percentages with percentage points

**Location:** `report.md:5`, “improved accuracy by 5%, from 70% to 75%.”

**Evidence and impact:** The supplied counts are 70/100 and 75/100 (`source-note.md:5`). Their difference is **5 percentage points**, or approximately **7.1% relative to the 70% baseline**: `(75 − 70) / 70 × 100`. Calling this a 5% improvement leaves the magnitude misstated or ambiguous.

**Proposed correction:** Use “Configuration B's accuracy was 75%, compared with 70% for configuration A, a difference of five percentage points.” Keep this wording descriptive, consistent with finding 1's attribution limits.

**Remaining uncertainty:** This arithmetic describes the observed sample difference; it does not establish statistical significance or a production gain.

### 4. Medium — The timing example does not measure cold-start latency

**Location:** `report.md:17–24`, especially the “cold-start inference latency” label and `runtime.warmup()` before the timer.

**Evidence and impact:** The timer starts after warmup and surrounds one `runtime.run(sample)` invocation. As confirmed by `source-note.md:11`, it records a post-warmup invocation and excludes process startup and model loading. The current label could cause engineers to treat this timing as evidence about startup behavior.

**Proposed correction:** Change the introduction to “The following times one post-warmup invocation of `runtime.run(sample)`; it excludes process startup and model loading.” The snippet can remain as an illustration under that description. If cold-start timing is intended, a separate procedure must define and include the relevant startup operations; those operations are not supplied here.

**Remaining uncertainty:** No numerical timing result is available. The example establishes a measurement boundary, not a measured latency or a latency distribution.

## Supported passages

- **Pressure limit (`report.md:13`):** Supported by `source-note.md:9`. At 70 °C, the “above 60 °C” condition applies, so connector K-42's maximum operating pressure under P-17 revision B, §7 is 8 MPa. That passage supplies the connector, revision, condition, and limit; no additional general-rule passage is needed.
- **Compatibility (`report.md:28`):** Supported directly by `source-note.md:13`: existing clients retain `/v1/answer`. This is a fixture requirement and needs no external product verification within this review.

## Clarity and organization

The section headings make the short proposal easy to scan. The material clarity problems are the missing configuration details in the pilot, the conflation of plans with results, and the timing label. Correct those in place and make the pilot's evidence limits visible before the deployment recommendation. No broader restructuring is necessary to address the demonstrated issues.
