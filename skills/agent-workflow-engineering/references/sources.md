# Source provenance

Written locally on 2026-10-12. State and execution boundaries are engineering recommendations, not benchmarked results or claims about current framework or vendor capabilities. The success-before-receipt-write case comes from a 2026-10-12 design refinement; the retention, uncertain-outcome, and logical-action-identity analysis is a design requirement for the synthetic evaluation case, not a claim that any provider guarantees those behaviors.

On 2026-11-10, [subagent boundaries](subagent-boundaries.md) was written locally from `stacks/ronny/skills/subagent-split-check` and the chain-of-summaries point in `review-capacity-check` in [MiniMax-AI/mcode-stack](https://github.com/MiniMax-AI/mcode-stack/tree/d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0) at `d520b2b7e864b08ddd62fa3b79c95ec79ec6c2e0` (MIT, inspected 2026-11-10). It was reworded and restructured, not copied; the upstream copyright and license notice ship as `LICENSE-mcode-stack` in this package. Its split conditions are that team's practice, not benchmarked evidence.

## Limits

No SDK or product version claims have been freshly verified for this package. Check installed behavior or current primary documentation before using version-sensitive APIs, and confirm replay, checkpoint, and idempotency retention rules against the installed runtime and provider. Behavioral acceptance fixtures and results live outside the deployable skill; synthetic trials do not establish production readiness or improvement over an unassisted baseline.

## Related documentation

Protocol and runtime references for checking those rules; these are not sources of the package's guidance.

- [IETF `Idempotency-Key` HTTP header field draft](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
- [Temporal: deterministic constraints](https://docs.temporal.io/workflows#deterministic-constraints)
