from __future__ import annotations

import socket
import threading

import pytest

from gw_instek_asr import ASR3000, CommunicationError
from gw_instek_asr.transport import SocketTransport


class _ScpiServer:
    def __init__(self, handler):
        self._handler = handler
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(1)
        self.host, self.port = self._sock.getsockname()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        conn, _ = self._sock.accept()
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
                conn.sendall(self._handler(line) + b"\n")

    def close(self):
        self._sock.close()


def test_end_to_end_idn():
    server = _ScpiServer(lambda cmd: b"GW-INSTEK,ASR-3300,G1234567,1.12")
    try:
        with SocketTransport(server.host, server.port, timeout=2.0) as t:
            t.send(b"*IDN?\n")
            assert t.readline() == b"GW-INSTEK,ASR-3300,G1234567,1.12"
    finally:
        server.close()


def test_instrument_over_socket():
    def handler(cmd: bytes) -> bytes:
        if cmd == b"*IDN?":
            return b"GW-INSTEK,ASR-3300,G1234567,1.12"
        if cmd == b":VOLTage?":
            return b"+230.0000"
        return b"0"

    server = _ScpiServer(handler)
    try:
        with ASR3000(server.host, server.port, timeout=2.0) as inst:
            assert inst.identify().model == "ASR-3300"
            assert inst.voltage() == 230.0
    finally:
        server.close()


def test_connection_refused():
    with pytest.raises(CommunicationError):
        ASR3000("127.0.0.1", 1, timeout=0.5)
