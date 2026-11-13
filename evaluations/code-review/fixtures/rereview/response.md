# Author response

CR-1 fixed: revised.py no longer deduplicates, so every event remains eligible.

CR-2 rejected: after deduplication timestamps are unique, so no two ranked events can tie and the tie order cannot be observed.

CR-3 rejected: requirements.md defines limit as a nonnegative integer; a negative limit is outside the contract.
