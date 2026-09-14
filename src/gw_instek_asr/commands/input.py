"""Input subsystem commands (``:INPut``)."""

from __future__ import annotations

from typing import Any

from .._types import SyncSource
from ..scpi import SCPIBase


class InputCommands(SCPIBase):
    """Input gain and sync-source configuration."""

    def gain(self, value: Any = None) -> float | None:
        """``:INPut:GAIN`` - set or query the input gain value."""
        if value is None:
            return self.query_float(":INPut:GAIN?")
        self.write(f":INPut:GAIN {self._num(value)}")
        return None

    def sync_source(self, value: SyncSource | int | str | None = None) -> SyncSource | None:
        """``:INPut:SYNC:SOURce`` - set or query the sync source (``LINE``/``EXT``)."""
        if value is None:
            return self.query_enum(":INPut:SYNC:SOURce?", SyncSource)
        self.write(f":INPut:SYNC:SOURce {self._enum(value, SyncSource)}")
        return None
