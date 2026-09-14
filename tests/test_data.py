from __future__ import annotations

import pytest

from gw_instek_asr import ASR3000, CommunicationError, ConnectionTimeout, QueryError
from gw_instek_asr.commands.data import _make_block
from tests.conftest import FakeTransport, RawScpiServer


def test_make_block():
    assert _make_block(b"abcd") == b"#14abcd"
    assert _make_block(b"x" * 8192).startswith(b"#48192")


def test_wave_data_download(instrument, transport):
    data = b"\x00\x01" * 4
    block = _make_block(data)
    transport.queue_block(block[:3], block[3:])
    assert instrument.wave_data(1) == data
    assert transport.sent[-1] == b":DATA:TRACe:WAVe? 1\n"


def test_wave_data_upload(instrument, transport):
    data = b"\x00\x01" * 4
    instrument.wave_data(1, data)
    payload = transport.sent[-1]
    assert payload.startswith(b":DATA:TRACe:WAVe 1,#18")
    assert payload.endswith(data + b"\n")


def test_sequence_memory(instrument, transport):
    instrument.sequence_store(2)
    assert transport.sent[-1] == b":DATA:TRACe:SEQuence:STORe 2\n"
    instrument.simulation_recall(0)
    assert transport.sent[-1] == b":DATA:TRACe:SIMulation:RECall 0\n"


def test_wave_clear(instrument, transport):
    instrument.wave_clear(13)
    assert transport.sent[-1] == b":DATA:TRACe:WAVe:CLEar 13\n"


def _socket_wave(response, calls=1):
    server = RawScpiServer(lambda count, cmd: response[count - 1] if calls > 1 else response)
    try:
        with ASR3000(server.host, server.port, timeout=0.2) as inst:
            result = [inst.wave_data(1) for _ in range(calls)]
        return result
    finally:
        server.close()


def test_socket_fragmented_block_and_lf():
    block = _make_block(b"abcd") + b"\n"
    assert _socket_wave([block[:2], block[2:]], calls=1) == [b"abcd"]


def test_socket_crlf_block():
    assert _socket_wave([b"#14abcd\r\n"], calls=1) == [b"abcd"]


def test_socket_missing_block_terminator_times_out_and_invalidates():
    server = RawScpiServer(lambda count, cmd: [b"#14abcd"])
    try:
        inst = ASR3000(server.host, server.port, timeout=0.05)
        with pytest.raises(ConnectionTimeout):
            inst.wave_data(1)
        assert not inst._transport.connected
    finally:
        server.close()


@pytest.mark.parametrize(
    "frame",
    [
        b"x14abcd\n",
        b"#x4abcd\n",
        b"#1xabcd\n",
        b"#04\n",
        b"#49999\n",
        b"#14ab\n",
    ],
)
def test_socket_malformed_block_is_query_error(frame):
    with pytest.raises((QueryError, CommunicationError)) as exc:
        _socket_wave([frame], calls=1)
    if frame != b"#14ab\n":
        assert isinstance(exc.value, QueryError)


def test_socket_truncated_payload_is_transport_error():
    with pytest.raises(CommunicationError):
        _socket_wave([b"#14ab\n"], calls=1)


def test_socket_consecutive_blocks_remain_aligned():
    assert _socket_wave([b"#14one!\n", b"#14two!\n"], calls=2) == [b"one!", b"two!"]


def test_socket_binary_framing_error_invalidates_before_reconnect():
    server = RawScpiServer(lambda count, cmd: [b"xstale\n"] if count == 1 else [b"#15fresh\n"])
    try:
        with ASR3000(server.host, server.port, timeout=0.2) as inst:
            with pytest.raises(QueryError, match="expected binary block header"):
                inst.wave_data(1)
            assert not inst._transport.connected
            assert inst.wave_data(1) == b"fresh"
    finally:
        server.close()


@pytest.mark.parametrize("frame", [b"x14abcd\n", b"#x4abcd\n", b"#1xabcd\n", b"#04\n", b"#49999\n", b"#14abcdX"])
def test_binary_framing_errors_close_transport(frame):
    transport = FakeTransport()
    transport._buf = frame
    inst = ASR3000(transport=transport, connect=False)

    with pytest.raises(QueryError):
        inst.wave_data(1)
    assert transport.closed
