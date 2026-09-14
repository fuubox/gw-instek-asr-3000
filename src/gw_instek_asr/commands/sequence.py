"""Sequence mode commands (``[:SOURce]:SEQuence``)."""

from __future__ import annotations

from typing import Any

from .._types import SequenceAction, SequenceCondition
from ..scpi import SCPIBase


class SequenceCommands(SCPIBase):
    """Sequence mode parameters and execution control."""

    @staticmethod
    def _mix(value: Any) -> str:
        if isinstance(value, bool):
            return "ON" if value else "OFF"
        return str(value)

    def common_parameter(self, *values: Any) -> list[str] | None:
        """``[:SOURce]:SEQuence:CPARameter`` - sequence common parameters.

        With no arguments, queries the 15 common parameters (returned as raw
        tokens).  Otherwise sets them from the supplied values.
        """
        cmd = ":SEQuence:CPARameter"
        if not values:
            return self.query_csv(cmd + "?")
        self.write(cmd + " " + ",".join(self._mix(v) for v in values))
        return None

    def sequence_current_step(self) -> int | None:
        """``[:SOURce]:SEQuence:CSTep?`` - currently running step number."""
        return self.query_int(":SEQuence:CSTep?")

    def current_jump_count(self) -> list[str]:
        """``[:SOURce]:SEQuence:CJUMp:CNT?`` - current step and jump count."""
        return self.query_csv(":SEQuence:CJUMp:CNT?")

    def sequence_current_time(self) -> list[int | None]:
        """``[:SOURce]:SEQuence:CTIMe?`` - current step and elapsed time."""
        return self.query_ints(":SEQuence:CTIMe?")

    def step_parameter(self, *values: Any) -> list[str] | None:
        """``[:SOURce]:SEQuence:SPARameter`` - parameters for the selected step."""
        cmd = ":SEQuence:SPARameter"
        if not values:
            return self.query_csv(cmd + "?")
        self.write(cmd + " " + ",".join(self._mix(v) for v in values))
        return None

    def step(self, value: Any = None) -> int | None:
        """``[:SOURce]:SEQuence:STEP`` - current step number."""
        if value is None:
            return self.query_int(":SEQuence:STEP?")
        self.write(f":SEQuence:STEP {self._int(value)}")
        return None

    def sequence_condition(self) -> SequenceCondition:
        """``[:SOURce]:SEQuence:CONDition?`` - sequence run status."""
        return self.query_enum(":SEQuence:CONDition?", SequenceCondition)

    def sequence_execute(self, action: SequenceAction | str) -> None:
        """``:TRIGger:SEQuence:SELected:EXECute`` - start/stop/hold/branch."""
        self.write(f":TRIGger:SEQuence:SELected:EXECute {self._enum(action, SequenceAction)}")
