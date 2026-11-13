# Assessment of the retrieval upgrade proposal

The report needs revision before it can support an engineering decision. Its pilot counts are consistent with the source note, but it attributes the improvement to one component despite simultaneous configuration changes, overstates production readiness, presents an unrun experiment as successful, and mislabels the timing example. The pressure-limit interpretation and API compatibility statement are supported.

This is an editorial and supplied-evidence review using only `source-note.md`. No external source audit was performed or needed; the note establishes the available facts. References below use the original input line numbers.

## Findings

### 1. High: the pilot does not isolate reranking or justify immediate replacement

**Report:** line 5. **Evidence:** source note, line 5.

Configuration A produced 70 correct answers using reader Small and a 2,000-token context cap. Configuration B produced 75 using reader Large, a 4,000-token cap, and a reranker. Because the reader, context cap, and reranking all changed, the result cannot establish how much improvement came from reranking. “Proving that the reranker improves production answers” exceeds the evidence: this was an internal pilot on answerable questions, with no estimate of statistical uncertainty or latency measurement.

The instruction to replace the baseline immediately is consequently not justified by the supplied evidence. The absence of uncertainty estimates does not establish either significance or insignificance; neither should be asserted.

**Suggested revision:** “In an internal pilot of 100 answerable questions, configuration A answered 70 correctly and configuration B answered 75 correctly. B changed the reader from Small to Large, increased the context cap from 2,000 to 4,000 tokens, and added a reranker. The pilot did not isolate component effects, estimate statistical uncertainty, or measure latency, so it does not establish a reranker-specific production benefit or justify immediate replacement.”

### 2. Medium: the percentage change is ambiguous

**Report:** line 5. **Evidence:** source note, line 5.

An increase from 70% to 75% is **5 percentage points**, or approximately **7.1% relative improvement** over 70%. “Improved accuracy by 5%” conflates these quantities. It also obscures that the observed difference was five correct answers out of 100.

**Suggested revision:** “Configuration B's observed accuracy was 75%, compared with 70% for configuration A, a five-percentage-point increase.” Attribute the difference to the configurations, subject to finding 1.

### 3. High: parent expansion's decision threshold is presented as a measured result

**Report:** line 9. **Evidence:** source note, line 7.

No parent-expansion study has run. The five-percentage-point gain is a proposed decision threshold, not an achieved improvement. The report also claims an evaluation date of “next month,” which the source note does not supply. Combining an asserted result with a future evaluation makes the experiment's status unclear.

**Suggested revision:** “A future paired study proposes testing parent expansion against a fixed pipeline, with a five-percentage-point gain as the proposed decision threshold. The study has not yet run.” Remove the unsupported date.

### 4. Medium: the timing example measures a post-warmup invocation

**Report:** lines 17–24. **Evidence:** source note, line 11.

`runtime.warmup()` occurs before the timer starts. The timed interval covers a subsequent `runtime.run(sample)` invocation, not process startup or model loading. Calling this “cold-start inference latency” misstates the measurement boundary. No numerical latency result is available.

**Suggested revision:** Change the introduction to “The following times one post-warmup invocation.” The existing code then matches the description. If cold-start latency is the intended metric, define its boundary and include the relevant startup and loading work in the timed interval; merely deleting the warmup call would not demonstrate that those costs are included.

## Supported statements to retain

- **Pressure limit (report line 13; source note line 9):** At 70 °C, connector K-42 falls under the “above 60 °C” condition in P-17 revision B, §7, so its maximum operating pressure is 8 MPa. The passage supplies the connector, revision, condition, and limit directly; no additional passage is needed. For clearer engineering wording, use “maximum operating pressure” instead of “limit” and “That passage” instead of “That exception.” The source does not establish that the rule is an exception.
- **API compatibility (report line 28; source note line 13):** The statement that existing clients retain `/v1/answer` matches the supplied fixture requirement. It needs no correction within this review's scope.

Address the unsupported conclusions and experiment status first, then correct the percentage terminology and timing description. Preserve the supported pressure and compatibility statements.
