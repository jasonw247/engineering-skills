# Skill mechanics

The packaging-specific reference for [writing-for-agents](SKILL.md).

## Discovery and invocation

Keep `name` and `description` concise. Describe the job and the conditions that make it relevant; avoid broad trigger words that attract unrelated tasks. A host can expose those metadata first and load the body only when selected.

Preserve the host's supported invocation policy. For Codex, normal implicit selection is the default. An existing explicit-only skill can retain `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; explicit invocation remains available. Do not rely on a Claude-specific frontmatter flag to configure another host.

An unavailable skill or a URL does not guarantee executable discovery. For a local shared reference, point directly to its file and include it in the installed package or declare the sibling skill as a registry dependency. Use the host's actual loading mechanism rather than assuming a tool named Skill exists.

## Check selection separately from execution

Before loading the body, compare the name and description with requests that should select the skill and neighboring requests that should not. Include the user's actual language, not just the skill's terminology. After loading it, evaluate whether the agent produces a sufficient result and preserves the task's constraints. These are different failure modes.

For an instruction-writing and prose-refinement skill, include a skill-description review, an informal “remove LLM-isms” request, a plain-language drafting request, and an ordinary implementation task. Include a substantive factual review to check the boundary with document-review workflows. Use the actual surrounding catalog when testing collisions. A local metadata exercise does not measure the host's automatic selection rate.

## Splitting and routing

Split when a distinct task needs independent discovery, or when a supporting reference materially reduces the main instruction path. Keep rules needed by every branch in the entrypoint and disclose branch-specific details behind conditional pointers.

A router is useful only when there are enough choices to justify one. A small registry and a bootstrap skill can select and install repository-specific packages; the registry should identify actual local folders, dependencies, and intended use.

Installing interactive skills does not integrate them into a custom harness. Inspect the harness's prompt assembly and execution contract before claiming integration. Non-interactive or read-only pipelines need guidance adapted to the tools and outputs they actually expose.

Official host behavior is documented at https://learn.chatgpt.com/docs/build-skills; check current documentation when changing discovery or invocation configuration.

For the rationale behind the writing and selection guidance, see [source notes](references/sources.md).
