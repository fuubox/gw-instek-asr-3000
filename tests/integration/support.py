"""Support helpers for hardware (system) integration tests.

Provides a timestamped text+JSON result logger and interactive prompt helpers
so an operator can confirm physical behaviour and have every observation
recorded for later review.
"""

from __future__ import annotations

import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from gw_instek_asr import OutputMode, Waveform


SETTLE_SECONDS = 1.0


def _log_dir() -> Path:
    return Path(os.environ.get("ASR_LOG_DIR", "logs"))


class ResultLog:
    """Append-only log that mirrors entries to stdout and a JSON summary."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.started = datetime.datetime.now()
        self.entries: list[dict[str, Any]] = []
        directory = _log_dir()
        directory.mkdir(exist_ok=True)
        stamp = self.started.strftime("%Y%m%d_%H%M%S")
        self.log_path = directory / f"{name}_{stamp}.log"
        self.json_path = directory / f"{name}_{stamp}.json"
        self._f = open(self.log_path, "w", encoding="utf-8")
        self._line(f"=== {name} started {self.started.isoformat()} ===")

    def _line(self, text: str) -> None:
        print(text)
        self._f.write(text + "\n")
        self._f.flush()

    def record(self, step: str, status: str, detail: Any = "") -> None:
        entry = {
            "step": step,
            "status": status,
            "detail": str(detail),
            "time": datetime.datetime.now().isoformat(),
        }
        self.entries.append(entry)
        self._line(f"[{status:^11}] {step}: {detail}")

    def close(self) -> tuple[Path, Path]:
        self._f.write(f"=== finished {datetime.datetime.now().isoformat()} ===\n")
        self._f.close()
        with open(self.json_path, "w", encoding="utf-8") as jf:
            json.dump(
                {
                    "name": self.name,
                    "started": self.started.isoformat(),
                    "entries": self.entries,
                },
                jf,
                indent=2,
            )
        return self.log_path, self.json_path


def _interactive(non_interactive: bool) -> bool:
    return not non_interactive and bool(getattr(sys.stdin, "isatty", lambda: False)())


def confirm(prompt: str, non_interactive: bool = False) -> bool | None:
    """Ask the operator a yes/no question.  ``None`` means unverified."""
    if not _interactive(non_interactive):
        return None
    try:
        while True:
            answer = input(f"{prompt} [y/n]: ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer y or n.")
    except (EOFError, KeyboardInterrupt):
        return None


def read_float(prompt: str, non_interactive: bool = False) -> float | None:
    """Ask the operator for a numeric reading (blank to skip)."""
    if not _interactive(non_interactive):
        return None
    try:
        while True:
            raw = input(f"{prompt} ").strip()
            if raw == "":
                return None
            try:
                return float(raw)
            except ValueError:
                print("Please enter a number (or blank to skip).")
    except (EOFError, KeyboardInterrupt):
        return None


def status(value: bool | None) -> str:
    if value is True:
        return "PASS"
    if value is False:
        return "FAIL"
    return "UNVERIFIED"


def run_checklist(hardware: Any, log: ResultLog, non_interactive: bool = False) -> None:
    """Run the guided hardware checklist against a connected instrument.

    Every automated reading and every operator confirmation is written to the
    ``ResultLog`` for later review.
    """
    log.record("identify", "INFO", hardware.idn())
    log.record("connection", "INFO", f"{hardware.host}:{hardware.port}")

    hardware.reset()
    log.record("reset", "INFO", "*RST issued")

    try:
        # -- AC-INT: 120 Vrms / 60 Hz sine ---------------------------------
        hardware.mode(OutputMode.AC_INT)
        hardware.waveform(Waveform.SIN)
        hardware.voltage(120.0)
        hardware.frequency(60.0)
        log.record("configure_ac", "INFO", "AC-INT, SIN, 120.0 Vrms, 60.0 Hz")

        hardware.output_on()
        time.sleep(SETTLE_SECONDS)
        log.record("ac_settle", "INFO", f"waited {SETTLE_SECONDS} s")
        ac_indicator = confirm("Is the OUTPUT indicator on?", non_interactive)
        log.record("ac_output_indicator", status(ac_indicator))
        if ac_indicator is False:
            hardware.output_off()
            log.record("aborted", "FAIL", "operator rejected AC output indicator")
            return

        ac_front_panel = confirm(
            "Front panel shows ~120.0 V and ~60.00 Hz?", non_interactive
        )
        log.record("ac_front_panel", status(ac_front_panel))
        if ac_front_panel is False:
            hardware.output_off()
            log.record("aborted", "FAIL", "operator rejected AC front-panel reading")
            return

        vrms = hardware.voltage_rms()
        irms = hardware.current_rms()
        power = hardware.power_real()
        log.record("ac_measurements", "INFO", f"Vrms={vrms} V, Irms={irms} A, P={power} W")

        dmm = read_float("DMM-measured Vrms (blank to skip):", non_interactive)
        log.record("dmm_vrms", "INFO", "not provided" if dmm is None else f"{dmm} V")
        hardware.output_off()

        # -- DC-INT: 48 Vdc ------------------------------------------------
        hardware.mode(OutputMode.DC_INT)
        hardware.voltage_offset(48.0)
        log.record("configure_dc", "INFO", "DC-INT, 48.0 Vdc")

        hardware.output_on()
        time.sleep(SETTLE_SECONDS)
        log.record("dc_settle", "INFO", f"waited {SETTLE_SECONDS} s")
        dc_front_panel = confirm("Front panel shows ~48.0 Vdc?", non_interactive)
        log.record("dc_front_panel", status(dc_front_panel))
        if dc_front_panel is False:
            hardware.output_off()
            log.record("aborted", "FAIL", "operator rejected DC front-panel reading")
            return
        hardware.output_off()

        # -- status / error queue ------------------------------------------
        err = hardware.error()
        log.record("error_queue", "INFO", f"code={err.code}, message={err.message}")
        log.record("status_byte", "INFO", f"0x{hardware.status_byte():02X}")
    finally:
        hardware.output_off()

    log.record("done", "INFO", "checklist complete")
