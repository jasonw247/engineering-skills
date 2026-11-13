# Assessment of citation-note.md

The recommendation requires material correction. Its citation identifies the supplied record correctly, but the record does not support attributing the latency reduction to connection pooling, explicitly contradicts the exactly-once guarantee, and does not establish the stated basis for choosing the transport.

Scope: targeted verification of every substantive claim in `citation-note.md` against the complete supplied `transport-record.md` (T1, revision 1, 2026-09-15). Both files were read in full. This assessment uses only those materials; it does not independently reproduce the pilot or verify protocol behavior. Locations below use the original files' line numbers. Both inputs are unchanged.

## Findings, in priority order

### 1. Exactly-once delivery is contradicted by the cited record

**Location:** `citation-note.md`, lines 6–7: “the retry protocol guarantees exactly-once delivery after process restarts.”

**Evidence:** T1 §3, `transport-record.md`, lines 13–14, states that the tested protocol permits duplicate delivery following a process restart, makes no exactly-once guarantee, and was not benchmarked for delivery correctness.

**Impact:** Engineers could rely on a delivery property that the tested protocol explicitly does not provide, leaving duplicate delivery unaccounted for after a restart.

**Correction:** State that duplicate delivery is permitted after process restarts and that the protocol provides no exactly-once guarantee. Retain the distinction between this stated protocol behavior and measured delivery correctness, which is unavailable. The record does not establish other delivery guarantees.

### 2. The latency result does not isolate connection pooling's contribution

**Location:** `citation-note.md`, line 6: “The connection pool caused the latency reduction.”

**Evidence:** T1 §2, `transport-record.md`, lines 7–9, reports that median latency fell from 100 ms to 80 ms on a fixed synthetic workload after both connection pooling and server CPU allocation changed. No component ablation was conducted, so neither change's contribution can be isolated.

**Impact:** The note presents a component-specific causal conclusion that the pilot cannot establish. Readers could expect pooling alone to reproduce the observed improvement.

**Correction:** Report the observed median latency change, workload, and both configuration changes together. Explicitly state that the pilot cannot isolate their individual contributions. A pooling-specific causal claim would require an isolating comparison absent from the supplied evidence.

### 3. The selection recommendation misrepresents what was measured

**Location:** `citation-note.md`, line 8: “We should choose this transport solely because these guarantees were measured.”

**Evidence:** T1 §2 reports a latency observation under the combined changes, not a latency guarantee. T1 §3 explicitly says that delivery correctness was not benchmarked and that no exactly-once guarantee exists.

**Impact:** The recommendation converts a limited pilot result and a contradicted protocol claim into an asserted sufficient basis for selection.

**Correction:** Withdraw the assertion that these guarantees were measured and that they alone justify selection. Present the pilot as limited evidence for consideration. The supplied materials do not establish that this transport should be selected; suitability remains unresolved without selection requirements and evidence addressing them.

## Source-supported replacement

> On a fixed synthetic workload, median latency fell from 100 ms to 80 ms after both connection pooling and server CPU allocation changed. No component ablation was conducted, so the pilot cannot isolate either change's contribution [T1, section 2]. The tested protocol permits duplicate delivery following a process restart and makes no exactly-once guarantee; delivery correctness was not benchmarked [T1, section 3]. These results alone do not establish that we should choose this transport.

The citation token `[T1]` resolves to the supplied record, and its section references exist. The defects concern support for the attached claims, rather than citation identification.
