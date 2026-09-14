"""Output subsystem commands (``:OUTPut``)."""

from __future__ import annotations

from typing import Any

from .._types import PowerOnState
from ..scpi import SCPIBase


class OutputCommands(SCPIBase):
    """Output control: state, power-on behaviour, relay, and protection."""

    def output_state(self, value: Any = None) -> bool | None:
        """``:OUTPut[:STATe]`` - set or query the output state (``ON``/``OFF``)."""
        if value is None:
            return self.query_bool(":OUTPut:STATe?")
        self.write(f":OUTPut:STATe {self._bool(value)}")
        return None

    def output_on(self) -> None:
        """Turn the output on."""
        self.write(":OUTPut:STATe ON")

    def output_off(self) -> None:
        """Turn the output off."""
        self.write(":OUTPut:STATe OFF")

    def power_on_state(self, value: PowerOnState | int | str | None = None) -> PowerOnState | None:
        """``:OUTPut:PON`` - set or query the power-on output state."""
        if value is None:
            return self.query_enum(":OUTPut:PON?", PowerOnState)
        self.write(f":OUTPut:PON {self._enum(value, PowerOnState)}")
        return None

    def protection_clear(self) -> None:
        """``:OUTPut:PROTection:CLEar`` - clear protection alarms."""
        self.write(":OUTPut:PROTection:CLEar")

    def output_relay(self, value: Any = None) -> bool | None:
        """``:OUTPut:RELay`` - set or query the output relay state."""
        if value is None:
            return self.query_bool(":OUTPut:RELay?")
        self.write(f":OUTPut:RELay {self._bool(value)}")
        return None
