# Assessment of the SDK 2.4 archival record

The SDK 2.4 API claim is correct for the stated version and edition. The supplied records also confirm removal in SDK 3.0, but do not establish current support availability. The note should remain an archival SDK 2.4 record; no code migration is warranted by this assessment.

## Claim assessment

| Statement in version-note.md | Finding from vendor-records.md |
| --- | --- |
| In SDK 2.4, `Session.resume(token)` resumes a session after process restart [V24]. | **Supported.** V24 explicitly describes this behavior for SDK 2.4 local edition, released 2024-04-15. Its removal in a later version does not invalidate this version-specific statement. |
| The API was removed in SDK 3.0 [V30]. | **Supported as a version-specific fact.** V30, released 2025-02-01, states that `Session.resume` is removed and SDK 3.0 uses `Client.restore(checkpoint)`. This does not establish the contract for any later or currently installed version. |
| For a current integration, confirm the installed version and its applicable contract before selecting the resume path. | **Appropriate guidance, not completed verification.** The supplied records show that the contract differs between 2.4 and 3.0. They do not identify an installed version or establish today's applicable contract. |
| SDK 2.4 local-edition support remains available today [V24]. | **Unsupported.** V24 explicitly makes no support-lifecycle promise, and no lifecycle notice is supplied. The records establish neither continued support nor an end of support. |

## Archival chronology and current verification

The note says it was written on 2024-05-01, while its V30 source is dated 2025-02-01. The removal claim agrees with the supplied later record, but that source cannot substantiate it as knowledge available on the stated original writing date. If the claim was added later, the archive should identify that later annotation or revision; the supplied evidence does not establish that revision history.

“Today” is undated within the support claim. Whether it means the note's stated writing date or the assessment date (2026-10-29), the supplied records do not verify support availability. SDK 3.0 is the newest release represented in the evidence, not a verified current release. No network or other sources were consulted.

## Recommended wording

Preserve the SDK 2.4 behavior statement. Identify the SDK 3.0 information as a later annotation if that reflects the actual revision history, without inventing a revision date. Replace the unsupported support claim with:

> The supplied SDK 2.4 release record does not establish support availability or lifecycle status. Current support status is unverified from the supplied records.

The input files were not edited.
