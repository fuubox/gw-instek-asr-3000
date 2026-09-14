# gw-instek-asr-3000

A pure-Python driver for the **GW Instek ASR-3000 series** programmable
AC/DC power source (ASR-3200, ASR-3300, ASR-3400, ASR-3400HF).  The MVP
communicates with the instrument over **Ethernet** using a raw TCP SCPI
socket.

> **Unofficial project.** This software is **not** affiliated with, endorsed
> by, or in any way connected to Good Will Instrument Co., Ltd. ("GW Instek").
> It is an independent, community-written driver created by reverse-engineering
> the publicly available programming manual. "GW Instek" and "ASR" are
> trademarks of their respective owners and are used here only to identify
> the hardware this driver targets.

## Features

- Zero runtime dependencies (stdlib `socket` only).
- Full SCPI command set from the *ASR-3000 Programming Manual* (Rev. E):
  IEEE 488.2 common commands, output, source, measure, system, status,
  sequence, simulation, data/trace, memory, input and display subsystems.
- Type-safe enums for enumerated parameters, with forgiving `int` / `str` /
  `Enum` input coercion.
- Binary arbitrary-waveform transfer (`:DATA:TRACe:WAVe` block data).
- Context-manager and connection management, with clear exception types.

## Installation

```bash
pip install -e .          # development install
pip install -e ".[dev]"   # include pytest
```

Requires Python 3.10+.

## Quick start

The ASR-3000 socket server port is fixed at **2268**.

```python
from gw_instek_asr import ASR3300, OutputMode, Waveform

with ASR3300("192.168.1.100") as asr:
    print(asr.identify())               # Identification(model='ASR-3300', ...)

    asr.mode(OutputMode.AC_INT)         # AC-INT output mode
    asr.waveform(Waveform.SIN)          # sine wave
    asr.voltage(230.0)                  # 230 Vrms
    asr.frequency(50.0)                 # 50 Hz
    asr.output_on()

    print("Vrms =", asr.voltage_rms())  # measured voltage
    print("Irms =", asr.current_rms())
```

`ASR3000` (the series) and `ASR3300` (the 3000 VA model) expose the same API.

## API conventions

- **Get/set pattern.**  A method sets when given a value and queries when
  called with no arguments:

  ```python
  asr.voltage(120.0)     # :VOLTage 120.0
  asr.voltage()          # :VOLTage?  -> 120.0
  ```

- **Enums.**  Enumerated parameters accept an enum member, an integer, or a
  mnemonic string and are returned as enum members:

  ```python
  asr.mode("ACDC-INT") is OutputMode.ACDC_INT
  ```

- **Booleans** accept `True`/`False`, `1`/`0`, or `"ON"`/`"OFF"`.

- **`MIN`/`MAX`.**  Numeric setters pass the mnemonics through:

  ```python
  asr.voltage("MAX")
  ```

## Raw command access

Anything not covered by a typed helper can be sent directly:

```python
asr.write(":SOURce:VOLTage 120.0")
value = asr.query(":SOURce:VOLTage?")
```

## Testing

The test suite uses an in-memory fake transport for command encoding plus a
local TCP socket server to exercise the real transport end-to-end.

```bash
python -m pytest
```

For the complete local quality gate, install the development extra and run:

```bash
python -m pip install -e ".[dev]"
python -m ruff check src tests scripts examples
python -m ruff format --check src tests scripts examples
python -m mypy src/gw_instek_asr
python -m pytest -q
```

## Publishing to PyPI

Publishing is handled by `.github/workflows/publish.yml`, which builds the
sdist/wheel, runs the test suite, and publishes to PyPI when you push a tag
like `v0.1.0` (or trigger the workflow manually). Configure one of:

- **Trusted publishing (recommended):** in PyPI → *Publishing*, add a trusted
  publisher for this repo (owner `fuubox`, repo `gw-instek-asr-3000`); no
  secrets required.
- **API token:** add a repository secret named `PYPI_API_TOKEN` and, in the
  workflow, pass `password: ${{ secrets.PYPI_API_TOKEN }}` to the
  `pypa/gh-action-pypi-publish` step.

## License

Zero-Clause BSD (0BSD) — see `LICENSE`.  Completely open source and free to
use, modify, and redistribute, with or without fee, for any purpose.
Attribution is appreciated but **not** required.
