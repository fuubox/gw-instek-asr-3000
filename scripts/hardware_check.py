"""Standalone guided hardware check for the ASR-3300.

Walks an operator through a physical verification checklist, prompting for
confirmation at each step, and logs everything to ``logs/`` for later review.

Usage::

    python scripts/hardware_check.py 192.168.1.100
    # or
    ASR_HOST=192.168.1.100 python scripts/hardware_check.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.integration.support import ResultLog, run_checklist  # noqa: E402

from gw_instek_asr import ASR3300  # noqa: E402


def main() -> int:
    host = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ASR_HOST")
    if not host:
        print("usage: python scripts/hardware_check.py <host>")
        return 2

    port = int(os.environ.get("ASR_PORT", "2268"))
    non_interactive = not bool(getattr(sys.stdin, "isatty", lambda: False)())

    log = ResultLog("asr3000_hardware")
    asr = ASR3300(host, port=port, timeout=15.0)
    try:
        run_checklist(asr, log, non_interactive)
    finally:
        asr.close()
        log_path, json_path = log.close()
        print(f"\nLogs written to:\n  {log_path}\n  {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
