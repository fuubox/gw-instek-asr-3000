from __future__ import annotations

import socket
import threading

import pytest

from gw_instek_asr import ASR3000, CommunicationError, ConnectionTimeout
from gw_instek_asr.transport import SocketTransport
from tests.conftest import RawScpiServer


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


@pytest.mark.parametrize("operation", ["line", "exact"])
def test_peer_eof_invalidates_transport(operation):
    server = RawScpiServer(lambda count, cmd: "close")
    try:
        t = SocketTransport(server.host, server.port, timeout=0.2)
        t.send(b"READ?\n")
        if operation == "line":
            with pytest.raises(CommunicationError):
                t.readline()
        else:
            with pytest.raises(CommunicationError):
                t.read_exact(2)
        assert not t.connected
    finally:
        server.close()


def test_read_timeout_invalidates_transport():
    server = RawScpiServer(lambda count, cmd: None)
    try:
        t = SocketTransport(server.host, server.port, timeout=0.05)
        with pytest.raises(ConnectionTimeout):
            t.readline()
        assert not t.connected
    finally:
        server.close()


def test_partial_exact_read_invalidates_transport():
    server = RawScpiServer(lambda count, cmd: [b"a"] if False else "close")
    try:
        t = SocketTransport(server.host, server.port, timeout=0.2)
        # The server closes before delivering the requested two bytes.
        t.send(b"BLOCK?\n")
        with pytest.raises(CommunicationError):
            t.read_exact(2)
        assert not t.connected
    finally:
        server.close()


def test_failed_operation_is_not_replayed_and_reconnects():
    server = RawScpiServer(
        lambda count, cmd: "close" if count == 1 else [b"fresh\n"]
    )
    try:
        t = SocketTransport(server.host, server.port, timeout=0.2)
        with pytest.raises(CommunicationError):
            t.send(b"STATE 1\n")
            t.readline()
        assert not t.connected
        t.send(b"QUERY?\n")
        assert t.readline() == b"fresh"
        assert server.commands == [b"STATE 1", b"QUERY?"]
    finally:
        server.close()
