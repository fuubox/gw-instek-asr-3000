"""Display commands (``:DISPlay``)."""

from __future__ import annotations

from .._types import DisplayMode, MeasureSource
from ..scpi import SCPIBase


class DisplayCommands(SCPIBase):
    """Front-panel display configuration."""

    def design_mode(self, value: DisplayMode | str | None = None) -> None:
        """``:DISPlay[:WINDow]:DESign:MODE`` - set the display mode (``NORMal``/``SIMPle``)."""
        if value is not None:
            self.write(f":DISPlay:DESign:MODE {self._enum(value, DisplayMode)}")

    def measure_source(self, item: int, value: MeasureSource | str | None = None) -> None:
        """``:DISPlay[:WINDow]:MEASure:SOURce<1|2|3>`` - set a measurement display item.

        ``item`` is 1, 2, or 3.
        """
        if value is not None:
            self.write(f":DISPlay:MEASure:SOURce{item} {self._enum(value, MeasureSource)}")
