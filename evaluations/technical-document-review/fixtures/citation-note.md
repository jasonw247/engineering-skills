# Transport recommendation

Synthetic proposal for transport engineers. All available evidence is in
transport-record.md. Citation [T1] identifies that supplied record.

The connection pool caused the latency reduction, and the retry protocol
guarantees exactly-once delivery after process restarts [T1, sections 2 and 3].
We should choose this transport solely because these guarantees were measured.
