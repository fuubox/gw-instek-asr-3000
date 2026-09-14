from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("method", "value", "expected"),
    [
        ("sequence_clear", 2, b":DATA:TRACe:SEQuence:CLEar 2\n"),
        ("sequence_recall", 2, b":DATA:TRACe:SEQuence:RECall 2\n"),
        ("sequence_store", 2, b":DATA:TRACe:SEQuence:STORe 2\n"),
        ("simulation_clear", 2, b":DATA:TRACe:SIMulation:CLEar 2\n"),
        ("simulation_recall", 2, b":DATA:TRACe:SIMulation:RECall 2\n"),
        ("simulation_store", 2, b":DATA:TRACe:SIMulation:STORe 2\n"),
        ("wave_clear", 3, b":DATA:TRACe:WAVe:CLEar 3\n"),
        ("memory_recall", 4, b":MEMory:RCL 4\n"),
        ("memory_save", 4, b":MEMory:SAV 4\n"),
        ("current_peak_clear", None, b":MEASure:CURRent:PEAK:CLEar\n"),
        ("protection_clear", None, b":OUTPut:PROTection:CLEar\n"),
        ("design_mode", "SIMPle", b":DISPlay:DESign:MODE SIMPLE\n"),
        ("measure_source", "VRMS", b":DISPlay:MEASure:SOURce2 VRMS\n"),
        ("gain", 1.25, b":INPut:GAIN 1.25\n"),
        ("sensing", True, b":MEASure:CONFigure:SENSing ON\n"),
        ("average_count", 8, b":MEASure:AVERage:COUNt 8\n"),
        ("update_rate", "FAST", b":MEASure:UPDate:RATE FAST\n"),
    ],
)
def test_additional_write_contracts(instrument, transport, method, value, expected):
    if method == "measure_source":
        getattr(instrument, method)(2, value)
    elif value is None:
        getattr(instrument, method)()
    else:
        getattr(instrument, method)(value)
    assert transport.sent[-1] == expected


@pytest.mark.parametrize(
    ("method", "command"),
    [
        ("current_crest_factor", ":MEASure:CURRent:CFACtor?"),
        ("current_high", ":MEASure:CURRent:HIGH?"),
        ("current_low", ":MEASure:CURRent:LOW?"),
        ("current_peak_hold", ":MEASure:CURRent:PEAK:HOLD?"),
        ("current_average", ":MEASure:CURRent:AVERage?"),
        ("measure_frequency", ":MEASure:FREQuency?"),
        ("power_apparent", ":MEASure:POWer:APParent?"),
        ("power_factor", ":MEASure:POWer:PFACtor?"),
        ("power_reactive", ":MEASure:POWer:REACtive?"),
        ("voltage_average", ":MEASure:VOLTage:AVERage?"),
        ("voltage_high", ":MEASure:VOLTage:HIGH?"),
        ("voltage_low", ":MEASure:VOLTage:LOW?"),
    ],
)
def test_measure_query_contracts(instrument, transport, method, command):
    transport.queue_line("+1.25")
    assert getattr(instrument, method)() == 1.25
    assert transport.sent[-1] == (command + "\n").encode()
