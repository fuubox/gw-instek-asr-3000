"""Reviewed command-wrapper inventory.

Each command mixin is covered by the subsystem contract tests below.  The
inventory is intentionally hand-maintained so expected SCPI literals remain
visible in tests instead of being generated from production implementation.
"""

from __future__ import annotations

from pathlib import Path

INVENTORY = {
    "common": "test_common.py",
    "data": "test_data.py",
    "display": "test_output_measure.py",
    "input": "test_source.py",
    "measure": "test_output_measure.py",
    "memory": "test_data.py",
    "output": "test_output_measure.py",
    "sequence": "test_status_seq_sim.py and test_command_contracts.py",
    "simulate": "test_status_seq_sim.py and test_command_contracts.py",
    "source": "test_source.py",
    "status": "test_status_seq_sim.py and test_command_contracts.py",
    "system": "test_system.py",
}


def test_every_command_mixin_has_an_inventory_row():
    command_dir = Path(__file__).parents[1] / "src" / "gw_instek_asr" / "commands"
    mixins = {path.stem for path in command_dir.glob("*.py") if path.stem != "__init__"}
    assert set(INVENTORY) == mixins
    assert all(value.startswith("test_") for value in INVENTORY.values())
