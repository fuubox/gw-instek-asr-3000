# Quick start

Install the package and create an `ASR3300` instance with the instrument's IP
address:

```python
from gw_instek_asr import ASR3300

with ASR3300("192.168.1.100") as instrument:
    instrument.output_off()
    instrument.voltage(120.0)
    instrument.frequency(60.0)
    instrument.output_on()
    print(instrument.voltage_rms())
```

The default TCP port is 2268. Pass `connect=False` to open the connection
lazily, or provide a custom `Transport` in tests. Always turn the output off
when a test or operating sequence is complete.
