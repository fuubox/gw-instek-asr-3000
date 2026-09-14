from __future__ import annotations

from gw_instek_asr.commands.data import _make_block


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
