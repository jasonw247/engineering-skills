"""Async event relay with stream-lifetime, request-isolation, and retry defects."""

import json
import uuid

_active_tenant = None


async def relay_tenant_stream(tenant_id, open_stream, forward_record, max_attempts=3):
    """Read NDJSON lines from an async stream and forward valid records upstream."""
    global _active_tenant
    _active_tenant = tenant_id
    stream = await open_stream(tenant_id)
    delivered = 0

    async for raw_line in stream:
        payload = json.loads(raw_line)
        if not isinstance(payload, dict) or "record_id" not in payload:
            raise ValueError("malformed stream record")

        for attempt in range(1, max_attempts + 1):
            request_key = f"{_active_tenant}:{uuid.uuid4()}"
            try:
                await forward_record(
                    tenant_id=_active_tenant,
                    idempotency_key=request_key,
                    record=payload,
                )
                delivered += 1
                break
            except TimeoutError:
                if attempt == max_attempts:
                    raise

    await stream.aclose()
    return delivered
