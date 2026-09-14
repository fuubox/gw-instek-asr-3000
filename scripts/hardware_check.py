"""Standalone guided hardware check for the ASR-3300.

Walks an operator through a physical verification checklist, prompting for
confirmation at each step, and logs everything to ``logs/`` for later review.

Usage::

    python scripts/hardware_check.py 192.168.1.100
    # or
    ASR_HOST=192.168.1.100 python scripts/hardware_check.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gw_instek_asr import ASR3300  # noqa: E402, I001
from tests.integration.support import ResultLog, run_checklist  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the guided ASR-3300 hardware checklist")
    parser.add_argument("host", nargs="?", help="instrument IP address or hostname (default: ASR_HOST)")
    parser.add_argument("--allow-output", action="store_true", help="authorize reset, configuration, and energized output")
    parser.add_argument("--non-interactive", action="store_true", help="skip operator prompts and record UNVERIFIED")
    args = parser.parse_args()

    host = args.host or os.environ.get("ASR_HOST")
    if not host:
        parser.print_usage()
        return 2
    if not args.allow_output:
        print("refusing to run hazardous checklist without explicit --allow-output")
        return 2

    port = int(os.environ.get("ASR_PORT", "2268"))
    non_interactive = args.non_interactive or not bool(getattr(sys.stdin, "isatty", lambda: False)())

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
