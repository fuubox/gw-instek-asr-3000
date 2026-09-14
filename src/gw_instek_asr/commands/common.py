"""IEEE 488.2 common commands."""

from __future__ import annotations

from .._types import Identification
from ..scpi import SCPIBase


class CommonCommands(SCPIBase):
    """IEEE 488.2 common commands (``*CLS``, ``*IDN?``, ...)."""

    def clear_status(self) -> None:
        """``*CLS`` - clear all event registers and the error queue."""
        self.write("*CLS")

    def standard_event_status_enable(self, value: int | None = None) -> int | None:
        """``*ESE`` - set or query the Standard Event Status Enable register (0-255)."""
        if value is None:
            return self.query_int("*ESE?")
        self.write(f"*ESE {self._int(value)}")
        return None

    def standard_event_status(self) -> int:
        """``*ESR?`` - query (and clear) the Standard Event Status register."""
        return self.query_int("*ESR?")

    def idn(self) -> str:
        """``*IDN?`` - return the raw identification string."""
        return self.query("*IDN?")

    def identify(self) -> Identification:
        """Return a parsed :class:`Identification` from ``*IDN?``."""
        parts = self.idn().split(",")
        if len(parts) != 4:
            return Identification(
                manufacturer=parts[0] if len(parts) > 0 else "",
                model=parts[1] if len(parts) > 1 else "",
                serial=parts[2] if len(parts) > 2 else "",
                firmware=parts[3] if len(parts) > 3 else "",
            )
        return Identification(*parts)

    def operation_complete(self) -> None:
        """``*OPC`` - set the OPC bit when all pending operations complete."""
        self.write("*OPC")

    def wait_for_completion(self) -> bool:
        """``*OPC?`` - block until pending operations complete and return ``True``."""
        return self.query_bool("*OPC?")

    def recall(self, slot: int | str) -> None:
        """``*RCL`` - recall settings from memory slot 0-9."""
        self.write(f"*RCL {self._int(slot)}")

    def reset(self) -> None:
        """``*RST`` - reset the instrument to factory default settings."""
        self.write("*RST")

    def save(self, slot: int | str) -> None:
        """``*SAV`` - save settings to memory slot 0-9."""
        self.write(f"*SAV {self._int(slot)}")

    def service_request_enable(self, value: int | None = None) -> int | None:
        """``*SRE`` - set or query the Service Request Enable register (0-255)."""
        if value is None:
            return self.query_int("*SRE?")
        self.write(f"*SRE {self._int(value)}")
        return None

    def status_byte(self) -> int:
        """``*STB?`` - query the Status Byte register."""
        return self.query_int("*STB?")

    def wait(self) -> None:
        """``*WAI`` - wait for all outstanding commands to complete."""
        self.write("*WAI")
