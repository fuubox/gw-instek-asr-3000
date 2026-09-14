"""Enumerated types, data containers, and value converters.

The ASR-3000 SCPI command set makes heavy use of enumerated parameters (both
numeric codes and mnemonic keywords).  The enums below model those parameters,
and the converter helpers normalise ``int`` / ``str`` / ``Enum`` inputs so that
command methods can accept any convenient form.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any

from .errors import InvalidValueError


class OutputMode(IntEnum):
    """[:SOURce]:MODE output mode."""

    ACDC_INT = 0
    AC_INT = 1
    DC_INT = 2
    ACDC_EXT = 3
    AC_EXT = 4
    ACDC_ADD = 5
    AC_ADD = 6
    ACDC_SYNC = 7
    AC_SYNC = 8
    AC_VCA = 9


class Waveform(IntEnum):
    """[:SOURce]:FUNCtion[:SHAPe] output waveform."""

    ARB1 = 0
    ARB2 = 1
    ARB3 = 2
    ARB4 = 3
    ARB5 = 4
    ARB6 = 5
    ARB7 = 6
    ARB8 = 7
    ARB9 = 8
    ARB10 = 9
    ARB11 = 10
    ARB12 = 11
    ARB13 = 12
    ARB14 = 13
    ARB15 = 14
    ARB16 = 15
    SIN = 16
    SQU = 17
    TRI = 18


class VoltageRange(IntEnum):
    """[:SOURce]:VOLTage:RANGe voltage range."""

    RANGE_100 = 0
    RANGE_200 = 1
    AUTO = 2

    __aliases__ = {"100": RANGE_100, "200": RANGE_200}


class PowerOnState(IntEnum):
    """:OUTPut:PON power-on output state."""

    OFF = 0
    ON = 1
    SEQ = 2
    SIM = 3


class ConfigMode(IntEnum):
    """[:SYSTem]:CONFigure[:MODE] test mode."""

    CONT = 0
    SEQ = 1
    SIM = 2

    __aliases__ = {"CONTINUOUS": CONT, "SEQUENCE": SEQ, "SIMULATION": SIM, "CONTINUE": CONT}


class THDFormat(IntEnum):
    """[:SOURce]:FUNCtion:THD:FORMat THD calculation standard."""

    IEC = 0
    CSA = 1


class SlewMode(IntEnum):
    """[:SYSTem]:SLEW:MODE slew mode."""

    TIME = 0
    SLOPE = 1


class SlopeMode(IntEnum):
    """[:SYSTem]:SLOPe:MODE slope speed."""

    SLOW = 0
    FAST = 1


class VoltageUnit(IntEnum):
    """[:SYSTem]:VUNit voltage setting unit for TRI/ARB waveforms."""

    RMS = 0
    PP = 1

    __aliases__ = {"P-P": PP, "P_P": PP, "PKPK": PP, "PEAK": PP}


class PhaseState(IntEnum):
    """Phase free/fixed state."""

    FREE = 0
    FIXED = 1


class SyncSource(IntEnum):
    """:INPut:SYNC:SOURce sync source."""

    LINE = 0
    EXT = 1


class RemoteState(str, Enum):
    """[:SYSTem]:COMMunicate:RLSTate local/remote state."""

    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
    RWLOCK = "RWLOCK"
    LREMOTE = "LREMOTE"


class TriggerSource(str, Enum):
    """[:SYSTem]:CONFigure:TRIGger:OUTPut:SOURce trigger output source."""

    NONE = "NONE"
    ZERO_CROSS = "ZERO-cross"
    OUTPUT_OFF = "OUTPut-off"


class DisplayMode(str, Enum):
    """:DISPlay:DESign:MODE display mode."""

    NORMAL = "NORMAL"
    SIMPLE = "SIMPLE"


class MeasureSource(str, Enum):
    """:DISPlay:MEASure:SOURce measurement display item."""

    VRMS = "VRMS"
    VAVG = "VAVG"
    VMAX = "VMAX"
    VMIN = "VMIN"
    IRMS = "IRMS"
    IAVG = "IAVG"
    IMAX = "IMAX"
    IMIN = "IMIN"
    IPKH = "IPKH"
    RPOWER = "RPOWer"
    SPOWER = "SPOWer"
    QPOWER = "QPOWer"
    FREQUENCY = "FREQuency"
    PFACTOR = "PFACtor"
    CFACTOR = "CFACtor"
    THDV = "THDV"
    THDI = "THDI"


class SerialParity(str, Enum):
    """[:SYSTem]:COMMunicate:SERial parity."""

    NONE = "NONE"
    ODD = "ODD"
    EVEN = "EVEN"


class SequenceAction(str, Enum):
    """:TRIGger:SEQuence:SELected:EXECute action."""

    STOP = "STOP"
    START = "START"
    HOLD = "HOLD"
    BRAN1 = "BRAN1"
    BRAN2 = "BRAN2"


class SimulateAction(str, Enum):
    """:TRIGger:SIMulation:SELected:EXECute action."""

    STOP = "STOP"
    START = "START"
    HOLD = "HOLD"


class BuiltinFunction(str, Enum):
    """[:SYSTem]:ARBitrary:EDIT:BUILtin built-in wave function."""

    TRIANGLE = "TRIangle"
    STAIR = "STAir"
    CLIP = "CLIP"
    CFACTOR1 = "CFACtor1"
    CFACTOR2 = "CFACtor2"
    SURGE = "SURGe"
    RIPPLE = "RIPPle"
    DIP = "DIP"
    LFRING = "LFRing"
    DST01 = "DST01"
    DST02 = "DST02"
    DST03 = "DST03"
    DST04 = "DST04"
    DST05 = "DST05"
    DST06 = "DST06"
    DST07 = "DST07"
    DST08 = "DST08"
    DST09 = "DST09"
    DST10 = "DST10"
    DST11 = "DST11"
    DST12 = "DST12"
    DST13 = "DST13"
    DST14 = "DST14"
    DST15 = "DST15"
    DST16 = "DST16"
    DST17 = "DST17"
    DST18 = "DST18"
    DST19 = "DST19"
    DST20 = "DST20"
    DST21 = "DST21"
    DST22 = "DST22"


class SequenceCondition(IntEnum):
    """[:SOURce]:SEQuence:CONDition sequence run status."""

    IDLE = 0
    RUN = 1
    HOLD = 2


class SimulationCondition(IntEnum):
    """[:SOURce]:SIMulation:CONDition simulation run status."""

    IDLE = 0
    RUN = 1
    HOLD = 2


class SimulationStep(IntEnum):
    """[:SOURce]:SIMulation:CSTep current simulation step."""

    INITIAL = 0
    NORMAL1 = 1
    TRANSITION1 = 2
    ABNORMAL = 3
    TRANSITION2 = 4
    NORMAL2 = 5


@dataclass(frozen=True)
class Identification:
    """Parsed ``*IDN?`` response."""

    manufacturer: str
    model: str
    serial: str
    firmware: str


@dataclass(frozen=True)
class Readings:
    """Parsed ``[:SOURce]:READ?`` response (17 fields)."""

    vrms: float | None
    vavg: float | None
    vmax: float | None
    vmin: float | None
    irms: float | None
    iavg: float | None
    imax: float | None
    imin: float | None
    ipk_hold: float | None
    power_real: float | None
    power_apparent: float | None
    power_reactive: float | None
    power_factor: float | None
    crest_factor: float | None
    thd_v: float | None
    thd_i: float | None
    frequency: float | None


@dataclass(frozen=True)
class SCPIError:
    """Parsed ``:SYSTem:ERRor?`` response."""

    code: int
    message: str


def _normalize(value: str) -> str:
    return value.strip().upper().replace("-", "_").replace(" ", "_")


def as_enum(value: Any, enum_cls: type[Enum]) -> Enum:
    """Coerce ``value`` into a member of ``enum_cls``."""
    if isinstance(value, enum_cls):
        return value
    if isinstance(value, bool):
        raise InvalidValueError(f"boolean not allowed for {enum_cls.__name__}: {value!r}")
    if isinstance(value, int):
        try:
            return enum_cls(value)
        except ValueError as exc:
            raise InvalidValueError(f"{value!r} is not a valid {enum_cls.__name__}") from exc
    if isinstance(value, str):
        key = _normalize(value)
        aliases = getattr(enum_cls, "__aliases__", {})
        if key in aliases:
            return enum_cls(aliases[key])
        for member in enum_cls:
            if member.name == key:
                return member
            if isinstance(member.value, str) and _normalize(member.value) == key:
                return member
        if issubclass(enum_cls, IntEnum):
            try:
                return enum_cls(int(value))
            except ValueError:
                pass
        raise InvalidValueError(f"{value!r} is not a valid {enum_cls.__name__}")
    raise InvalidValueError(f"cannot interpret {value!r} as {enum_cls.__name__}")


def fmt_enum(value: Any, enum_cls: type[Enum]) -> str:
    """Format an enumerated value for a SCPI command."""
    member = as_enum(value, enum_cls)
    if issubclass(enum_cls, IntEnum):
        return str(int(member))
    return str(member.value)


def as_bool(value: Any) -> bool:
    """Coerce a boolean-ish value (bool/int/``"ON"``/``"OFF"``/``"0"``/``"1"``)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        key = _normalize(value)
        if key in ("ON", "TRUE"):
            return True
        if key in ("OFF", "FALSE"):
            return False
        try:
            return bool(int(key, 10))
        except ValueError:
            pass
    raise InvalidValueError(f"cannot interpret {value!r} as boolean")


def fmt_bool(value: Any) -> str:
    """Format a boolean value as ``ON``/``OFF``."""
    return "ON" if as_bool(value) else "OFF"


def fmt_number(value: Any) -> str:
    """Format a numeric value, passing ``MIN``/``MAX`` mnemonics through."""
    if isinstance(value, str):
        key = _normalize(value)
        if key in ("MIN", "MINIMUM"):
            return "MIN"
        if key in ("MAX", "MAXIMUM"):
            return "MAX"
    return repr(float(value))


def fmt_int(value: Any) -> str:
    """Format an integer value, passing ``MIN``/``MAX`` mnemonics through."""
    if isinstance(value, str):
        key = _normalize(value)
        if key in ("MIN", "MINIMUM"):
            return "MIN"
        if key in ("MAX", "MAXIMUM"):
            return "MAX"
    return str(int(value))


def fmt_string(value: Any) -> str:
    """Format a string parameter as a quoted SCPI string."""
    return '"' + str(value).replace('"', "") + '"'


def parse_float(token: str) -> float | None:
    """Parse a numeric token, mapping ``Invalid``/blank to ``None``."""
    token = token.strip()
    if not token or token.upper() in ("INVALID", "NAN"):
        return None
    return float(token)


def parse_int(token: str) -> int | None:
    """Parse an integer token, mapping ``Invalid``/blank to ``None``."""
    token = token.strip()
    if not token or token.upper() in ("INVALID", "NAN"):
        return None
    return int(float(token))
