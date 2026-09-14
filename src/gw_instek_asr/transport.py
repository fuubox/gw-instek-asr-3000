"""Transport layer for the ASR-3000 (raw TCP SCPI socket)."""

from __future__ import annotations

import socket
from typing import BinaryIO, Protocol

from .errors import CommunicationError, ConnectionTimeout

DEFAULT_PORT = 2268
DEFAULT_TIMEOUT = 10.0
DEFAULT_TERMINATOR = b"\n"


class Transport(Protocol):
    """Minimal byte-oriented transport contract used by the SCPI layer."""

    def send(self, data: bytes) -> None: ...

    def readline(self) -> bytes: ...

    def read_exact(self, n: int) -> bytes: ...

    def close(self) -> None: ...


class SocketTransport:
    """Raw TCP socket transport speaking SCPI with an LF terminator.

    The ASR-3000 exposes a socket server on TCP port **2268** (fixed).  Each
    command/response is terminated with a line-feed (``\\n``).
    """

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
        terminator: bytes = DEFAULT_TERMINATOR,
    ) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout
        self._terminator = terminator
        self._sock: socket.socket | None = None
        self._rfile: BinaryIO | None = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def connected(self) -> bool:
        return self._sock is not None

    def connect(self) -> None:
        """Open the TCP connection to the instrument."""
        if self._sock is not None:
            return
        try:
            self._sock = socket.create_connection((self._host, self._port), timeout=self._timeout)
            self._sock.settimeout(self._timeout)
            self._rfile = self._sock.makefile("rb")
        except (socket.timeout, TimeoutError) as exc:
            self.close()
            raise ConnectionTimeout(f"timed out connecting to {self._host}:{self._port}") from exc
        except OSError as exc:
            self.close()
            raise CommunicationError(f"failed to connect to {self._host}:{self._port}: {exc}") from exc

    def send(self, data: bytes) -> None:
        """Send raw bytes to the instrument."""
        self._ensure_connected()
        assert self._sock is not None
        try:
            self._sock.sendall(data)
        except (socket.timeout, TimeoutError) as exc:
            self.close()
            raise ConnectionTimeout("timed out writing to instrument") from exc
        except OSError as exc:
            self.close()
            raise CommunicationError(f"write failed: {exc}") from exc

    def readline(self) -> bytes:
        """Read a single response line (terminator stripped)."""
        self._ensure_connected()
        assert self._rfile is not None
        try:
            line = self._rfile.readline()
        except (socket.timeout, TimeoutError) as exc:
            self.close()
            raise ConnectionTimeout("timed out reading from instrument") from exc
        except OSError as exc:
            self.close()
            raise CommunicationError(f"read failed: {exc}") from exc
        if not line:
            self.close()
            raise CommunicationError("connection closed by instrument")
        return line.rstrip(b"\r\n")

    def read_exact(self, n: int) -> bytes:
        """Read exactly ``n`` bytes from the instrument."""
        self._ensure_connected()
        assert self._rfile is not None
        if n <= 0:
            return b""
        try:
            data = self._rfile.read(n)
        except (socket.timeout, TimeoutError) as exc:
            self.close()
            raise ConnectionTimeout("timed out reading from instrument") from exc
        except OSError as exc:
            self.close()
            raise CommunicationError(f"read failed: {exc}") from exc
        if data is None or len(data) < n:
            self.close()
            raise CommunicationError("connection closed while reading block data")
        return data

    def close(self) -> None:
        """Close the connection (idempotent)."""
        rfile, self._rfile = self._rfile, None
        sock, self._sock = self._sock, None
        if rfile is not None:
            try:
                rfile.close()
            except OSError:
                pass
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass

    def _ensure_connected(self) -> None:
        if self._sock is None:
            self.connect()

    def __enter__(self) -> "SocketTransport":
        self.connect()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
