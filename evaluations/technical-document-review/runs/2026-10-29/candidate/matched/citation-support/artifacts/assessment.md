# Assessment of citation-note.md

The recommendation requires substantive correction. Its component-specific latency claim is unsupported, its exactly-once claim contradicts the cited record, and its selection rationale treats observations as measured guarantees.

Scope: targeted verification of all substantive claims in `citation-note.md` against the complete supplied `transport-record.md` (T1, revision 1, 2026-09-15). This review uses only those materials; it does not independently reproduce the pilot or establish behavior beyond the record. Both inputs are unchanged.

## Prioritized findings

### 1. Exactly-once delivery claim contradicts the record — high priority

- **Location:** `citation-note.md`, lines 6–7, “the retry protocol guarantees exactly-once delivery after process restarts.”
- **Evidence:** T1 §3, lines 13–14, explicitly permits duplicate delivery following a process restart, disclaims an exactly-once guarantee, and states that delivery correctness was not benchmarked.
- **Impact:** Engineers could select a transport on a delivery guarantee that the tested protocol does not provide.
- **Correction:** State that the tested protocol permits duplicate delivery after a process restart and makes no exactly-once guarantee. Do not describe delivery correctness as measured.
- **Limit:** The supplied record establishes neither a delivery-correctness benchmark result nor any stronger delivery guarantee.

### 2. Latency improvement is incorrectly attributed to connection pooling — high priority

- **Location:** `citation-note.md`, line 6, “The connection pool caused the latency reduction.”
- **Evidence:** T1 §2, lines 7–9, reports that median latency fell from 100 ms to 80 ms on a fixed synthetic workload after both connection pooling and server CPU allocation changed. No component ablation was conducted, so neither change's contribution can be isolated.
- **Impact:** The note credits one component without evidence and could lead readers to expect the same improvement from pooling alone.
- **Correction:** Report the observed median latency change alongside both configuration changes and the inability to isolate their contributions. Preserve the fixed synthetic workload qualification.
- **Limit:** A comparison that isolates pooling would be needed to establish its individual effect; the supplied pilot does not provide one.

### 3. Transport-selection rationale is unsupported — high priority

- **Location:** `citation-note.md`, line 8, “We should choose this transport solely because these guarantees were measured.”
- **Evidence:** T1 §2 reports a workload-specific latency observation, not a performance guarantee. T1 §3 explicitly denies exactly-once delivery and says delivery correctness was not benchmarked.
- **Impact:** The proposed selection rests on guarantees that the source does not establish. The record alone cannot justify the stated decision rationale.
- **Correction:** Withdraw the selection conclusion as written. State that the pilot observations do not establish sufficient grounds for the proposed selection and that a decision requires relevant selection criteria and supporting evidence.
- **Limit:** The supplied materials do not establish whether this transport should ultimately be selected or rejected.

## Citation support

`[T1]` resolves to the supplied record, and sections 2 and 3 are the relevant sections. The citation is identifiable but does not support the adjacent claims as written: §2 expressly limits causal attribution, and §3 contradicts the claimed delivery guarantee. Correcting the prose is necessary; changing citation formatting alone would not resolve these defects.

## Suggested replacement for lines 6–8

> On a fixed synthetic workload, median latency fell from 100 ms to 80 ms after both connection pooling and server CPU allocation changed. The pilot did not isolate either change's contribution [T1, section 2]. The tested protocol permits duplicate delivery following a process restart and makes no exactly-once guarantee; delivery correctness was not benchmarked [T1, section 3]. These observations do not establish sufficient grounds to select this transport. Selection requires relevant criteria and supporting evidence.
