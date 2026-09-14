"""Simulation mode commands (``[:SOURce]:SIMulation``)."""

from __future__ import annotations

from typing import Any

from .._types import SimulateAction, SimulationCondition, SimulationStep
from ..scpi import SCPIBase


class SimulateCommands(SCPIBase):
    """Simulation mode step parameters and execution control."""

    def _getset_num(self, cmd: str, value: Any = None) -> float | None:
        if value is None:
            return self.query_float(cmd + "?")
        self.write(f"{cmd} {self._num(value)}")
        return None

    def _getset_int(self, cmd: str, value: Any = None) -> int | None:
        if value is None:
            return self.query_int(cmd + "?")
        self.write(f"{cmd} {self._int(value)}")
        return None

    def _getset_bool(self, cmd: str, value: Any = None) -> bool | None:
        if value is None:
            return self.query_bool(cmd + "?")
        self.write(f"{cmd} {self._bool(value)}")
        return None

    def simulation_condition(self) -> SimulationCondition:
        """``[:SOURce]:SIMulation:CONDition?`` - simulation run status."""
        return self.query_enum(":SIMulation:CONDition?", SimulationCondition)

    # -- abnormal step -----------------------------------------------------

    def abnormal_code(self, value: Any = None) -> int | None:
        return self._getset_int(":SIMulation:ABNormal:CODE", value)

    def abnormal_frequency(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:ABNormal:FREQuency", value)

    def abnormal_start_phase_enable(self, value: Any = None) -> bool | None:
        return self._getset_bool(":SIMulation:ABNormal:PHASe:STARt:ENABle", value)

    def abnormal_start_phase(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:ABNormal:PHASe:STARt", value)

    def abnormal_stop_phase_enable(self, value: Any = None) -> bool | None:
        return self._getset_bool(":SIMulation:ABNormal:PHASe:STOP:ENABle", value)

    def abnormal_stop_phase(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:ABNormal:PHASe:STOP", value)

    def abnormal_time(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:ABNormal:TIME", value)

    def abnormal_voltage(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:ABNormal:VOLTage", value)

    # -- run status --------------------------------------------------------

    def simulation_current_step(self) -> SimulationStep:
        """``[:SOURce]:SIMulation:CSTep?`` - currently running step."""
        return self.query_enum(":SIMulation:CSTep?", SimulationStep)

    def current_repeat_count(self) -> list[str]:
        """``[:SOURce]:SIMulation:CREPeat:COUNt?`` - current step and repeat count."""
        return self.query_csv(":SIMulation:CREPeat:COUNt?")

    def simulation_current_time(self) -> list[int | None]:
        """``[:SOURce]:SIMulation:CTIMe?`` - current step and elapsed time."""
        return self.query_ints(":SIMulation:CTIMe?")

    # -- initial step ------------------------------------------------------

    def initial_code(self, value: Any = None) -> int | None:
        return self._getset_int(":SIMulation:INITial:CODE", value)

    def initial_frequency(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:INITial:FREQuency", value)

    def initial_start_phase_enable(self, value: Any = None) -> bool | None:
        return self._getset_bool(":SIMulation:INITial:PHASe:STARt:ENABle", value)

    def initial_start_phase(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:INITial:PHASe:STARt", value)

    def initial_stop_phase_enable(self, value: Any = None) -> bool | None:
        return self._getset_bool(":SIMulation:INITial:PHASe:STOP:ENABle", value)

    def initial_stop_phase(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:INITial:PHASe:STOP", value)

    def initial_voltage(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:INITial:VOLTage", value)

    # -- normal steps ------------------------------------------------------

    def normal_code(self, n: int, value: Any = None) -> int | None:
        return self._getset_int(f":SIMulation:NORMal{n}:CODE", value)

    def normal_frequency(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:NORMal1:FREQuency", value)

    def normal_start_phase_enable(self, n: int, value: Any = None) -> bool | None:
        return self._getset_bool(f":SIMulation:NORMal{n}:PHASe:STARt:ENABle", value)

    def normal_start_phase(self, n: int, value: Any = None) -> float | None:
        return self._getset_num(f":SIMulation:NORMal{n}:PHASe:STARt", value)

    def normal_stop_phase_enable(self, n: int, value: Any = None) -> bool | None:
        return self._getset_bool(f":SIMulation:NORMal{n}:PHASe:STOP:ENABle", value)

    def normal_stop_phase(self, n: int, value: Any = None) -> float | None:
        return self._getset_num(f":SIMulation:NORMal{n}:PHASe:STOP", value)

    def normal_time(self, n: int, value: Any = None) -> float | None:
        return self._getset_num(f":SIMulation:NORMal{n}:TIME", value)

    def normal_voltage(self, value: Any = None) -> float | None:
        return self._getset_num(":SIMulation:NORMal1:VOLTage", value)

    # -- repeat ------------------------------------------------------------

    def repeat_count(self, value: Any = None) -> int | None:
        return self._getset_int(":SIMulation:REPeat:COUNt", value)

    def repeat_enable(self, value: Any = None) -> bool | None:
        return self._getset_bool(":SIMulation:REPeat:ENABle", value)

    # -- transition steps --------------------------------------------------

    def transition_time(self, n: int, value: Any = None) -> float | None:
        return self._getset_num(f":SIMulation:TRANsition{n}:TIME", value)

    def transition_code(self, n: int, value: Any = None) -> int | None:
        return self._getset_int(f":SIMulation:TRANsition{n}:CODE", value)

    # -- execution ---------------------------------------------------------

    def simulation_execute(self, action: SimulateAction | str) -> None:
        """``:TRIGger:SIMulation:SELected:EXECute`` - start/stop/hold simulation."""
        self.write(f":TRIGger:SIMulation:SELected:EXECute {self._enum(action, SimulateAction)}")
