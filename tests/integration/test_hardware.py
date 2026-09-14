"""System integration tests against a physical ASR-3000 over Ethernet.

Skipped automatically unless ``--asr-host`` / ``ASR_HOST`` is set.  Run with
``-s`` so the operator confirmation prompts are visible::

    python -m pytest tests/integration -s --asr-host=192.168.1.100

Results are written to ``logs/asr3000_hardware_<timestamp>.log`` (and ``.json``).
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.hardware


def test_identify(hardware, log) -> None:
    ident = hardware.identify()
    log.record("identify", "INFO", ident)
    assert ident.model.startswith("ASR-")


def test_socket_port(hardware, log) -> None:
    port = hardware.tcpip_control()
    log.record("socket_port", "INFO", port)
    assert port == 2268


@pytest.mark.hazardous
def test_hardware_checklist(hardware, log, non_interactive) -> None:
    from .support import run_checklist

    run_checklist(hardware, log, non_interactive)
