# Editorial review

Edited `contract-edit.md` for integration engineers. Shortened wording, made the
retry condition's subject explicit, and grouped the dry-run behavior with its
command. Preserved the requirement terms, retry conditions and limit, commands,
ledger path, and quoted reconnect instruction.

Checked the complete revised document against the supplied text for meaning,
internal consistency, and formatting. This was an editorial review using only
the supplied document; commands were not executed and external specifications
were not checked.

## Unresolved issue

- **Reconnect instruction** (`contract-edit.md`, final paragraph): In "Resume the
  session after the server acknowledges it," "it" could mean the session or the
  last batch. Engineers cannot determine which acknowledgment permits resuming.
  The supplied document provides no further source. The instruction's owner must
  identify the intended object before "it" can be replaced with "the session" or
  "the last batch." The quotation remains unchanged in the edited document.
