---
name: writing-for-agents
description: Write or review agent instructions, skills, stage prompts, AGENTS.md, and CLAUDE.md for clear triggers and sufficient execution guidance. Also use when asked to remove LLM-isms, de-jargon, or refine AI-written prose, or to draft prose using a plain-language writing guide. Not for ordinary code changes or factual document audits alone.
---

# Writing for agents

Help an agent find the right guidance and act on it. Write prose that a reader can understand on the first pass. Apply the shared writing guidance while drafting and when refining an existing draft.

## Choose the work

Infer the audience, purpose, requested action, and output destination from the request and existing material. Preserve established terminology, voice, and format. Ask only when missing information would materially change the result.

- **Agent instructions:** apply the instruction-design guidance below and the shared prose guidance. For skill packaging or discovery, read [skill mechanics](SKILL-MECHANICS.md).
- **Prose drafting or cleanup:** apply the shared prose guidance. A request such as “remove LLM-isms” calls for a revision of the supplied text; it does not require converting it into agent instructions. Consult [editing examples](references/editing-examples.md) when a difficult passage needs more than word substitution.
- **Assessment:** report consequential problems and proposed corrections. Edit files when revision is requested; an assessment alone leaves them unchanged.

For pasted prose, return the revised text by default. For file edits, update the requested files and briefly report material changes and unresolved ambiguities. Keep editorial commentary outside the finished prose unless requested.

## Write clear prose

Lead with the point, action, or result the reader needs. Develop each paragraph around one idea, with concrete subjects and verbs. Put causes, conditions, and consequences in an order that makes their relationship clear.

Revise recurring problems by meaning, rather than applying a word blacklist:

| Problem | Revision |
| --- | --- |
| Staged contrasts such as “it's not X, it's Y” or “not merely X, but Y” | State the useful claim directly. Retain a distinction when it corrects a real misconception or defines consequential behavior. |
| Dense jargon, invented labels, and stacks of abstract nouns | Name who does what to which object. Retain precise technical terms the audience needs; explain unfamiliar ones where used. |
| Sentences with unclear subjects, pronouns, or logical connections | Resolve the referent and split the sentence at the change in action or idea. If the intended relationship is unknown, flag it instead of guessing. |
| Defensive caveats and repeated hedging | Keep qualifications that change a decision, claim, or operating limit. State the specific condition once, beside the claim it limits. |
| Inflated claims, stock transitions, and generic praise | Give the supported fact or recommendation and its reason. Remove staging such as “it's worth noting” when it adds no information. |
| Repetition, canned conclusions, forced lists, and excessive emphasis | Keep each point where it helps most. Choose paragraphs, lists, tables, and headings to fit the information and requested format. |

Read the passage as a whole after editing. Rebuild an awkward paragraph around its main point when local replacements leave the structure unclear. Vary sentence length naturally; neither brevity nor a lower jargon count alone establishes clarity. Leave already effective text alone.

Preserve meaning during cleanup:

- Keep facts, quantities, units, citations, conditions, exceptions, and the original strength of evidence. A plausible explanation is not permission to add a claim.
- Preserve required prohibitions and exact technical distinctions. “Do not retry after an unknown write outcome” carries information that a general instruction to “retry safely” loses.
- Preserve code, commands, identifiers, link targets, and quoted text unless their revision is in scope. For instruction-writing tasks, metadata and examples may be the requested edit targets.
- Match the requested voice without inventing personal experience, opinions, humor, or certainty to sound human. These patterns are editing cues, not proof of AI authorship.

## Design instructions an agent can use

### Make the guidance discoverable

A skill description or a conditional link must identify both the job and when to use it. The agent must be able to select it before reading its body. Include the distinct tasks it handles and a boundary for likely neighboring tasks. Use recognizable task language; compressing a trigger into a clever label can obscure its meaning.

For a reference link, state the condition and use a descriptive label: `For uncertain remote write outcomes, read [recovery](recovery.md).` Check that the target is available in the installed package or actual environment. Material with no usable pointer may never be read.

Judge selection wording against realistic positive and negative requests, including informal paraphrases. A description review can identify likely misses and collisions; actual activation reliability requires trials with the host and catalog in use.

### Supply enough to execute

An instruction document should let the agent determine the next action and recognize completion. Include what the task needs:

- **Scope and inputs:** what to change or inspect, required artifacts, and how to obtain missing context.
- **Decisions and actions:** the constraints, ordering, or decision rules that change how the work proceeds. Use ordered steps when order matters; reference guidance can stand alone.
- **Completion and evidence:** the observable result and checks needed to support it. Replace “understand the system” with an outcome such as “trace the request from entry point to persistent write and identify the owner of retries.”
- **Failure handling:** what to do when a prerequisite, tool, or source is missing, where that is a realistic obstacle. Keep any stopping rule proportional to the consequences.
- **Deliverable:** the artifact or report the requester should receive, including material unresolved issues.

These are sufficiency checks, not required headings for every document. Spend instruction space on concrete domain traps, non-obvious edge cases, and verifiable defaults that a capable model misses on its own rather than restating textbook basics or padding sections with defensive scope disclaimers. Include examples when they resolve a likely ambiguity. More demanding adjectives such as “relentless” do not substitute for a verifiable outcome.

State desired behavior directly. Use explicit prohibitions when they express a real boundary, and pair them with the appropriate next action when useful. Treat claims about model attention, negation, or keyword effects as hypotheses to test rather than universal laws.

### Organize and prune

Keep purpose, shared constraints, and the main action path in the entrypoint. Move substantial guidance needed only for a particular task into a linked reference, with its reading condition beside the link. A short, coherent skill can remain one file. Split into separate skills when the jobs need independent discovery.

Keep a concept's definition, rule, example, and exception together. Give each maintained rule one authoritative home. Prefer existing project configuration and commands over restating facts the agent can cheaply inspect; document the conventions, reasons, and pitfalls those sources omit.

Remove repetition, stale instructions, and generic advice that does not change decisions. Preserve enough explanation for the next agent to apply the rule correctly. Optimize for reliable execution and maintenance rather than the fewest tokens.

## Finish the pass

For prose, compare the revision with the source for changed meaning, missing qualifications, and unsupported additions. Read the finished text continuously for unclear references and broken reasoning.

For agent instructions, also check whether a fresh reader can select the guidance, find its references, perform the task, and tell when it is done. Report untested behavioral claims as untested. Use realistic trials when warranted; syntactic validation and an author's walkthrough do not establish selection rates or improvement over an agent without the skill.
