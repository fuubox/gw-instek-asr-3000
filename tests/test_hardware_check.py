from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location("hardware_check", Path(__file__).parents[1] / "scripts" / "hardware_check.py")
assert _SPEC is not None and _SPEC.loader is not None
hardware_check = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(hardware_check)


def test_standalone_hardware_check_requires_explicit_output_authorization(monkeypatch, capsys):
    monkeypatch.setenv("ASR_HOST", "192.0.2.10")
    monkeypatch.setattr(sys, "argv", ["hardware_check.py"])

    assert hardware_check.main() == 2
    assert "--allow-output" in capsys.readouterr().out


def test_standalone_hardware_check_passes_non_interactive_mode(monkeypatch):
    calls: dict[str, object] = {}

    class FakeInstrument:
        def __init__(self, host, port, timeout):
            calls["instrument"] = (host, port, timeout)

        def close(self):
            calls["closed"] = True

    class FakeLog:
        def __init__(self, name):
            calls["log_name"] = name

        def close(self):
            return Path("run.log"), Path("run.json")

    def fake_checklist(instrument, log, non_interactive):
        calls["non_interactive"] = non_interactive

    monkeypatch.setattr(hardware_check, "ASR3300", FakeInstrument)
    monkeypatch.setattr(hardware_check, "ResultLog", FakeLog)
    monkeypatch.setattr(hardware_check, "run_checklist", fake_checklist)
    monkeypatch.setattr(sys, "argv", ["hardware_check.py", "192.0.2.10", "--allow-output", "--non-interactive"])

    assert hardware_check.main() == 0
    assert calls["non_interactive"] is True
    assert calls["closed"] is True
