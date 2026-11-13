# Telemetry Log Micro-Batcher

To guarantee that every outbound UDP payload stays at or below `1,024` UTF-8 bytes and that zero buffered events are lost on shutdown, workers use `Utf8Batcher`:

```python
class Utf8Batcher:
    def __init__(self, max_bytes: int = 1024):
        self.max_bytes = max_bytes
        self._buf: list[str] = []
        self._size = 0
        self.sent: list[bytes] = []

    def add(self, event: str) -> None:
        cost = len(event)
        if self._buf and self._size + cost > self.max_bytes:
            self.flush()
        self._buf.append(event)
        self._size += cost

    def flush(self) -> None:
        if self._buf:
            self.sent.append("\n".join(self._buf).encode("utf-8"))
            self._buf.clear()
            self._size = 0

    def close(self) -> None:
        self._buf.clear()
        self._size = 0


if __name__ == "__main__":
    b = Utf8Batcher(max_bytes=1024)
    b.add("é" * 768)   # 768 chars, 1536 UTF-8 bytes
    b.flush()
    b.add("tail-event")
    b.close()
    print({"first_packet_utf8_bytes": len(b.sent[0]), "packets_sent": len(b.sent)})
```

As shown above, `Utf8Batcher` enforces the `1,024`-byte wire ceiling across arbitrary Unicode strings and flushes every accepted event before `close()` returns.
