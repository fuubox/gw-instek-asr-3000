"""Source subsystem commands (``[:SOURce]``)."""

from __future__ import annotations

from typing import Any

from .._types import (
    OutputMode,
    PhaseState,
    Readings,
    THDFormat,
    VoltageRange,
    Waveform,
    parse_float,
)
from ..scpi import SCPIBase
from ..errors import QueryError

_READ_FIELDS = (
    "vrms",
    "vavg",
    "vmax",
    "vmin",
    "irms",
    "iavg",
    "imax",
    "imin",
    "ipk_hold",
    "power_real",
    "power_apparent",
    "power_reactive",
    "power_factor",
    "crest_factor",
    "thd_v",
    "thd_i",
    "frequency",
)


class SourceCommands(SCPIBase):
    """Source configuration: limits, frequency, waveform, mode, phase, voltage."""

    # -- current limits ----------------------------------------------------

    def current_limit_peak_high(self, value: Any = None) -> float | None:
        """``[:SOURce]:CURRent:LIMit:PEAK:HIGH`` - Ipk-high limit (Arms)."""
        if value is None:
            return self.query_float(":CURRent:LIMit:PEAK:HIGH?")
        self.write(f":CURRent:LIMit:PEAK:HIGH {self._num(value)}")
        return None

    def current_limit_peak_low(self, value: Any = None) -> float | None:
        """``[:SOURce]:CURRent:LIMit:PEAK:LOW`` - Ipk-low limit (Arms)."""
        if value is None:
            return self.query_float(":CURRent:LIMit:PEAK:LOW?")
        self.write(f":CURRent:LIMit:PEAK:LOW {self._num(value)}")
        return None

    def current_limit_rms(self, value: Any = None) -> float | None:
        """``[:SOURce]:CURRent:LIMit:RMS`` - Irms limit (A)."""
        if value is None:
            return self.query_float(":CURRent:LIMit:RMS?")
        self.write(f":CURRent:LIMit:RMS {self._num(value)}")
        return None

    def current_limit_peak_mode(self, value: Any = None) -> bool | None:
        """``[:SOURce]:CURRent:LIMit:PEAK:MODE`` - enable/disable Ipk limiting."""
        if value is None:
            return self.query_bool(":CURRent:LIMit:PEAK:MODE?")
        self.write(f":CURRent:LIMit:PEAK:MODE {self._bool(value)}")
        return None

    def current_limit_rms_mode(self, value: Any = None) -> bool | None:
        """``[:SOURce]:CURRent:LIMit:RMS:MODE`` - enable/disable Irms limiting."""
        if value is None:
            return self.query_bool(":CURRent:LIMit:RMS:MODE?")
        self.write(f":CURRent:LIMit:RMS:MODE {self._bool(value)}")
        return None

    # -- frequency ---------------------------------------------------------

    def frequency_limit_high(self, value: Any = None) -> float | None:
        """``[:SOURce]:FREQuency:LIMit:HIGH`` - frequency upper limit (Hz)."""
        if value is None:
            return self.query_float(":FREQuency:LIMit:HIGH?")
        self.write(f":FREQuency:LIMit:HIGH {self._num(value)}")
        return None

    def frequency_limit_low(self, value: Any = None) -> float | None:
        """``[:SOURce]:FREQuency:LIMit:LOW`` - frequency lower limit (Hz)."""
        if value is None:
            return self.query_float(":FREQuency:LIMit:LOW?")
        self.write(f":FREQuency:LIMit:LOW {self._num(value)}")
        return None

    def frequency(self, value: Any = None) -> float | None:
        """``[:SOURce]:FREQuency[:IMMediate]`` - output frequency (Hz)."""
        if value is None:
            return self.query_float(":FREQuency?")
        self.write(f":FREQuency {self._num(value)}")
        return None

    # -- waveform ----------------------------------------------------------

    def waveform(self, value: Waveform | int | str | None = None) -> Waveform | None:
        """``[:SOURce]:FUNCtion[:SHAPe][:IMMediate]`` - output waveform."""
        if value is None:
            return self.query_enum(":FUNCtion?", Waveform)
        self.write(f":FUNCtion {self._enum(value, Waveform)}")
        return None

    def thd_format(self, value: THDFormat | int | str | None = None) -> THDFormat | None:
        """``[:SOURce]:FUNCtion:THD:FORMat`` - THD calculation standard (``IEC``/``CSA``)."""
        if value is None:
            return self.query_enum(":FUNCtion:THD:FORMat?", THDFormat)
        self.write(f":FUNCtion:THD:FORMat {self._enum(value, THDFormat)}")
        return None

    # -- mode --------------------------------------------------------------

    def mode(self, value: OutputMode | int | str | None = None) -> OutputMode | None:
        """``[:SOURce]:MODE`` - output mode (e.g. ``ACDC-INT``, ``AC-INT``, ``DC-INT``)."""
        if value is None:
            return self.query_enum(":MODE?", OutputMode)
        self.write(f":MODE {self._enum(value, OutputMode)}")
        return None

    # -- phase -------------------------------------------------------------

    def start_phase_state(self, value: PhaseState | int | str | None = None) -> PhaseState | None:
        """``[:SOURce]:PHASe:STARt:STATe`` - start phase free/fixed."""
        if value is None:
            return self.query_enum(":PHASe:STARt:STATe?", PhaseState)
        self.write(f":PHASe:STARt:STATe {self._enum(value, PhaseState)}")
        return None

    def stop_phase_state(self, value: PhaseState | int | str | None = None) -> PhaseState | None:
        """``[:SOURce]:PHASe:STOP:STATe`` - stop phase free/fixed."""
        if value is None:
            return self.query_enum(":PHASe:STOP:STATe?", PhaseState)
        self.write(f":PHASe:STOP:STATe {self._enum(value, PhaseState)}")
        return None

    def start_phase(self, value: Any = None) -> float | None:
        """``[:SOURce]:PHASe:STARt[:IMMediate]`` - start phase (0-359.9 deg)."""
        if value is None:
            return self.query_float(":PHASe:STARt?")
        self.write(f":PHASe:STARt {self._num(value)}")
        return None

    def stop_phase(self, value: Any = None) -> float | None:
        """``[:SOURce]:PHASe:STOP[:IMMediate]`` - stop phase (0-359.9 deg)."""
        if value is None:
            return self.query_float(":PHASe:STOP?")
        self.write(f":PHASe:STOP {self._num(value)}")
        return None

    def sync_phase(self, value: Any = None) -> float | None:
        """``[:SOURce]:PHASe:SYNC[:IMMediate]`` - sync delay phase (0-359.9 deg)."""
        if value is None:
            return self.query_float(":PHASe:SYNC?")
        self.write(f":PHASe:SYNC {self._num(value)}")
        return None

    # -- measurement readback ---------------------------------------------

    def read(self) -> Readings:
        """``[:SOURce]:READ?`` - return the full measurement readout."""
        tokens = self.query_csv(":READ?")
        if len(tokens) != len(_READ_FIELDS):
            raise QueryError(
                f":READ? expected {len(_READ_FIELDS)} fields, got {len(tokens)}"
            )
        values = []
        for position, token in enumerate(tokens, 1):
            try:
                values.append(parse_float(token))
            except (TypeError, ValueError) as exc:
                raise QueryError(
                    f":READ? invalid numeric token at field {position}: {token!r}"
                ) from exc
        return Readings(**dict(zip(_READ_FIELDS, values)))

    # -- voltage -----------------------------------------------------------

    def voltage_range(self, value: VoltageRange | int | str | None = None) -> VoltageRange | None:
        """``[:SOURce]:VOLTage:RANGe`` - voltage range (``100``/``200``/``AUTO``)."""
        if value is None:
            return self.query_enum(":VOLTage:RANGe?", VoltageRange)
        self.write(f":VOLTage:RANGe {self._enum(value, VoltageRange)}")
        return None

    def voltage_limit_rms(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage:LIMit:RMS`` - Vrms limit."""
        if value is None:
            return self.query_float(":VOLTage:LIMit:RMS?")
        self.write(f":VOLTage:LIMit:RMS {self._num(value)}")
        return None

    def voltage_limit_peak(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage:LIMit:PEAK`` - Vpp limit."""
        if value is None:
            return self.query_float(":VOLTage:LIMit:PEAK?")
        self.write(f":VOLTage:LIMit:PEAK {self._num(value)}")
        return None

    def voltage_limit_high(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage:LIMit:HIGH`` - voltage high limit."""
        if value is None:
            return self.query_float(":VOLTage:LIMit:HIGH?")
        self.write(f":VOLTage:LIMit:HIGH {self._num(value)}")
        return None

    def voltage_limit_low(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage:LIMit:LOW`` - voltage low limit."""
        if value is None:
            return self.query_float(":VOLTage:LIMit:LOW?")
        self.write(f":VOLTage:LIMit:LOW {self._num(value)}")
        return None

    def voltage(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage[:LEVel][:IMMediate][:AMPLitude]`` - RMS voltage (V)."""
        if value is None:
            return self.query_float(":VOLTage?")
        self.write(f":VOLTage {self._num(value)}")
        return None

    def voltage_offset(self, value: Any = None) -> float | None:
        """``[:SOURce]:VOLTage[:LEVel][:IMMediate]:OFFSet`` - voltage offset (V)."""
        if value is None:
            return self.query_float(":VOLTage:OFFSet?")
        self.write(f":VOLTage:OFFSet {self._num(value)}")
        return None
