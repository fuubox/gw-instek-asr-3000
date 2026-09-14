from __future__ import annotations

import pytest

from gw_instek_asr import SimulationCondition


@pytest.mark.parametrize(
    ("call", "expected"),
    [
        (lambda i: i.abnormal_code(7), b":SIMulation:ABNormal:CODE 7\n"),
        (lambda i: i.abnormal_frequency(60), b":SIMulation:ABNormal:FREQuency 60.0\n"),
        (
            lambda i: i.abnormal_start_phase_enable(True),
            b":SIMulation:ABNormal:PHASe:STARt:ENABle ON\n",
        ),
        (lambda i: i.abnormal_start_phase(12.5), b":SIMulation:ABNormal:PHASe:STARt 12.5\n"),
        (
            lambda i: i.abnormal_stop_phase_enable(False),
            b":SIMulation:ABNormal:PHASe:STOP:ENABle OFF\n",
        ),
        (lambda i: i.abnormal_stop_phase(180), b":SIMulation:ABNormal:PHASe:STOP 180.0\n"),
        (lambda i: i.abnormal_voltage(230), b":SIMulation:ABNormal:VOLTage 230.0\n"),
        (lambda i: i.initial_code(1), b":SIMulation:INITial:CODE 1\n"),
        (lambda i: i.initial_frequency(50), b":SIMulation:INITial:FREQuency 50.0\n"),
        (lambda i: i.initial_start_phase_enable(1), b":SIMulation:INITial:PHASe:STARt:ENABle ON\n"),
        (lambda i: i.initial_stop_phase_enable(0), b":SIMulation:INITial:PHASe:STOP:ENABle OFF\n"),
        (lambda i: i.initial_voltage(120), b":SIMulation:INITial:VOLTage 120.0\n"),
        (lambda i: i.normal_code(1, 4), b":SIMulation:NORMal1:CODE 4\n"),
        (
            lambda i: i.normal_start_phase_enable(2, False),
            b":SIMulation:NORMal2:PHASe:STARt:ENABle OFF\n",
        ),
        (lambda i: i.normal_start_phase(2, 10), b":SIMulation:NORMal2:PHASe:STARt 10.0\n"),
        (
            lambda i: i.normal_stop_phase_enable(2, True),
            b":SIMulation:NORMal2:PHASe:STOP:ENABle ON\n",
        ),
        (lambda i: i.normal_stop_phase(2, 20), b":SIMulation:NORMal2:PHASe:STOP 20.0\n"),
        (lambda i: i.normal_time(2, 3.5), b":SIMulation:NORMal2:TIME 3.5\n"),
        (lambda i: i.repeat_count(5), b":SIMulation:REPeat:COUNt 5\n"),
        (lambda i: i.repeat_enable(True), b":SIMulation:REPeat:ENABle ON\n"),
        (lambda i: i.transition_time(1, 2), b":SIMulation:TRANsition1:TIME 2.0\n"),
        (lambda i: i.transition_code(2, 9), b":SIMulation:TRANsition2:CODE 9\n"),
    ],
)
def test_simulation_setter_contracts(instrument, transport, call, expected):
    call(instrument)
    assert transport.sent[-1] == expected


def test_simulation_query_contracts(instrument, transport):
    transport.queue_line("1")
    assert instrument.simulation_condition() is SimulationCondition.RUN
    assert transport.sent[-1] == b":SIMulation:CONDition?\n"

    transport.queue_line("1,2,3")
    assert instrument.simulation_current_time() == [1, 2, 3]
    assert transport.sent[-1] == b":SIMulation:CTIMe?\n"


def test_sequence_compound_contracts(instrument, transport):
    instrument.common_parameter(1, True, "MAX")
    assert transport.sent[-1] == b":SEQuence:CPARameter 1,ON,MAX\n"
    transport.queue_line("1,ON,MAX")
    assert instrument.common_parameter() == ["1", "ON", "MAX"]
    assert transport.sent[-1] == b":SEQuence:CPARameter?\n"

    instrument.step_parameter(2, False, "MIN")
    assert transport.sent[-1] == b":SEQuence:SPARameter 2,OFF,MIN\n"


@pytest.mark.parametrize(
    "method,command",
    [
        ("operation_condition", ":STATus:OPERation:CONDition?"),
        ("operation_event", ":STATus:OPERation:EVENt?"),
        ("questionable_condition", ":STATus:QUEStionable:CONDition?"),
        ("questionable_event", ":STATus:QUEStionable:EVENt?"),
        ("warning_condition", ":STATus:WARNing:CONDition?"),
        ("warning_event", ":STATus:WARNing:EVENt?"),
        ("lock_condition", ":STATus:LOCK:CONDition?"),
        ("lock_event", ":STATus:LOCK:EVENt?"),
    ],
)
def test_status_query_contracts(instrument, transport, method, command):
    transport.queue_line("16")
    assert getattr(instrument, method)() == 16
    assert transport.sent[-1] == (command + "\n").encode()
