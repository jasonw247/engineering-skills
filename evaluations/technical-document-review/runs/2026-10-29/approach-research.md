# Potential review approaches — supplemental research

Research date: 2026-10-29. Status: **research and proposed experiments only**.
None of the variants below has been behaviorally evaluated or installed. The
earlier comparison and its recorded outputs remain unchanged.

## What this investigation adds

The previous work showed that the current skill and a no-skill baseline could
handle twelve small, explicit synthetic tasks. The identical original and final
packages did not compare alternative approaches. That does not establish that
better approaches are unavailable.

The current entrypoint is 761 whitespace-separated words. The earlier original,
retained, and no-skill arms reported 71/65/49 terminal commands and
17,916/16,712/13,596 output tokens, respectively. These are observations from
`results.json`, not controlled estimates of the skill's causal overhead.
They justify investigating efficiency, while the ceiling in pass counts calls
for harder tasks before judging quality improvements.

Two specific limitations of the current workflow are discoverable by inspection:
it gives review criteria without a claim-coverage mechanism, and its instruction
to preserve meaning does not specify an explicit comparison of edited claims.
These are opportunities for a different method, not demonstrated behavioral
defects. Much of the desired behavior is already described at a high level;
merely repeating those principles would not constitute a new approach.

## Primary evidence and limits

All sources below were opened, not just located through snippets. Source findings
are paraphrased. Proposed applications in subsequent sections are our inferences.

| Source, publication/version, and inspected material | Finding relevant to an alternative | Transfer limit |
| --- | --- | --- |
| [FActScore](https://aclanthology.org/2023.emnlp-main.741/), Min et al., EMNLP, December 2023; abstract and publication record | Evaluates supported atomic facts rather than assigning a single binary judgment to mixed factual text. | Generation evaluation, mainly biographies, does not prove that adding a claim ledger improves document review. Precision alone does not measure useful content retained. |
| [ALCE](https://aclanthology.org/2023.emnlp-main.398.pdf), Gao et al., EMNLP, December 2023; §3.3, appendix F.2, and G.2 | Separates correctness and citation quality; support can come from a joint source set. Its instruction comparison reports stronger correctness and citation recall with full instructions. | Its citation generator and NLI grader are not this reviewer. Automated judgments and prompt-length findings are specific to those models and tasks. Shorter is not inherently better. |
| [Chain-of-Verification](https://arxiv.org/html/2309.11495v2), Dhuliawala et al., arXiv v2, September 25, 2023; §3–4 | Separates verification questions from draft answers; factored verification removes the draft and other verification answers from each question's context. Experiments report factuality benefits. | Primarily Llama 65B generation experiments. Adding a same-context “double-check” sentence does not reproduce the factored method or establish a benefit for the current model. |
| [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/html/2310.01798v2), Huang et al., ICLR 2024, arXiv v2, March 14, 2024; §1, §6–7 | Finds limits and sometimes degradation in reasoning self-correction without external feedback; calls for comparable inference budgets and strong baselines. | Its reasoning benchmarks and older models do not establish universal inability to self-correct. It cautions against assuming more critique calls make a reviewer better. |
| [RARR](https://aclanthology.org/2023.acl-long.910.pdf), Gao et al., ACL, July 2023; §2.2, §6, and footnote 2 | Evaluates both evidence attribution and preservation of original intent. Deleting or replacing content can improve attribution while destroying the document's purpose. Attribution itself does not establish source truth. | Post-editing model outputs differs from editing an authored technical document. Edit distance alone is not a semantic-preservation test. |
| [Studies on Reading Techniques](https://www.cs.umd.edu/~basili/publications/technical/T114.pdf), Basili et al.; §2.2 and bibliography | Human requirements-review experiments use tester, designer, and user perspectives. Results depend on document/domain; review can take longer without a significant false-positive reduction. | Human teams and requirements specifications do not establish an LLM result. The fetched PDF has no explicit cover publication date; it cites the 1996 journal study and November 1996 work. Do not assign it the repository's crawl date. |
| [The Empirical Investigation of Perspective-Based Reading](https://drum.lib.umd.edu/items/7eb0ef0c-4045-4a28-b7ca-b8e2df410d16/full), UMD CS-TR-3585, issued December 1995 | Repository metadata establishes the technical-report identity and operational-scenario subject. | Metadata was inspected; the full report was not successfully fetched. Experimental findings above come from the opened authors' Studies paper, not an inferred reading of this report. |
| [Lost in the Middle](https://arxiv.org/abs/2307.03172v3), Liu et al., arXiv v3, November 20, 2023; abstract and version record | Relevant-information position affects performance in the tested long-context QA and retrieval settings. | Does not test this model or prove a section map solves document review. It motivates a position-controlled long-document test. |
| [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), accessed October 29, 2026; edge cases and model-grader guidance; revision date not established | Recommends realistic and difficult inputs, criterion-based comparisons, and attention to judge position and verbosity biases. | Evaluation guidance supports a design, not a numerical improvement prediction. No dependence on a hosted Evals API is proposed. |

## Candidate approaches

### A. Track consequential claims against evidence

**Change from the current skill:** for evidence-dense documents, make a compact
working map of the consequential claims before writing findings. For each, retain
the statement's conditions and source location, and distinguish supported,
contradicted, inferred, and unresolved support. Review the supplied source set
together when support is distributed. Consult it when deciding whether a claim
was missed or its scope was strengthened.

This operationalizes existing evidence rules rather than adding more kinds of
prohibited claims. FActScore and ALCE motivate the granularity; adoption here is
an inference. Keep the map as working material unless an audit trail is requested.
Do not require a visible table for every document or atomize qualifications away.

**Expected benefit:** fewer missed subclaims, citation mismatches, and unsupported
inferences in reports with many interdependent assertions. **Cost/risk:** extra
context and bookkeeping; unreliable decomposition can remove relevant conditions.

**Discriminating test:** a long report with a partly supported compound claim,
two jointly sufficient passages, a conflicting edition, and a valid numerical
observation beside an unsupported causal inference. Compare material-defect
recall and valid-source-set acceptance at comparable verification budgets.

### B. Validate proposed findings against sources and plausible interpretations

**Change:** before finalizing a material finding, formulate a neutral question
about its premise, answer from the actual text/source/measurement, and check
whether a plausible interpretation defeats the alleged defect. Downgrade missing
metadata or optional improvements when they do not establish an error or a reader
problem. Do not repeat the draft finding as if repetition verified it.

CoVe suggests separating a question from a proposed answer; the self-correction
study cautions against unsupported reconsideration. A single-context source check
is a practical variant, not an implementation of factored CoVe. A genuinely
separate verifier is a different, higher-cost harness experiment, not a default
skill requirement or an authorization to delegate.

**Expected benefit:** fewer asserted defects based on assumptions. **Risk:** an
overly skeptical check can suppress genuine problems or add circular critique.

**Discriminating test:** clean and defective pairs covering a creation date with
a documented later amendment, an actually inconsistent snapshot date, a defined
technical term that sounds promotional, and a real contradictory source. The
previous ambiguous chronology observation is motivation, not a confirmed failure
or an answer key. Measure invalid findings and missed valid defects separately.

### C. Audit the meaning of material edits

**Change:** before substantial editing, identify the small set of requirements,
qualifications, values, and references that must survive. After editing, compare
the changed assertions with the originals and their evidence. Each factual change
must resolve a supported issue; otherwise preserve the assertion or report the
uncertainty. Follow changes into dependent conclusions, tables, and examples.

RARR motivates evaluating evidence and preservation together. The current skill
already demands minimal, meaning-preserving edits; this candidate supplies an
explicit comparison mechanism. A short task need not acquire a separate ledger.

**Expected benefit:** catches technically consequential rewrites that remain
fluent. **Risk:** models may misstate the original invariants; preserving false
claims is not success. Byte comparisons protect exact text, not semantic intent.

**Discriminating test:** a multi-section edit with a genuine numerical correction
but otherwise valid negation, modality, quantifiers, scope exceptions, table
denominators, and API literals. Score useful corrections, retention of supported
meaning, and unauthorized assertion changes. Do not reward deleting difficult
claims or minimizing edit distance at the expense of accuracy.

### D. Review through the reader's task

**Change:** for a procedure or implementation-facing design, walk one meaningful
reader task from starting state to expected result. Identify where the reader
must guess a prerequisite, select an undefined branch, or interpret a result
without criteria. For a proposal, follow the decision the reader must make.

Perspective-based reading supplies a rationale for focused scenarios. This is a
mental or permitted local walkthrough by the current reviewer, not mandatory
multiple personas or live production execution. Keep infrastructure redesign
outside a document-review assignment.

**Expected benefit:** detects missing information that sentence-level fact checks
can overlook. **Risk:** adding assumed audience needs can manufacture omissions;
more review perspectives can increase time without improving precision.

**Discriminating test:** a superficially accurate runbook with an omitted required
permission and no way to recognize successful recovery, paired with a complete
runbook that legitimately refers to a stated prerequisite. Compare actionable
omission findings and unnecessary demands on the clean control.

### E. Track coverage and dependencies in long documents

**Change:** when context size or many cross-references make omission likely,
maintain a short section/dependency map while reading. Revisit decisive
definitions, exceptions, table notes, and conclusions together before reporting.
Record unreviewed regions. Avoid treating retrieved snippets as complete coverage.

The current skill already requires continuous reading and consequential
cross-references. The new method makes coverage state explicit. Lost in the
Middle motivates testing positional sensitivity, not rearranging or truncating
all source material by default.

**Expected benefit:** catches distant contradictions and qualifiers. **Risk:**
summaries can themselves lose exceptions; mapping adds work to simple documents.

**Discriminating test:** matched document variants placing an exception at the
beginning, middle, and end, plus a contradiction spanning a table and a distant
conclusion. Measure positional consistency and correct use of exceptions while
keeping the full raw documents accessible.

### F. Reduce default instruction and reporting overhead

Test two small changes **separately**:

1. **Conditional detail:** keep modes, authority, verification depth, core
   preservation rules, finding requirements, and stopping in the entrypoint.
   Move the extraction/SDK caveat and schema/plotting illustration into the
   existing technical-evidence reference, where the same distinctions already
   appear. Preserve explicit routing so the detail remains discoverable.
2. **Report proportionality:** prefer located material findings and one concise
   coverage/verification statement. For a clean result, do not require an
   exhaustive list of successful checks unless requested. Preserve evidence
   needed to assess every consequential finding and all unresolved limitations.

These candidates are motivated by local duplication and the prior resource-use
observations, supported by the local skill-creator's progressive-disclosure
guidance. They are not empirically established optimizations. ALCE's fuller-prompt
result is relevant counterevidence against assuming shorter instructions improve
quality. A shorter final report is also distinct from fewer model/tool tokens.

**Expected benefit:** lower default context or reader effort on ordinary reviews.
**Risk:** conditional instructions may fail to load; aggressive concision can hide
needed evidence or qualifications. No universal word limit is proposed.

**Discriminating test:** retain the existing regression suite, then compare short
clean notes, dense flawed reports, and extraction/example cases that need the
moved detail. Require equivalent correctness and preservation before considering
tokens, calls, or report length. Do not infer billing or speed from token totals.

## Recommended order and comparison design

Start with **A (claim coverage)** and **F1 (conditional detail)** as separate
candidate packages. A tests a substantive review method; F1 tests a small,
plausible efficiency change. Follow with **B** using clean/defective pairs to test
finding precision, then C for editing, and D/E where the document type warrants
them. This order is an engineering judgment about benefit, risk, and testability,
not an empirical ranking of the approaches.

Use the existing cases as regression guards. They have a demonstrated ceiling
for the tested agent; they cannot be the only optimization benchmark. Create
new realistic multi-section documents with unobvious errors and clean controls.
Keep acceptance keys and defect locations out of actor context, and avoid
teaching proposed methods by embedding their conclusions in the source notes.
Use public or otherwise authorized documents; document amendments and applicable
versions in the evaluation ground truth.

Compare each real candidate against the frozen original and no-skill baseline
using matched inputs, model settings, tool access, and inference budgets. Change
one method at a time. For a multi-call verifier, include an equally budgeted
baseline rather than attributing extra inference to the method itself. Repeat
change-supporting and regression cases as previously selected by the user.

Judge material finding precision and recall, severity, source support, technical
meaning retained, stopping and questions, and reader usefulness. Keep metrics
separate: abstaining or deleting claims cannot earn a perfect usefulness score.
Use deterministic checks for bytes and arithmetic, plus semantic review for
findings and edits. In pairwise review, conceal the arm and vary answer order;
do not reward verbosity. A fresh final holdout should confirm any chosen change.

All proposed comparisons remain **not run**. No source establishes improvement
for this skill, this agent, or the current model. No runtime instructions or
registry metadata are changed by this supplemental research.
