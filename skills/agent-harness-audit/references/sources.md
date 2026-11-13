# Source provenance

Written locally on 2026-11-10 from the harness-engineering skills and notes in [MiniMax-AI/mcode-stack](https://github.com/MiniMax-AI/mcode-stack/tree/d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0) at `d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0` (MIT, inspected 2026-11-10; its copyright and license notice ship as `LICENSE-mcode-stack` in this package):

| Local file | Source in `stacks/ronny/skills/` |
| --- | --- |
| `references/tool-catalog.md` | `tool-budget-audit` |
| `references/request-context.md` | `context-tax-audit` |
| `references/long-commands.md` | `long-command-check` |
| `references/long-sessions.md` | `long-session-check` (review mode) |
| "Confirm changes experimentally" in `SKILL.md` | `harness-experiment` |

The checklists were restructured and reworded, not copied, and combined into one package because they share a trigger: auditing a harness's context and execution design. The source is the MiniMax Code team's practice and its companion *MCode Engineering Notes* 02–05; it is guidance and illustration, not benchmarked evidence.

Not adopted: MiniMax Code commands and tag names, the in-session mode of `long-session-check` (its handoff parts informed the local `handoff` skill), the subagent guidance (adapted separately into `agent-workflow-engineering`), and the human-workflow skills in the same stack.

## Limits

Unverified claims, to check against current provider documentation before relying on them: prompt-cache lifetimes, minimum cacheable prefix sizes, breakpoint limits, and invalidation rules; whether a provider rejects unpaired tool calls; and tool-search recall on real catalogs. No behavioral trial has been run on this package.

## Related documentation

Provider documentation for the checks above; these are not sources of the package's guidance.

- [Anthropic: Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) and [Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [OpenAI: Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) and [Function calling](https://platform.openai.com/docs/guides/function-calling)
- [Google Gemini API: Context caching](https://ai.google.dev/gemini-api/docs/caching)
