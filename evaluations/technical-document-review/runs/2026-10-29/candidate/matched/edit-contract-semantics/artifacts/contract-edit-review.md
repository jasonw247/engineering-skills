# Editorial review

Edited `contract-edit.md` for engineers integrating the batch client, using only
the supplied document. Clarified the retry conditions, grouped the dry-run
behavior with its command, and shortened the ledger instruction.

Checked the revised text against the original for meaning and internal
consistency. Preserved the RFC requirement terms, both retry prerequisites, the
limit of two retries, the dry-run behavior, the command and variable assignment,
and the quoted reconnect instruction. Commands were reviewed as text, not run;
no external verification was performed.

## Unresolved issue

In `contract-edit.md`, the final paragraph quotes the handover note: "Resume the
session after the server acknowledges it." The supplied document does not say
whether "it" means the session or the last batch, so engineers cannot determine
which acknowledgment permits resuming. The quote remains unchanged. The
instruction's owner must identify the intended acknowledgment target before
"it" can be replaced with an explicit noun. No further source is available in
the supplied document.
