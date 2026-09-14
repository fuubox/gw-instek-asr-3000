"""Example: connect to an ASR-3300 over Ethernet and take a measurement."""

from gw_instek_asr import ASR3300, OutputMode, Waveform


def main() -> None:
    HOST = "192.168.1.100"  # <- set your instrument's IP address

    with ASR3300(HOST) as asr:
        print(asr.identify())

        # Configure a 230 Vrms / 50 Hz sine output in AC-INT mode.
        asr.mode(OutputMode.AC_INT)
        asr.waveform(Waveform.SIN)
        asr.voltage(230.0)
        asr.frequency(50.0)

        asr.output_on()
        print(f"Vrms = {asr.voltage_rms():.3f} V")
        print(f"Irms = {asr.current_rms():.3f} A")
        print(f"Power = {asr.power_real():.3f} W")
        asr.output_off()


if __name__ == "__main__":
    main()
