# Writing-for-agents assessment — 2026-10-29

## Findings on the previous revision

1. **Selection missed the requested workflow.** The description covered skills, AGENTS.md, and CLAUDE.md. It did not name prose refinement, LLM-isms, de-jargoning, or plain-language drafting. Instruction-file requests were plausible matches; the user's normal cleanup prompt was a likely miss. This is an editorial prediction, not a measured selection rate.
2. **The audience was clear, but the action was underspecified.** The opening described documents agents consume. It supplied a conceptual essay without a clear assessment/editing distinction, expected deliverable, or final pass. It did not support ordinary prose cleanup.
3. **Useful coverage came with avoidable complexity.** Conditional references, co-location, avoiding duplication, and completion criteria were worth retaining. Dense labels such as “variance lever,” “two loads,” and “post-completion steps” made the guide harder to apply than necessary.
4. **Several recommendations overstated their evidence.** Assertions that negation promotes forbidden behavior, stronger adjectives beat defaults, or hiding later steps improves effort were presented as general mechanisms. The skill supplied no experiment establishing those effects. Compression into a single “leading word” could remove the detail required for correct execution.
5. **Content was incomplete for the requested use.** It lacked practical sentence repair, meaningful caveat retention, technical-term preservation, before/after examples, and checks against changing facts while polishing prose.

## Revision and alternatives

The revised skill retains its installed name and instruction-design role, while explicitly matching requested prose cleanup and drafting with a plain-language guide. Shared writing rules appear in the entrypoint; editing examples are conditional. The instruction path now checks scope, inputs, decisions, completion evidence, realistic failure handling, and deliverables.

Compared plain-language guidance, a detailed AI-pattern editor, and task-oriented skill guidance; [source notes](../../../../skills/writing-for-agents/references/sources.md) record the sources and adopted ideas. A pure pattern blacklist risks removing useful technical contrasts and uncertainty. A general writing guide alone provides weak discovery for the user's cleanup prompt. A second skill would give prose its own discovery name, but duplicate much of this small shared guide. Keep one package for now and reconsider with host evidence.

The updated wording is a plausible match for the informal cleanup request and original instruction-writing work. Ordinary code changes, runtime debugging, and factual audits alone are excluded. Neighboring document-review skills may still overlap on broad clarity requests; test with the actual catalog before claiming reliable automatic selection.

## Validation and limits

The retained cleanup artifact is an **author exercise**, made with the fixture and acceptance criteria visible. It removes empty staging and jargon while preserving supplied facts, necessary uncertainty, retry instructions, the command, and the link target. It is not an independent forward trial or a comparison against an unassisted agent.

Eight cases declare observable expectations. The other seven remain not run. No metadata-only blind routing trial, automatic host-selection trial, or matched baseline was performed. Packaging checks and the existing installer suite are recorded separately in results.json. Those checks do not establish activation rates or writing-quality gains.
