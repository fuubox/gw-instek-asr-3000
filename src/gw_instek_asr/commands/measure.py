"""Measure subsystem commands (``:MEASure``)."""

from __future__ import annotations

from typing import Any

from .._types import parse_float
from ..scpi import SCPIBase


class MeasureCommands(SCPIBase):
    """Measurement readbacks: current, voltage, power, harmonics."""

    # -- current -----------------------------------------------------------

    def current_crest_factor(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent:CFACtor?`` - output current crest factor."""
        return self.query_float(":MEASure:CURRent:CFACtor?")

    def current_high(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent:HIGH?`` - current maximum peak (Imax)."""
        return self.query_float(":MEASure:CURRent:HIGH?")

    def current_low(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent:LOW?`` - current minimum (Imin)."""
        return self.query_float(":MEASure:CURRent:LOW?")

    def current_peak_clear(self) -> None:
        """``:MEASure[:SCALar]:CURRent:PEAK:CLEar`` - clear peak-hold value."""
        self.write(":MEASure:CURRent:PEAK:CLEar")

    def current_peak_hold(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent:PEAK:HOLD?`` - current peak hold (IPK-Hold)."""
        return self.query_float(":MEASure:CURRent:PEAK:HOLD?")

    def current_rms(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent[:RMS]?`` - output current (Irms)."""
        return self.query_float(":MEASure:CURRent?")

    def current_average(self) -> float | None:
        """``:MEASure[:SCALar]:CURRent:AVERage?`` - current average (Iavg)."""
        return self.query_float(":MEASure:CURRent:AVERage?")

    def current_harmonic_rms(self) -> list[float | None]:
        """``:MEASure[:SCALar]:CURRent:HARMonic[:RMS]?`` - 41 harmonic current values."""
        return self.query_floats(":MEASure:CURRent:HARMonic?")

    def current_harmonic_ratio(self) -> list[float | None]:
        """``:MEASure[:SCALar]:CURRent:HARMonic:RATio?`` - 41 harmonic current ratios."""
        return self.query_floats(":MEASure:CURRent:HARMonic:RATio?")

    # -- frequency ---------------------------------------------------------

    def measure_frequency(self) -> float | None:
        """``:MEASure[:SCALar]:FREQuency?`` - SYNC signal frequency (Hz)."""
        return self.query_float(":MEASure:FREQuency?")

    # -- power -------------------------------------------------------------

    def power_apparent(self) -> float | None:
        """``:MEASure[:SCALar]:POWer[:AC]:APParent?`` - apparent power (VA)."""
        return self.query_float(":MEASure:POWer:APParent?")

    def power_factor(self) -> float | None:
        """``:MEASure[:SCALar]:POWer[:AC]:PFACtor?`` - power factor."""
        return self.query_float(":MEASure:POWer:PFACtor?")

    def power_reactive(self) -> float | None:
        """``:MEASure[:SCALar]:POWer[:AC]:REACtive?`` - reactive power (VAR)."""
        return self.query_float(":MEASure:POWer:REACtive?")

    def power_real(self) -> float | None:
        """``:MEASure[:SCALar]:POWer[:AC][:REAL]?`` - active power (W)."""
        return self.query_float(":MEASure:POWer?")

    # -- voltage -----------------------------------------------------------

    def voltage_rms(self) -> float | None:
        """``:MEASure[:SCALar]:VOLTage[:RMS]?`` - output voltage (Vrms)."""
        return self.query_float(":MEASure:VOLTage?")

    def voltage_average(self) -> float | None:
        """``:MEASure[:SCALar]:VOLTage:AVERage?`` - voltage average (Vavg)."""
        return self.query_float(":MEASure:VOLTage:AVERage?")

    def voltage_high(self) -> float | None:
        """``:MEASure[:SCALar]:VOLTage:HIGH?`` - voltage maximum peak (Vmax)."""
        return self.query_float(":MEASure:VOLTage:HIGH?")

    def voltage_low(self) -> float | None:
        """``:MEASure[:SCALar]:VOLTage:LOW?`` - voltage minimum (Vmin)."""
        return self.query_float(":MEASure:VOLTage:LOW?")

    def voltage_harmonic_rms(self) -> list[float | None]:
        """``:MEASure[:SCALar]:VOLTage:HARMonic[:RMS]?`` - 41 harmonic voltage values."""
        return self.query_floats(":MEASure:VOLTage:HARMonic?")

    def voltage_harmonic_ratio(self) -> list[float | None]:
        """``:MEASure[:SCALar]:VOLTage:HARMonic:RATio?`` - 41 harmonic voltage ratios."""
        return self.query_floats(":MEASure:VOLTage:HARMonic:RATio?")

    # -- configuration -----------------------------------------------------

    def sensing(self, value: Any = None) -> bool | None:
        """``:MEASure:CONFigure:SENSing`` - set or query remote sense."""
        if value is None:
            return self.query_bool(":MEASure:CONFigure:SENSing?")
        self.write(f":MEASure:CONFigure:SENSing {self._bool(value)}")
        return None

    def average_count(self, value: Any = None) -> int | None:
        """``:MEASure:AVERage:COUNt`` - averaging count (1-128)."""
        if value is None:
            return self.query_int(":MEASure:AVERage:COUNt?")
        self.write(f":MEASure:AVERage:COUNt {self._int(value)}")
        return None

    def update_rate(self, value: Any = None) -> float | str | None:
        """``:MEASure:UPDate:RATE`` - data update interval, or ``"FAST"``."""
        if value is None:
            raw = self.query(":MEASure:UPDate:RATE?")
            parsed = parse_float(raw)
            return parsed if parsed is not None else raw
        if isinstance(value, str) and value.strip().upper() == "FAST":
            self.write(":MEASure:UPDate:RATE FAST")
        else:
            self.write(f":MEASure:UPDate:RATE {self._num(value)}")
        return None
