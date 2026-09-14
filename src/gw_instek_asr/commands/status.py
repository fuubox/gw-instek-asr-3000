"""Status subsystem commands (``:STATus``)."""

from __future__ import annotations

from ..scpi import SCPIBase


class StatusCommands(SCPIBase):
    """Status register groups: operation, questionable, warning, lock."""

    def _register(self, subsystem: str, register: str, value: int | None = None) -> int | None:
        cmd = f":STATus:{subsystem}:{register}"
        if value is None:
            return self.query_int(cmd + "?")
        self.write(f"{cmd} {self._int(value)}")
        return None

    # -- operation ---------------------------------------------------------

    def operation_condition(self) -> int:
        return self.query_int_required(":STATus:OPERation:CONDition?")

    def operation_enable(self, value: int | None = None) -> int | None:
        return self._register("OPERation", "ENABle", value)

    def operation_event(self) -> int:
        return self.query_int_required(":STATus:OPERation:EVENt?")

    def operation_ntransition(self, value: int | None = None) -> int | None:
        return self._register("OPERation", "NTRansition", value)

    def operation_ptransition(self, value: int | None = None) -> int | None:
        return self._register("OPERation", "PTRansition", value)

    # -- questionable ------------------------------------------------------

    def questionable_condition(self) -> int:
        return self.query_int_required(":STATus:QUEStionable:CONDition?")

    def questionable_enable(self, value: int | None = None) -> int | None:
        return self._register("QUEStionable", "ENABle", value)

    def questionable_event(self) -> int:
        return self.query_int_required(":STATus:QUEStionable:EVENt?")

    def questionable_ntransition(self, value: int | None = None) -> int | None:
        return self._register("QUEStionable", "NTRansition", value)

    def questionable_ptransition(self, value: int | None = None) -> int | None:
        return self._register("QUEStionable", "PTRansition", value)

    # -- warning -----------------------------------------------------------

    def warning_condition(self) -> int:
        return self.query_int_required(":STATus:WARNing:CONDition?")

    def warning_enable(self, value: int | None = None) -> int | None:
        return self._register("WARNing", "ENABle", value)

    def warning_event(self) -> int:
        return self.query_int_required(":STATus:WARNing:EVENt?")

    def warning_ntransition(self, value: int | None = None) -> int | None:
        return self._register("WARNing", "NTRansition", value)

    def warning_ptransition(self, value: int | None = None) -> int | None:
        return self._register("WARNing", "PTRansition", value)

    # -- system lock -------------------------------------------------------

    def lock_condition(self) -> int:
        return self.query_int_required(":STATus:LOCK:CONDition?")

    def lock_enable(self, value: int | None = None) -> int | None:
        return self._register("LOCK", "ENABle", value)

    def lock_event(self) -> int:
        return self.query_int_required(":STATus:LOCK:EVENt?")

    def lock_ntransition(self, value: int | None = None) -> int | None:
        return self._register("LOCK", "NTRansition", value)

    def lock_ptransition(self, value: int | None = None) -> int | None:
        return self._register("LOCK", "PTRansition", value)

    # -- preset ------------------------------------------------------------

    def preset(self) -> None:
        """``:STATus:PRESet`` - reset enable registers and transition filters."""
        self.write(":STATus:PRESet")
