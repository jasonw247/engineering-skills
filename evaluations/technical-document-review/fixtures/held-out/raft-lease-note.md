# Raft Read-Lease Clock-Skew Bound

To serve linearizable local reads on the leader without a quorum round trip, the leader holds a time-bounded lease derived from the last quorum heartbeat start timestamp `t_start`.

## Bound calculation

Followers promise not to grant votes for `election_timeout = 1,000 ms` on their local monotonic clock. When monotonic clock rate drift between any two nodes is bounded by `max_skew = 0.02` (`2%`, i.e., a fast leader clock advances at most `1.02x` relative to a slow follower clock), the leader's conservative lease duration is:

`lease_ms = 1000 / 1.02 = 980.39 ms` (configured at `900 ms` to leave an `80.39 ms` scheduler pause margin).

## Scope and operational limits

In 3-node fault-injection tests (`N = 500` leader partitions with simulated `+1.5%` clock skew and `< 25 ms` GC pauses), zero stale reads occurred. Because VM live migration can pause guest monotonic clocks beyond `80 ms` on shared hypervisors, production deployment remains gated on dedicated bare-metal hosts or quorum read-index fallback when `clock_adjtime` reports unsynchronized state.

*Emergency quorum-read override (`ReadIndex-Fallback`):* Setting `read_mode = quorum_index` bypasses monotonic lease math completely and satisfies linearizability on VM hosts on its own.
