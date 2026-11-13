# Request-scoped single-call extraction assistant

Use an ordinary request handler. The request needs no workflow engine, graph, durable task state, approval process, or side-effect recovery: it has one model call and no external mutations. This is a design, not an executed implementation.

Define the target record schema and business rules in application code before implementation. Validate/authenticate the incoming request and bound its size; treat its text as untrusted data. Send one fixed extraction instruction plus the source text to the existing model adapter, requesting a structured object with only the allowed fields. The record schema, required fields, allowed values, nullability, date/unit rules, and cross-field consistency are application-owned, not chosen by the model. The specific target record is not provided here and remains an interface dependency.

The synchronous states are:

`RECEIVED → INPUT_VALIDATED → MODEL_PENDING → OUTPUT_VALIDATED → SUCCEEDED`

Alternative terminal outcomes are `INPUT_INVALID`, `EXTRACTION_INVALID`, `UPSTREAM_ERROR`, `TIMED_OUT`, or `CANCELLED`. `SUCCEEDED` means exactly one returned record passes deterministic schema and business validation. It does not by itself prove every extracted fact is true; include source-span checks for fields where correspondence is mechanically checkable, and return an uncertainty/validation error when the required source content is missing.

Make exactly one model request per handler invocation. Disable SDK automatic retries and do not add repair prompts: malformed JSON, extra fields, invalid types, failed constraints, or missing required values return a structured error such as `{status: "invalid_extraction", issues: [...]}`. Transport failure returns an upstream error. No external tool access or mutation is exposed to the model. Application code returns the validated typed record, not arbitrary instructions embedded in the model response.

Proposed resource settings are a 30-second model deadline, a schema-appropriate input limit, a 2,000 output-token cap, and a configured per-request cost ceiling checked before the call. Tune these to the record size rather than expand calls automatically. Client cancellation stops waiting and requests cooperative cancellation from the adapter; if remote inference already started it may still consume cost. Because there is no business mutation, no shipment-like uncertain-effect state is needed. A caller retry is a new request and may create another inference charge; do not claim inference executes once across caller retries.

State lives in the request context and is discarded after response. Log only the correlation ID, timing, model/config version, outcome code, and permitted validation diagnostics under existing data-handling policy; do not retain source/record payloads by default. Return a typed error if the request process crashes or expires through the existing server boundary. Persistence or deduplication is unnecessary unless a later requirement adds resumability or cross-request billing control.

Verify with a fake model adapter: valid record, malformed JSON, missing/extra fields, invalid enum/date/units, contradictory fields, source text attempting instruction injection, timeout, cancellation, and upstream failure. Assert one call maximum, no tool/mutation calls, and no successful response for invalid output. Evaluate extraction accuracy on representative reviewed examples separately from these deterministic handler checks. These checks are proposed; none were executed for this design-only request.
