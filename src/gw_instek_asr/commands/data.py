"""Data/Trace commands (``:DATA`` / ``:TRACe``)."""

from __future__ import annotations

from ..scpi import SCPIBase


def _make_block(data: bytes) -> bytes:
    length = str(len(data)).encode("ascii")
    return b"#" + str(len(length)).encode("ascii") + length + data


class DataCommands(SCPIBase):
    """Sequence/simulation memory and arbitrary-waveform data transfer."""

    # -- sequence memory ---------------------------------------------------

    def sequence_clear(self, slot: int | str) -> None:
        """``:DATA|TRACe:SEQuence:CLEar`` - clear sequence data (Seq0-9)."""
        self.write(f":DATA:TRACe:SEQuence:CLEar {self._int(slot)}")

    def sequence_recall(self, slot: int | str) -> None:
        """``:DATA|TRACe:SEQuence:RECall`` - load sequence data (Seq0-9)."""
        self.write(f":DATA:TRACe:SEQuence:RECall {self._int(slot)}")

    def sequence_store(self, slot: int | str) -> None:
        """``:DATA|TRACe:SEQuence:STORe`` - save sequence data (Seq0-9)."""
        self.write(f":DATA:TRACe:SEQuence:STORe {self._int(slot)}")

    # -- simulation memory -------------------------------------------------

    def simulation_clear(self, slot: int | str) -> None:
        """``:DATA|TRACe:SIMulation:CLEar`` - clear simulation data (SIM0-9)."""
        self.write(f":DATA:TRACe:SIMulation:CLEar {self._int(slot)}")

    def simulation_recall(self, slot: int | str) -> None:
        """``:DATA|TRACe:SIMulation:RECall`` - load simulation data (SIM0-9)."""
        self.write(f":DATA:TRACe:SIMulation:RECall {self._int(slot)}")

    def simulation_store(self, slot: int | str) -> None:
        """``:DATA|TRACe:SIMulation:STORe`` - save simulation data (SIM0-9)."""
        self.write(f":DATA:TRACe:SIMulation:STORe {self._int(slot)}")

    # -- arbitrary waveform data ------------------------------------------

    def wave_clear(self, arb: int | str) -> None:
        """``:DATA|TRACe:WAVe:CLEar`` - clear arbitrary waveform data (ARB1-16)."""
        self.write(f":DATA:TRACe:WAVe:CLEar {self._int(arb)}")

    def wave_data(self, arb: int, data: bytes | None = None) -> bytes | None:
        """``:DATA|TRACe:WAVe[:DATA]`` - upload or download arbitrary waveform data.

        When ``data`` is ``None`` the 4096-word (8192-byte) big-endian,
        two's-complement waveform for ``arb`` (1-16) is returned as raw bytes.
        Otherwise ``data`` is uploaded to the selected ARB slot.
        """
        if data is None:
            return self.query_block(f":DATA:TRACe:WAVe? {self._int(arb)}")
        payload = f":DATA:TRACe:WAVe {self._int(arb)},".encode("ascii") + _make_block(data)
        self.write_raw(payload)
        return None
