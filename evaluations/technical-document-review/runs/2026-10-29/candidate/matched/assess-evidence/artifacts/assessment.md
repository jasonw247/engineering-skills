# Assessment of report.md

The proposal needs substantive corrections before an engineering reader can use it to justify deployment. Its main problems are causal overstatement, a proposed outcome presented as a result, and an incorrectly labeled timing example.

## Scope

Reviewed all of `report.md` against all of `source-note.md`, following the technical-document-review skill in assessment mode. This is an editorial and supplied-evidence review of synthetic fixtures, not an external source audit. Checks covered claim support, internal consistency, arithmetic, measurement boundaries, and clarity. No experiments or runtime code were executed; neither input was edited.

## Prioritized findings

### 1. High — The pilot does not establish a reranker effect or justify immediate production replacement

**Location:** `report.md:5`, “Reranking improved … proving that the reranker improves production answers” and “replace the baseline immediately.”

**Evidence and impact:** `source-note.md:5` reports 70 correct answers for configuration A and 75 for configuration B on 100 answerable questions. A used reader Small and a 2,000-token context cap; B used reader Large, a 4,000-token cap, and a reranker. The report omits these concurrent changes, so the reader could mistakenly attribute the entire difference to reranking. The pilot did not isolate component effects, estimate statistical uncertainty, or measure latency. It therefore supports a descriptive comparison of the tested configurations, not proof of a reranker benefit in production or an evidence-backed immediate rollout.

**Proposed correction:** “On the same 100 answerable questions, configuration A answered 70 correctly using reader Small and a 2,000-token context cap. Configuration B answered 75 correctly using reader Large, a 4,000-token cap, and a reranker. These results compare the complete configurations; they do not isolate the reranker's contribution. Statistical uncertainty and latency were not evaluated. Further evaluation is needed to support a production replacement decision.”

**Remaining uncertainty:** The reranker's individual contribution, production performance, and deployment tradeoffs are not established by the supplied evidence.

### 2. High — Parent expansion's decision threshold is presented as an achieved result

**Location:** `report.md:9`, “Parent expansion achieved a five-percentage-point improvement. We will run its evaluation next month.”

**Evidence and impact:** `source-note.md:7` says no study has run. Five percentage points is a proposed decision threshold for a future paired comparison against a fixed pipeline. The current wording invents an outcome and contradicts the statement that evaluation is still pending. The source also supplies no date supporting “next month.”

**Proposed correction:** “A future paired study will test parent expansion against a fixed pipeline. A five-percentage-point accuracy gain is the proposed decision threshold, not a measured result. No study has run.” Remove “next month” unless a schedule is supplied.

**Remaining uncertainty:** The outcome and schedule are unknown. For an executable experiment plan, specify the evaluation set, accuracy scoring, fixed pipeline and comparison conditions, and uncertainty analysis; these details cannot be filled in from the note.

### 3. Medium — The timing example measures a post-warmup invocation

**Location:** `report.md:17–23`, “cold-start inference latency” and the accompanying code.

**Evidence and impact:** `runtime.warmup()` runs before `start = clock()`. As confirmed by `source-note.md:11`, the timed interval records a post-warmup invocation and excludes process startup and model loading. Calling it cold-start latency could lead engineers to evaluate startup behavior using the wrong measurement boundary.

**Proposed correction:** Relabel the introduction: “The following records elapsed time for one post-warmup invocation; it excludes process startup and model loading.” Retain the code as an illustration of that boundary. If cold-start timing is required, define the startup boundary and supply an example that includes the intended initialization work.

**Remaining uncertainty:** No numerical timing result is supplied, and the runtime and clock implementations are unspecified. The snippet alone establishes no measured latency value or general performance result.

### 4. Medium — The accuracy difference uses the wrong unit

**Location:** `report.md:5`, “improved accuracy by 5%, from 70% to 75%.”

**Evidence and impact:** The absolute increase is **5 percentage points**: 75% − 70%. The relative increase is approximately **7.1%**: (75 − 70) / 70 × 100. Calling it 5% blurs two different comparisons.

**Proposed correction:** Use “Configuration B's observed accuracy was 75%, compared with 70% for configuration A, a five-percentage-point increase.” Keep the configuration attribution and limitations in finding 1.

**Remaining uncertainty:** This arithmetic describes the observed sample difference; it does not establish statistical significance or an expected production gain.

## Supported passages and clarity

- **Pressure limit (`report.md:13`):** Supported by `source-note.md:9`. At 70 °C, K-42 meets the above-60 °C condition in P-17 revision B, §7, so its maximum operating pressure is 8 MPa. This self-contained passage supplies the necessary condition and limit; no additional general-rule citation is needed. For precision, replace “limit” with “maximum operating pressure.”
- **Compatibility (`report.md:28`):** The `/v1/answer` statement matches `source-note.md:13` and should remain. It is a fixture requirement; no external API verification is needed within this review.
- **Reading flow:** The short sections are easy to scan. The consequential clarity problems concern the status and scope of evidence, rather than sentence complexity. Present the pilot configurations and limitations before the deployment recommendation, and distinguish the planned parent-expansion study from completed results.
