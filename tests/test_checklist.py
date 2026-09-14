"""Verify the checklist flow and result logging without real hardware."""

from __future__ import annotations

import json
from types import SimpleNamespace


def test_run_checklist_logs(monkeypatch, tmp_path, instrument, transport):
    monkeypatch.setenv("ASR_LOG_DIR", str(tmp_path))

    from tests.integration import support
    from tests.integration.support import ResultLog, run_checklist

    settle_events = []

    def record_settle(delay):
        settle_events.append((delay, transport.sent[-1]))

    monkeypatch.setattr(
        support,
        "time",
        SimpleNamespace(sleep=record_settle),
        raising=False,
    )

    transport.queue_line("GW-INSTEK,ASR-3300,G1234567,1.12")  # *IDN?
    transport.queue_line("120.0")  # :MEASure:VOLTage?
    transport.queue_line("1.5")  # :MEASure:CURRent?
    transport.queue_line("180.0")  # :MEASure:POWer?
    transport.queue_line('0,"No error"')  # :SYSTem:ERRor?
    transport.queue_line("0")  # *STB?

    result_log = ResultLog("test_checklist")
    run_checklist(instrument, result_log, non_interactive=True)
    log_path, json_path = result_log.close()

    assert log_path.exists()
    assert json_path.exists()

    data = json.loads(json_path.read_text())
    steps = {entry["step"]: entry for entry in data["entries"]}

    assert steps["ac_output_indicator"]["status"] == "UNVERIFIED"
    assert steps["ac_front_panel"]["status"] == "UNVERIFIED"
    assert steps["dc_front_panel"]["status"] == "UNVERIFIED"
    assert steps["ac_settle"]["detail"] == "waited 1.0 s"
    assert steps["dc_settle"]["detail"] == "waited 1.0 s"
    assert steps["ac_measurements"]["detail"] == "Vrms=120.0 V, Irms=1.5 A, P=180.0 W"
    assert steps["done"]["status"] == "INFO"
    assert settle_events == [
        (1.0, b":OUTPut:STATe ON\n"),
        (1.0, b":OUTPut:STATe ON\n"),
    ]
