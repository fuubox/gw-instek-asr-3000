# Changelog

Notable changes to this project are documented here.

## 0.2.0 — 2026-09-14

### Safety

- Reject ambiguous boolean setter values instead of treating arbitrary truthy values as `ON`.
- Require explicit `--allow-output` authorization for energized hardware checks.
- De-energize and abort the hardware checklist immediately after an operator rejects a confirmation.

### Reliability

- Invalidate failed socket transports without replaying commands whose delivery may be uncertain.
- Strictly validate bounded IEEE 488.2 binary blocks, including headers, lengths, terminators, and connection state after malformed frames.
- Reject malformed fixed-shape `READ?` responses with contextual driver errors.

### Development and documentation

- Add CI coverage for Python 3.10 through 3.13, distribution builds, linting, formatting, type checking, and strict documentation builds.
- Add contract coverage for the public SCPI command wrappers.
- Add a navigable API reference and generated SCPI-to-Python index.

## 0.1.1

- Preserve signed boolean replies and improve hardware-checklist settling behavior.

## 0.1.0

- Initial release of the ASR-3000 series Python driver.
