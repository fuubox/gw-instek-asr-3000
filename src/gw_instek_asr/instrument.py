"""High-level instrument class for the GW Instek ASR-3000 series."""

from __future__ import annotations

from .commands.common import CommonCommands
from .commands.data import DataCommands
from .commands.display import DisplayCommands
from .commands.input import InputCommands
from .commands.measure import MeasureCommands
from .commands.memory import MemoryCommands
from .commands.output import OutputCommands
from .commands.sequence import SequenceCommands
from .commands.simulate import SimulateCommands
from .commands.source import SourceCommands
from .commands.status import StatusCommands
from .commands.system import SystemCommands
from .scpi import SCPIBase
from .transport import DEFAULT_PORT, DEFAULT_TIMEOUT, SocketTransport, Transport


class ASR3000(
    CommonCommands,
    OutputCommands,
    SourceCommands,
    MeasureCommands,
    SystemCommands,
    StatusCommands,
    SequenceCommands,
    SimulateCommands,
    DataCommands,
    MemoryCommands,
    InputCommands,
    DisplayCommands,
    SCPIBase,
):
    """Driver for the GW Instek ASR-3000 series programmable AC/DC source.

    The series covers the ASR-3200, ASR-3300, ASR-3400 and ASR-3400HF models,
    which share an identical remote command set.  Communication uses a raw
    TCP SCPI socket (default port 2268).

    Parameters
    ----------
    host:
        Instrument IP address or hostname (required unless ``transport`` is given).
    port:
        TCP port.  The ASR-3000 socket port is fixed at 2268.
    timeout:
        Socket timeout in seconds.
    transport:
        Optional pre-configured :class:`~gw_instek_asr.transport.Transport`
        (used mainly for testing).  When supplied, ``host`` is ignored.
    connect:
        When ``False`` the connection is opened lazily on first use.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        transport: Transport | None = None,
        connect: bool = True,
    ) -> None:
        if transport is None:
            if host is None:
                raise ValueError("either 'host' or 'transport' must be provided")
            transport = SocketTransport(host, port=port, timeout=timeout)
        super().__init__(transport)
        self._connect_on_first_use = connect
        if connect:
            opener = getattr(transport, "connect", None)
            if opener is not None:
                opener()

    @property
    def host(self) -> str | None:
        return getattr(self._transport, "host", None)

    @property
    def port(self) -> int | None:
        return getattr(self._transport, "port", None)

    @property
    def connected(self) -> bool:
        return bool(getattr(self._transport, "connected", False))

    def connect(self) -> None:
        """Open the connection to the instrument."""
        opener = getattr(self._transport, "connect", None)
        if opener is not None:
            opener()

    def close(self) -> None:
        """Close the connection to the instrument."""
        closer = getattr(self._transport, "close", None)
        if closer is not None:
            closer()

    def __enter__(self) -> "ASR3000":
        self.connect()
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def __repr__(self) -> str:
        state = "connected" if self.connected else "disconnected"
        return f"<{type(self).__name__} {self.host}:{self.port} ({state})>"


class ASR3300(ASR3000):
    """ASR-3300 (3000 VA) — identical command set to the ASR-3000 series."""
