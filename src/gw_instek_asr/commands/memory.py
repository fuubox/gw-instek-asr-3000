"""Memory commands (``:MEMory``)."""

from __future__ import annotations

from ..scpi import SCPIBase


class MemoryCommands(SCPIBase):
    """Preset memory slots (equivalent to ``*RCL``/``*SAV``)."""

    def memory_recall(self, slot: int | str) -> None:
        """``:MEMory:RCL`` - recall settings from memory slot 0-9."""
        self.write(f":MEMory:RCL {self._int(slot)}")

    def memory_save(self, slot: int | str) -> None:
        """``:MEMory:SAV`` - save settings to memory slot 0-9."""
        self.write(f":MEMory:SAV {self._int(slot)}")
