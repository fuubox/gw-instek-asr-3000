"""SCPI command/query plumbing shared by every command group."""

from __future__ import annotations

from typing import Any

from ._types import (
    as_bool,
    as_enum,
    fmt_bool,
    fmt_enum,
    fmt_int,
    fmt_number,
    fmt_string,
    parse_float,
    parse_int,
)
from .errors import QueryError
from .transport import Transport

_TERMINATOR = b"\n"
_WAVEFORM_MAX_BLOCK = 8192


class SCPIBase:
    """Base class providing ``write``/``query`` plus value formatting helpers."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    # -- raw I/O -----------------------------------------------------------

    def write(self, command: str) -> None:
        """Send a command (no response expected)."""
        self._transport.send(command.encode("ascii") + _TERMINATOR)

    def write_raw(self, data: bytes) -> None:
        """Send raw bytes followed by the terminator."""
        self._transport.send(data + _TERMINATOR)

    def query(self, command: str) -> str:
        """Send a query and return the trimmed response string."""
        self.write(command)
        return self._transport.readline().decode("ascii", errors="replace").strip()

    def query_block(self, command: str) -> bytes:
        """Send a query and read an IEEE 488.2 definite-length binary block."""
        self.write(command)
        tr = self._transport
        marker = tr.read_exact(1)
        if marker != b"#":
            raise QueryError(f"expected binary block header, got {marker!r}")
        digit_token = tr.read_exact(1)
        if len(digit_token) != 1 or not digit_token.isdigit():
            raise QueryError(f"invalid binary block digit count: {digit_token!r}")
        ndigits = digit_token[0] - ord("0")
        if ndigits < 1 or ndigits > 4:
            raise QueryError(f"invalid binary block digit count: {ndigits}")
        length_token = tr.read_exact(ndigits)
        if len(length_token) != ndigits or not length_token.isdigit():
            raise QueryError(f"invalid binary block length: {length_token!r}")
        length = int(length_token)
        if length > _WAVEFORM_MAX_BLOCK:
            raise QueryError(f"binary block length {length} exceeds maximum {_WAVEFORM_MAX_BLOCK}")
        data = tr.read_exact(length)
        terminator = tr.read_exact(1)
        if terminator == b"\r":
            if tr.read_exact(1) != b"\n":
                raise QueryError("binary block has invalid CRLF terminator")
        elif terminator != b"\n":
            raise QueryError(f"binary block missing LF terminator: {terminator!r}")
        return data

    # -- typed queries -----------------------------------------------------

    def query_float(self, command: str) -> float | None:
        return parse_float(self.query(command))

    def query_int(self, command: str) -> int | None:
        return parse_int(self.query(command))

    def query_int_required(self, command: str) -> int:
        value = self.query_int(command)
        if value is None:
            raise QueryError(f"expected integer response for {command}")
        return value

    def query_bool(self, command: str) -> bool:
        return as_bool(self.query(command))

    def query_enum(self, command: str, enum_cls: type) -> Any:
        return as_enum(self.query(command), enum_cls)

    def query_floats(self, command: str) -> list[float | None]:
        return [parse_float(t) for t in self.query(command).split(",")]

    def query_ints(self, command: str) -> list[int | None]:
        return [parse_int(t) for t in self.query(command).split(",")]

    def query_csv(self, command: str) -> list[str]:
        return [t.strip() for t in self.query(command).split(",")]

    # -- value formatting --------------------------------------------------

    @staticmethod
    def _bool(value: Any) -> str:
        return fmt_bool(value)

    @staticmethod
    def _num(value: Any) -> str:
        return fmt_number(value)

    @staticmethod
    def _int(value: Any) -> str:
        return fmt_int(value)

    @staticmethod
    def _enum(value: Any, enum_cls: type) -> str:
        return fmt_enum(value, enum_cls)

    @staticmethod
    def _str(value: Any) -> str:
        return fmt_string(value)
