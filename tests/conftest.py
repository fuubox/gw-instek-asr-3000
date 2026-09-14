from __future__ import annotations

import pytest

from gw_instek_asr import ASR3000


class FakeTransport:
    """In-memory transport for unit-testing command encoding."""

    def __init__(self) -> None:
        self.sent: list[bytes] = []
        self.closed = False
        self._lines: list[bytes] = []
        self._buf = b""

    def send(self, data: bytes) -> None:
        self.sent.append(data)

    def queue_line(self, line: str | bytes) -> None:
        self._lines.append(line.encode() if isinstance(line, str) else line)

    def queue_block(self, header: bytes, data: bytes) -> None:
        self._buf += header + data + b"\n"

    def readline(self) -> bytes:
        if self._lines:
            return self._lines.pop(0)
        return b""

    def read_exact(self, n: int) -> bytes:
        chunk, self._buf = self._buf[:n], self._buf[n:]
        return chunk

    def close(self) -> None:
        self.closed = True


@pytest.fixture
def transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def instrument(transport: FakeTransport) -> ASR3000:
    return ASR3000(transport=transport, connect=False)
