# Implementation contract integration

Use this only when adapting a host's implementation instructions. Merge missing decision rules into the existing contract; do not install another always-active skill or duplicate rules already present. It does not change stage permissions or require a plan artifact for trivial work.

Suggested compact contract:

> Choose the smallest complete solution to the original request. Inspect existing implementations, callers, and constraints before adding structure. Reuse repository facilities, suitable platform APIs, and installed dependencies; justify a new dependency by the complexity or risk it removes. Minimize maintenance obligations rather than line count.
>
> Give each new boundary, option, or abstraction a current purpose. Security, resource ownership, public contracts, and meaningful test isolation can justify a boundary with one implementation. Share duplicated knowledge without coupling unrelated domain rules.
>
> Fix the shared cause when evidence supports it, and propagate required changes to callers, tests, fixtures, and contracts. Preserve supported behavior and trust-boundary checks. State observable acceptance criteria and relevant exclusions in an existing plan when needed; revise the plan when evidence changes.
>
> Establish changed behavior with risk-appropriate checks. Treat review feedback as a hypothesis to verify against requirements and code, then apply supported corrections. Report what the final candidate's evidence establishes and what remains unverified. List the decisions the request left open, such as defaults chosen, scope excluded, and requirements reinterpreted where they conflicted, so the requester or reviewer can accept or change them.

These locally written rules draw on [Ponytail](https://github.com/DietrichGebert/ponytail/blob/84740e3d344b69b4a133201fa519eb37a62a2b2a/skills/ponytail/SKILL.md) and [Greybeard](https://github.com/nassiharel/greybeard/tree/d9b9881fe9b0ce7456af367393db7376408c7776), inspected 2026-10-15. Their session modes, mandatory loops, response templates, and hook integrations are not adopted. The open-decisions list draws on `evidence-first-review` in [mcode-stack](https://github.com/MiniMax-AI/mcode-stack/tree/d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0/stacks/ronny/skills/evidence-first-review), inspected 2026-11-10.
