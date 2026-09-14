"""Python driver for the GW Instek ASR-3000 series programmable AC/DC source."""

from __future__ import annotations

from . import errors
from ._types import (
    BuiltinFunction,
    ConfigMode,
    DisplayMode,
    Identification,
    MeasureSource,
    OutputMode,
    PhaseState,
    PowerOnState,
    Readings,
    RemoteState,
    SCPIError,
    SequenceAction,
    SequenceCondition,
    SerialParity,
    SimulateAction,
    SimulationCondition,
    SimulationStep,
    SlewMode,
    SlopeMode,
    SyncSource,
    THDFormat,
    TriggerSource,
    VoltageRange,
    VoltageUnit,
    Waveform,
)
from .errors import (
    CommandError,
    CommunicationError,
    ConnectionTimeout,
    GWInstekError,
    InvalidValueError,
    QueryError,
)
from .instrument import ASR3000, ASR3300
from .transport import DEFAULT_PORT, DEFAULT_TIMEOUT

__version__ = "0.1.1"

__all__ = [
    "ASR3000",
    "ASR3300",
    "DEFAULT_PORT",
    "DEFAULT_TIMEOUT",
    "__version__",
    "errors",
    "GWInstekError",
    "CommunicationError",
    "ConnectionTimeout",
    "CommandError",
    "QueryError",
    "InvalidValueError",
    "BuiltinFunction",
    "ConfigMode",
    "DisplayMode",
    "Identification",
    "MeasureSource",
    "OutputMode",
    "PhaseState",
    "PowerOnState",
    "Readings",
    "RemoteState",
    "SCPIError",
    "SequenceAction",
    "SequenceCondition",
    "SerialParity",
    "SimulateAction",
    "SimulationCondition",
    "SimulationStep",
    "SlewMode",
    "SlopeMode",
    "SyncSource",
    "THDFormat",
    "TriggerSource",
    "VoltageRange",
    "VoltageUnit",
    "Waveform",
]
