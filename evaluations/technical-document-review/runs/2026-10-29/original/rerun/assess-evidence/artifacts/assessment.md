# Assessment of `report.md`

The report needs substantive correction before an engineering reader can rely on its conclusions. Its pilot results support a comparison of two configurations, but do not establish a reranker effect or justify immediate production replacement. It also presents a proposed experiment threshold as a result and labels a post-warmup measurement as cold-start latency.

Scope: editorial and supplied-evidence review of the complete `report.md`, using only `source-note.md` as factual evidence. Checks covered claim support, internal consistency, arithmetic, measurement boundaries, and clarity. No external source audit, experiment reproduction, or runtime execution was performed. Locations below refer to the original input line numbers. Neither input was edited.

## Prioritized findings

### 1. High — Pilot attribution and production recommendation exceed the evidence

**Location:** `report.md:5`, “Reranking … proving that the reranker improves production answers” and “replace the baseline immediately.”

**Evidence and impact:** `source-note.md:5` reports 70 correct answers for configuration A (reader Small, 2,000-token context cap) and 75 for configuration B (reader Large, 4,000-token cap, and a reranker), on 100 answerable questions. Multiple components changed, so the comparison cannot isolate reranking. The pilot estimated no statistical uncertainty and measured no latency. Describing it as proof of improved production answers hides these limits and gives the replacement recommendation more support than the evidence supplies.

**Proposed correction:** Report both configurations and attribute the observed difference to the configuration comparison. For example: “On the same 100 answerable questions, configuration A answered 70 correctly and configuration B answered 75 correctly. A used reader Small with a 2,000-token context cap; B used reader Large with a 4,000-token cap and a reranker. The pilot did not isolate individual component effects, estimate statistical uncertainty, or measure latency.” Replace the immediate-replacement recommendation with a recommendation for further evaluation before a production decision.

**Remaining uncertainty:** The supplied evidence cannot establish which change produced the difference, the uncertainty of that difference, or expected production performance. A component-isolating comparison would be needed to support a reranker-specific claim.

### 2. High — A future decision threshold is reported as an achieved result

**Location:** `report.md:9`, both sentences.

**Evidence and impact:** `source-note.md:7` says no parent-expansion study has run. Five percentage points is a proposed decision threshold. “Achieved” invents a measured outcome and conflicts with the following statement that evaluation is still upcoming. The source also supplies no “next month” schedule.

**Proposed correction:** “A future paired study proposes testing parent expansion against a fixed pipeline. A five-percentage-point improvement is the proposed decision threshold; no study has run.” Remove the unsupported date. If this section is intended as an executable experiment plan, specify the evaluation metric and dataset before using the threshold to make a decision.

**Remaining uncertainty:** The study date, evaluation dataset, and precise metric are not established by the source note. Do not fill them in as facts.

### 3. Medium — The accuracy change uses the wrong unit

**Location:** `report.md:5`, “improved accuracy by 5%, from 70% to 75%.”

**Evidence and impact:** The absolute change is **five percentage points** (75% − 70%). The relative increase is approximately **7.1%** ((75 − 70) / 70 × 100). Calling the change “5%” confuses these quantities and makes comparisons ambiguous.

**Proposed correction:** Use “Accuracy was 70% for A and 75% for B, a five-percentage-point difference on the 100-question pilot.” Retain the configuration and uncertainty qualifications in finding 1. The relative figure is calculated here, not a separate measured result.

### 4. Medium — The timing example does not measure cold-start latency

**Location:** `report.md:17–23`, measurement description and code.

**Evidence and impact:** `runtime.warmup()` occurs before the timer starts. As confirmed by `source-note.md:11`, the snippet records one post-warmup invocation and excludes process startup and model loading. An engineering reader could otherwise treat this measurement as evidence about startup costs.

**Proposed correction:** Keep the snippet and change its introduction to: “The following records elapsed time for one post-warmup invocation; it excludes process startup and model loading.” If cold-start measurement is the intended goal, define the startup boundary and provide a different procedure that includes the intended initialization work.

**Remaining uncertainty:** No numerical timing result is supplied. The snippet and source do not establish cold-start performance or a representative latency distribution.

## Supported passages

- **`report.md:13` — Pressure limit:** Supported by `source-note.md:9`. At 70 °C, the above-60 °C condition applies, and P-17 revision B, §7 directly establishes a maximum operating pressure of 8 MPa for K-42. No additional general-rule passage is needed. For precision, “maximum operating pressure” could replace “limit”; this is optional clarification.
- **`report.md:28` — Compatibility:** Supported by `source-note.md:13`. Preserve `/v1/answer` for existing clients. This is a supplied fixture requirement and requires no external product verification within this review.

The section headings and short format are easy to scan. The main clarity improvements are to expose the pilot configurations, separate observations from proposed decisions, and make the timing label match the code.
