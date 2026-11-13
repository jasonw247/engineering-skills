# Request context and prompt caching

Every request carries more than the user's message: the system prompt, environment details, skill and tool listings, per-turn context blocks, and reminders. Most of it is worth sending. The audit finds the parts that are not, and the parts placed so that they defeat the prompt cache.

## Inventory one real request

Capture an actual request from a debug log, a proxy, or the code that assembles it. Do this for the first request of a fresh session and for a later turn. List every part except the user's message:

| Part | Position | How often it changes | Size |
| --- | --- | --- | --- |

## Necessity

For each part, finish the sentence "without this, the model would ...": guess the operating system, assume its training year is the current date, miss a deadline. A part with no answer is a candidate for removal. Then check the recovery paths: if the part is removed or moved, is it restored after compaction, on session resume, and in subagents, and by what?

## Cache placement

Prefix caches match from the start of the request; one changed byte invalidates everything after it. Classify each part:

1. **Early and changes per request.** The most expensive placement, because it invalidates everything after it. Move it later.
2. **Appended to history and never edited.** Paid once, then cached with the rest of the prefix.
3. **Attached to the current request only and not kept in history.** Never cached and paid in full every time. Limit how often it is sent. This saving is separate from protecting the prefix.

Rules of thumb:

- Put stable content first and volatile content last. Keep the current time, counters, and other changing values out of the system prompt and tool definitions; send them in a per-turn block.
- Do not rewrite reminders or tool results already in history, except through deliberate compaction. Change only future turns.
- Use the precision the model needs. A timestamp to the second differs on every request; a date often suffices.
- Send a changing field at session start, on change, or at key points, rather than every turn, when that is enough.

Provider cache semantics differ: minimum cacheable length, lifetime, explicit breakpoints, and what invalidates a cached prefix. Read the current documentation for the provider in use.

## Checklist

| Item | Question |
| --- | --- |
| Prefix boundary | Can you point to where the stable prefix ends and per-turn content begins? |
| Necessity | For each part, what goes wrong without it? |
| Position | Is anything volatile inside the system prompt or tool definitions? |
| Frequency | Does each changing field need to be sent every turn, or only at the start, on change, or at key points? |
| Precision | Does any field carry more precision than the model uses? |
| History | Are entries already in history ever rewritten? |
| Recovery | Is removed or moved content restored after compaction, resume, and subagent start? |
| Measurement | Are cache hit rate, cost per turn, and task quality compared before and after, not just token counts? |

A change can cut tokens while breaking the cache, so token count alone is not evidence of improvement.
