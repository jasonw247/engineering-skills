# #41 Sync clients cause retry storms during outages

During the 2026-10-30 outage every sync client retried each failed request up
to five times with exponential backoff. With hundreds of concurrent requests per
client, the recovering service received several times its normal load and took
40 minutes to recover instead of 5.

We need a bound on the total retries a client generates, not only per request.
Callers should get a clear error when retries are not allowed.
