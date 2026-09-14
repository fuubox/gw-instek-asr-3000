"""Exception hierarchy for the GW Instek ASR-3000 driver."""

from __future__ import annotations


class GWInstekError(Exception):
    """Base class for all errors raised by this package."""


class CommunicationError(GWInstekError):
    """Raised when communication with the instrument fails."""


class ConnectionTimeout(CommunicationError):
    """Raised when a socket operation times out."""


class CommandError(GWInstekError):
    """Raised when the instrument reports an error for a command."""


class QueryError(GWInstekError):
    """Raised when a query returns no data or malformed data."""


class InvalidValueError(GWInstekError, ValueError):
    """Raised when an invalid parameter value is supplied to a command."""
