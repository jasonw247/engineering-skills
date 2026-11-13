# Focused research — 2026-10-29

Primary sources were browsed during planning and implementation. Access date:
2026-10-29. Source statements below are paraphrases. Applicability to this skill
is an inference unless identified as an existing repository requirement.

| Primary source and date/version | Established guidance | Application, expected benefit, and tradeoff |
| --- | --- | --- |
| [OpenAI, Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills), Dominik Kundel and Gabriel Chua, 2026-01-22 | Define measurable success before revising instructions. Evaluate captured runs and artifacts with deterministic checks and qualitative rubrics; evaluate activation as well as task execution. | Extend the existing case format, hide acceptance keys from actors, preserve JSONL traces and raw outputs, and distinguish routing from behavior. More model calls cost time and usage; use one full comparison and focused repeats rather than treating anecdotal passes as causal proof. The installed CLI differs from the article's example flags, so commands follow local `codex exec --help`. |
| [Google Technical Writing Two, Self-editing](https://developers.google.com/tech-writing/two/editing), updated 2025-03-31 UTC | Adapt writing to audience; use an appropriate editing strategy and specific constructive feedback. Stylistic techniques are context dependent. | Preserve existing audience-centered structure and optional phrasing reference. Add a standalone clean case and wording-only neighbor. This tests false positives without adding stylistic rules. A clean synthetic note cannot establish false-positive rates on real prose. |
| [ICMJE, Preparing a Manuscript for Submission](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html), sections 3.e–g; no revision date established on fetched page | Report absolute quantities behind percentages, limit conclusions to supported evidence, distinguish unfinished work, and verify that references support associated statements using original or bibliographic sources. | Existing arithmetic and evidence instructions already embody these methods. Add a citation that is identifiable but contradicts its attached claim; check numerical and causal reasoning in existing cases. Do not import medical manuscript templates, universal confidence-interval demands, or journal-specific citation format. |
| [NIST, Technical Series Publications](https://www.nist.gov/nist-research-library/nist-publications), updated 2024-10-10; version policy describes August 2022 changes | Distinct publication versions retain separate identifiers, and status information can identify errata or revisions. | Add paired synthetic version records and an archival document. Check correct applicability rather than requiring every historical document to describe the newest API. Extending a publication-version principle to SDK review is our inference; the fixture establishes its own SDK facts. No real vendor claim is imported. |
| [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt), March 1997, and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.txt), May 2017 | Adopted normative terms distinguish requirements, recommendations, and options; RFC 8174 clarifies uppercase usage while allowing normative text without these keywords. | Test that editing and reassessment preserve the meaning of adopted requirements and conditional prohibitions. This is a testable preservation hypothesis, not evidence the original skill fails. Do not impose RFC capitalization or replace ordinary prose universally. |

Google's [Code samples](https://developers.google.com/style/code-samples) page
was also inspected. Its dominant guidance concerns formatting; it does not
establish that executing an example proves its intended claim. No instruction
change follows from it. The existing skill and repository evaluation protocol
already make the execution-versus-analytical-validity distinction.

## Research decisions before trials

- Demonstrated weakness: current behavioral coverage is incomplete and historical
  results have mixed evidentiary levels. Improve evaluations directly.
- Hypotheses: a model might alter a conditional contract while polishing, repair
  protected errors, carry forward an invalid reviewer preference, over-update an
  archival API claim, or accept an identifiable but contradictory citation.
  Declare outcomes and test before adding runtime instructions.
- Optional preferences rejected: mandatory positive feedback, fixed review
  headings, stylistic blacklists, comprehensive browsing for every number,
  mandatory reformatting of code, and a new general review checklist. None has a
  demonstrated benefit here; several would increase work or false positives.
- Runtime changes require an observed improvement on matched inputs without a
  material regression. Sources explain why a hypothesis matters; they do not
  substitute for behavioral evidence.
