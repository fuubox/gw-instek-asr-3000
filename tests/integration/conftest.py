"""Fixtures and CLI options for hardware integration tests.

These tests talk to a physical ASR-3000 over Ethernet and are skipped unless a
host is supplied via ``--asr-host`` or the ``ASR_HOST`` environment variable::

    python -m pytest tests/integration -s --asr-host=192.168.1.100
"""

from __future__ import annotations

import os
import sys

import pytest

from gw_instek_asr import ASR3300


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--asr-host",
        action="store",
        default=None,
        help="ASR-3000 IP address or hostname (default: $ASR_HOST)",
    )
    parser.addoption(
        "--asr-port",
        action="store",
        default=None,
        help="ASR-3000 socket port (default: $ASR_PORT or 2268)",
    )
    parser.addoption(
        "--non-interactive",
        action="store_true",
        help="Skip operator confirmation prompts (record as UNVERIFIED)",
    )
    parser.addoption(
        "--allow-output",
        action="store_true",
        help="Authorize reset/configuration and energized output in hazardous hardware tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "hazardous: test may reset, configure, or energize physical hardware",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--allow-output"):
        return
    skip = pytest.mark.skip(reason="requires explicit --allow-output authorization")
    for item in items:
        if item.get_closest_marker("hazardous"):
            item.add_marker(skip)


@pytest.fixture(scope="session")
def asr_host(request: pytest.FixtureRequest) -> str:
    host = request.config.getoption("--asr-host") or os.environ.get("ASR_HOST")
    if not host:
        pytest.skip("no --asr-host / ASR_HOST provided; skipping hardware tests")
    return host


@pytest.fixture(scope="session")
def asr_port(request: pytest.FixtureRequest) -> int:
    return int(request.config.getoption("--asr-port") or os.environ.get("ASR_PORT", "2268"))


@pytest.fixture(scope="session")
def non_interactive(request: pytest.FixtureRequest) -> bool:
    if request.config.getoption("--non-interactive"):
        return True
    return not bool(getattr(sys.stdin, "isatty", lambda: False)())


@pytest.fixture(scope="session")
def hardware(request: pytest.FixtureRequest, asr_host: str, asr_port: int) -> ASR3300:
    inst = ASR3300(asr_host, port=asr_port, timeout=15.0)
    request.addfinalizer(inst.close)
    return inst


@pytest.fixture(scope="session")
def log(request: pytest.FixtureRequest):
    from .support import ResultLog

    result_log = ResultLog("asr3000_hardware")
    request.addfinalizer(result_log.close)
    return result_log
