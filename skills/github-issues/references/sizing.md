# Sizing notes

## What the 500-line trigger rests on

- **SmartBear/Cisco code review study** (about 2,500 reviews covering 3.2 million lines, published as *Best Kept Secrets of Peer Code Review*, 2006). Reviewers inspected about 200–400 lines well in a 60–90 minute session. At faster inspection rates they found fewer defects. These numbers come from SmartBear's own summary of the study, not from independent replication.
- **Google engineering practices, "Small CLs".** A change of about 100 lines is usually reasonable and about 1,000 lines is usually too large. A change spread across many files is larger in effect than its line count suggests.

Both sources measure how well a reviewer can inspect code, not whether a pull request of a given size succeeds. So about 500 lines is the point at which to *consider* a split, and coherence decides the outcome. A smaller change that mixes two purposes may need splitting. A larger one that cannot be reviewed or merged in parts may not. A size limit in the repository's own instructions replaces this figure.

## Other signals to consider splitting

- The change needs more than one behavior change, or it mixes a refactor with a behavior change.
- Its acceptance criteria cannot be met by one pull request.
- Separate owners must each approve independent parts.
- Configuration, rollout, or migration steps would be reverted on a different schedule from the code.

## Count

- Count lines added or changed in hand-written code and tests.
- Exclude generated code, vendored code, lockfiles, and snapshots.
- Count a mechanical rewrite produced by a tool as one reviewable unit. Record the command that produced it.

## Estimate

1. List the modules, interfaces, and tests the work touches.
2. Guess the changed lines for each, including the tests for its behavior.
3. Compare the total with similar merged pull requests in the same repository (see [gh commands](gh-commands.md)).
4. Round the result and label it as an estimate in the issue.

Once implementation exists, the actual diff replaces the estimate. If it overshoots badly, consider splitting the remaining work. Do not reopen work that has already merged in order to split it.
