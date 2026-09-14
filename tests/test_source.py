from __future__ import annotations

import pytest

from gw_instek_asr import OutputMode, QueryError, VoltageRange, Waveform


def test_voltage_set(instrument, transport):
    instrument.voltage(150.0)
    assert transport.sent[-1] == b":VOLTage 150.0\n"


def test_voltage_query(instrument, transport):
    transport.queue_line("+150.0000")
    assert instrument.voltage() == 150.0
    assert transport.sent[-1] == b":VOLTage?\n"


def test_frequency_set(instrument, transport):
    instrument.frequency(60)
    assert transport.sent[-1] == b":FREQuency 60.0\n"


def test_mode_set(instrument, transport):
    instrument.mode(OutputMode.ACDC_INT)
    assert transport.sent[-1] == b":MODE 0\n"
    instrument.mode("DC-INT")
    assert transport.sent[-1] == b":MODE 2\n"


def test_mode_query(instrument, transport):
    transport.queue_line("ACDC-INT")
    assert instrument.mode() == OutputMode.ACDC_INT


def test_waveform_set(instrument, transport):
    instrument.waveform(Waveform.SIN)
    assert transport.sent[-1] == b":FUNCtion 16\n"
    instrument.waveform("TRI")
    assert transport.sent[-1] == b":FUNCtion 18\n"


def test_waveform_query(instrument, transport):
    transport.queue_line("TRI")
    assert instrument.waveform() == Waveform.TRI


def test_voltage_range(instrument, transport):
    instrument.voltage_range("AUTO")
    assert transport.sent[-1] == b":VOLTage:RANGe 2\n"
    transport.queue_line("200")
    assert instrument.voltage_range() == VoltageRange.RANGE_200


def test_read_parses_17_fields(instrument, transport):
    transport.queue_line(
        "+0.3204,+0.0306,+0.1879,-0.5809,+0.0121,-0.0007,+0.0030,-0.0060,"
        "-0.0201,+0.0013,+0.0039,+0.0037,+0.3400,+1.1500,Invalid,Invalid,Invalid"
    )
    r = instrument.read()
    assert r.vrms == 0.3204
    assert r.ipk_hold == -0.0201
    assert r.power_factor == 0.34
    assert r.thd_v is None
    assert r.thd_i is None
    assert r.frequency is None


@pytest.mark.parametrize("reply", ["1,2,3", ",".join(["1"] * 18)])
def test_read_rejects_wrong_field_count(instrument, transport, reply):
    transport.queue_line(reply)
    with pytest.raises(QueryError, match=r":READ\? expected 17 fields"):
        instrument.read()


def test_read_rejects_malformed_numeric_token(instrument, transport):
    transport.queue_line(",".join(["1"] * 16 + ["oops"]))
    with pytest.raises(QueryError, match=r":READ\? invalid numeric token at field 17"):
        instrument.read()


def test_read_rejects_empty_response(instrument, transport):
    transport.queue_line("")
    with pytest.raises(QueryError, match=r":READ\? expected 17 fields"):
        instrument.read()


def test_current_limit(instrument, transport):
    instrument.current_limit_rms(10.5)
    assert transport.sent[-1] == b":CURRent:LIMit:RMS 10.5\n"
    transport.queue_line("+10.5000")
    assert instrument.current_limit_rms() == 10.5
