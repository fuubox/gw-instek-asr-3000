from __future__ import annotations

import pytest

from gw_instek_asr import InvalidValueError, PowerOnState


def test_output_state(instrument, transport):
    instrument.output_state(True)
    assert transport.sent[-1] == b":OUTPut:STATe ON\n"
    transport.queue_line("+1")
    assert instrument.output_state() is True


def test_output_state_rejects_invalid_without_sending(instrument, transport):
    sent_before = list(transport.sent)
    with pytest.raises(InvalidValueError):
        instrument.output_state("OF")
    assert transport.sent == sent_before


def test_output_relay_rejects_invalid_without_sending(instrument, transport):
    with pytest.raises(InvalidValueError):
        instrument.output_relay("maybe")
    assert transport.sent == []


def test_output_helpers(instrument, transport):
    instrument.output_on()
    assert transport.sent[-1] == b":OUTPut:STATe ON\n"
    instrument.output_off()
    assert transport.sent[-1] == b":OUTPut:STATe OFF\n"


def test_power_on_state(instrument, transport):
    instrument.power_on_state(PowerOnState.SEQ)
    assert transport.sent[-1] == b":OUTPut:PON 2\n"
    transport.queue_line("0")
    assert instrument.power_on_state() == PowerOnState.OFF


def test_measure_voltage(instrument, transport):
    transport.queue_line("+230.0000")
    assert instrument.voltage_rms() == 230.0
    assert transport.sent[-1] == b":MEASure:VOLTage?\n"


def test_measure_power(instrument, transport):
    transport.queue_line("+1500.0000")
    assert instrument.power_real() == 1500.0
    assert transport.sent[-1] == b":MEASure:POWer?\n"


def test_measure_harmonic(instrument, transport):
    transport.queue_line(",".join(["1.0"] * 41))
    values = instrument.voltage_harmonic_rms()
    assert len(values) == 41
    assert values[0] == 1.0
