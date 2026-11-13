# Workflow recovery request

Our existing application stores workflow state in a transactional database. A model drafts a request to ship a replacement device. A human approves that specific customer, address, and item; ordinary code validates the request and sends it to a shipping provider. The workflow may be offline for 72 hours after a worker crash.

The provider supports `submit(operation_key, payload)` and `lookup(operation_key)`. Repeating the same key and payload is deduplicated for 24 hours. A different payload with the same key is rejected during that period. Lookup returns a stored receipt if found, ABSENT if no record is currently retained, and UNKNOWN on network/provider failure. After 24 hours, key retention is not guaranteed; ABSENT therefore does not prove that no shipment was created. There is no transaction spanning our database and the provider.

An action can succeed while acknowledgment or our subsequent database receipt write fails. Some requests legitimately ship identical items to the same address on different dates. Do not merge these separate user intentions by payload hash.

Provide states, retry/termination rules, and recovery for: crash before submit; success followed by lost acknowledgment; success followed by local receipt-write failure; recovery after 72 hours with ABSENT lookup; duplicate approval events; and cancellation while submission outcome is UNKNOWN. No real shipment should be executed. Keep the current stack unless its capabilities demonstrably fail a requirement.
