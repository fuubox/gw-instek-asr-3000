from __future__ import annotations

from gw_instek_asr import Identification


def test_idn(instrument, transport):
    transport.queue_line("GW-INSTEK,ASR-3300,G1234567,1.12")
    assert instrument.idn() == "GW-INSTEK,ASR-3300,G1234567,1.12"
    assert transport.sent[-1] == b"*IDN?\n"


def test_identify(instrument, transport):
    transport.queue_line("GW-INSTEK,ASR-3300,G1234567,1.12")
    ident = instrument.identify()
    assert isinstance(ident, Identification)
    assert ident.manufacturer == "GW-INSTEK"
    assert ident.model == "ASR-3300"
    assert ident.serial == "G1234567"
    assert ident.firmware == "1.12"


def test_reset(instrument, transport):
    instrument.reset()
    assert transport.sent[-1] == b"*RST\n"


def test_clear_status(instrument, transport):
    instrument.clear_status()
    assert transport.sent[-1] == b"*CLS\n"


def test_operation_complete_query(instrument, transport):
    transport.queue_line("1")
    assert instrument.wait_for_completion() is True
    assert transport.sent[-1] == b"*OPC?\n"


def test_save_recall(instrument, transport):
    instrument.save(3)
    assert transport.sent[-1] == b"*SAV 3\n"
    instrument.recall(3)
    assert transport.sent[-1] == b"*RCL 3\n"


def test_service_request_enable(instrument, transport):
    transport.queue_line("32")
    assert instrument.service_request_enable() == 32
    assert transport.sent[-1] == b"*SRE?\n"
    instrument.service_request_enable(48)
    assert transport.sent[-1] == b"*SRE 48\n"
