from __future__ import annotations

import socket
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


class RawScpiServer:
    """Socket fixture that sends response chunks exactly as supplied."""

    def __init__(self, responses):
        import threading

        self._responses = responses
        self.commands: list[bytes] = []
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(5)
        self.host, self.port = self._sock.getsockname()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while True:
            try:
                conn, _ = self._sock.accept()
            except OSError:
                return
            with conn:
                buf = b""
                while True:
                    try:
                        chunk = conn.recv(4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    buf += chunk
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        self.commands.append(line)
                        response = self._responses(len(self.commands), line)
                        if response == "close":
                            conn.shutdown(socket.SHUT_RDWR)
                            break
                        close_after = isinstance(response, tuple) and response[0] == "close_after"
                        if close_after:
                            response = response[1]
                        if response is None:
                            continue
                        if isinstance(response, bytes):
                            response = [response]
                        for chunk in response:
                            conn.sendall(chunk)
                        if close_after:
                            conn.shutdown(socket.SHUT_RDWR)
                            break

    def close(self):
        self._sock.close()


@pytest.fixture
def transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def instrument(transport: FakeTransport) -> ASR3000:
    return ASR3000(transport=transport, connect=False)
