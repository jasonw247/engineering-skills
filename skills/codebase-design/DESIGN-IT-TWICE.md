# Design it twice

Compare two or three genuinely different module boundaries when an interface is hard to change later or the first sketch feels awkward.

## Procedure

1. **State the problem in one paragraph:** callers, core invariants, failure modes, and hard constraints.
2. **Sketch distinct shapes**, varying abstraction level or ownership rather than minor naming tweaks:
   - a minimal high-level operation that owns retries/state internally vs a lower-level composable primitive;
   - passing plain data values in/out vs stateful handle/guard ownership;
   - extending an existing module's contract vs introducing a new seam.
3. **Write a real caller snippet for each option.** Count what the caller has to import, configure, order, clean up, and handle on error.
4. **Compare trade-offs explicitly:** interface cost to callers, where edge-case bugs live (locality), how failure paths are tested, and what breaks if requirements shift slightly.
5. **Recommend one design** (or a clean synthesis) and state what complexity it deliberately accepts. Keep this comparison inside the current session unless the user explicitly asks to fan out parallel subagents.
