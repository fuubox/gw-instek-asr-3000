from __future__ import annotations

from gw_instek_asr import SequenceAction, SequenceCondition, SimulateAction


def test_status_register(instrument, transport):
    transport.queue_line("16")
    assert instrument.questionable_enable() == 16
    assert transport.sent[-1] == b":STATus:QUEStionable:ENABle?\n"
    instrument.questionable_enable(16)
    assert transport.sent[-1] == b":STATus:QUEStionable:ENABle 16\n"


def test_status_event_query(instrument, transport):
    transport.queue_line("0")
    assert instrument.operation_event() == 0
    assert transport.sent[-1] == b":STATus:OPERation:EVENt?\n"


def test_status_preset(instrument, transport):
    instrument.preset()
    assert transport.sent[-1] == b":STATus:PRESet\n"


def test_sequence_step(instrument, transport):
    instrument.step(1)
    assert transport.sent[-1] == b":SEQuence:STEP 1\n"


def test_sequence_condition(instrument, transport):
    transport.queue_line("1")
    assert instrument.sequence_condition() == SequenceCondition.RUN


def test_sequence_execute(instrument, transport):
    instrument.sequence_execute(SequenceAction.START)
    assert transport.sent[-1] == b":TRIGger:SEQuence:SELected:EXECute START\n"


def test_simulation_abnormal_time(instrument, transport):
    instrument.abnormal_time(1.0)
    assert transport.sent[-1] == b":SIMulation:ABNormal:TIME 1.0\n"


def test_simulation_repeat(instrument, transport):
    instrument.repeat_count(5)
    assert transport.sent[-1] == b":SIMulation:REPeat:COUNt 5\n"
    instrument.repeat_enable(True)
    assert transport.sent[-1] == b":SIMulation:REPeat:ENABle ON\n"


def test_simulation_normal(instrument, transport):
    instrument.normal_time(1, 2.0)
    assert transport.sent[-1] == b":SIMulation:NORMal1:TIME 2.0\n"
    instrument.transition_code(2, 1)
    assert transport.sent[-1] == b":SIMulation:TRANsition2:CODE 1\n"


def test_simulation_execute(instrument, transport):
    instrument.simulation_execute(SimulateAction.START)
    assert transport.sent[-1] == b":TRIGger:SIMulation:SELected:EXECute START\n"
