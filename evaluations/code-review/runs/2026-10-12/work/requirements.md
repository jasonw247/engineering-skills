# Event listing contract

`latest(events, limit)` returns at most limit events, newest timestamp first. Input order breaks timestamp ties. Distinct events may share a timestamp and must all remain eligible. limit is a nonnegative integer; zero returns an empty list. The input may be a very large list; common limits are 10 or 20. Preserve this contract. Do not edit during review.
