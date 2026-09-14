# Running the ASR-3000 Integration Tests

System integration tests drive a **physical** ASR-3000 over Ethernet and ask an
operator to confirm physical behaviour. Every reading and confirmation is
written to a timestamped log for later review.

## Prerequisites

- Instrument powered on with the Ethernet (LAN) cable connected.
- Your PC on the same network; know the instrument's IP address (Menu → LAN).
- The socket port is **fixed at 2268** — no configuration needed.
- A local virtualenv with the package installed:

  ```powershell
  & ".venv\Scripts\python.exe" -m pip install -e ".[dev]"
  ```

## Quick start

```powershell
# pytest (use -s so prompts are visible)
& ".venv\Scripts\python.exe" -m pytest tests/integration -s --asr-host=192.168.1.100
```

```powershell
# or the standalone script (no pytest needed)
& ".venv\Scripts\python.exe" scripts\hardware_check.py 192.168.1.100
```

## Options / environment variables

| Option / env var       | Default | Meaning                                  |
| ---------------------- | ------- | ---------------------------------------- |
| `--asr-host` / `ASR_HOST` | —     | Instrument IP or hostname (required)     |
| `--asr-port` / `ASR_PORT` | `2268` | Socket port                              |
| `--non-interactive`    | off     | Skip operator prompts (record `UNVERIFIED`) |
| `ASR_LOG_DIR`          | `logs`  | Where result logs are written            |

Without a host, the pytest tests are **skipped** (not failures). With a host
but a non-TTY stdin, read-only tests remain available. The checklist is
hazardous: `ASR_HOST` alone never authorizes reset, configuration, or energized
output. Run it only when operator-attended and explicitly authorize it:

```powershell
& ".venv\Scripts\python.exe" -m pytest tests/integration -s --asr-host=192.168.1.100 --allow-output
```

`--non-interactive` does not replace `--allow-output`; it only records prompts
as `UNVERIFIED` after output has been separately authorized.

## What the checklist does

Run order and what to observe at each prompt:

1. **Identify** — queries `*IDN?` and logs model/serial/firmware.
2. **Reset** — issues `*RST`.
3. **Configure AC** — AC-INT, sine, **120.0 Vrms / 60.0 Hz**.
4. **Output ON** → *"Is the OUTPUT indicator on?"*
5. → *"Front panel shows ~120.0 V and ~60.00 Hz?"*
6. Reads back `Vrms`, `Irms`, `P` automatically.
7. → *"DMM-measured Vrms"* (optional; blank to skip).
8. **Output OFF.**
9. **Configure DC** — DC-INT, **48.0 Vdc** (set via `:VOLTage:OFFSet`).
10. **Output ON** → *"Front panel shows ~48.0 Vdc?"*
11. **Output OFF.**
12. Queries the error queue and status byte, then finishes.

The output is always forced off in a `finally` block, even on error.

If an operator answers “no” to a confirmation, the checklist de-energizes the
instrument and ends immediately. Non-interactive `UNVERIFIED` confirmations
continue only when `--allow-output` was explicitly supplied.

## Result logs

Each run writes two files:

```
logs/
  asr3000_hardware_YYYYMMDD_HHMMSS.log   # human-readable, mirrors stdout
  asr3000_hardware_YYYYMMDD_HHMMSS.json  # machine-readable summary
```

Every step is recorded with a status:

| Status       | Meaning                                   |
| ------------ | ----------------------------------------- |
| `PASS`       | operator confirmed the physical behaviour |
| `FAIL`       | operator reported a mismatch              |
| `UNVERIFIED` | no confirmation (non-interactive run)     |
| `INFO`       | automated reading or log note             |

The `.json` is a list under `entries`, e.g.
`{"step": "ac_measurements", "status": "INFO", "detail": "Vrms=120.0 V, ...", "time": "..."}`.

## Troubleshooting

| Symptom                          | Likely cause / fix                                        |
| -------------------------------- | --------------------------------------------------------- |
| `failed to connect to ...`       | Wrong IP, cable unplugged, or firewalled port 2268        |
| `timed out reading ...`          | Instrument busy or not responding; check it's in remote mode |
| `ConnectionTimeout`              | Increase timeout / verify instrument is reachable (`ping`)|
| Tests show `SKIPPED`             | No `--asr-host` / `ASR_HOST` provided                     |
| Prompts don't appear             | You forgot `-s`, or run with `--non-interactive`          |
