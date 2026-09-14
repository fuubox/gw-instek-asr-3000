"""System function commands (``:SYSTem``)."""

from __future__ import annotations

from typing import Any

from .._types import (
    BuiltinFunction,
    ConfigMode,
    RemoteState,
    SCPIError,
    SerialParity,
    SlewMode,
    SlopeMode,
    TriggerSource,
    VoltageUnit,
)
from ..scpi import SCPIBase


class SystemCommands(SCPIBase):
    """System configuration: arbitrary edit, beeper, communications, errors."""

    # -- helpers -----------------------------------------------------------

    def _str_get_set(self, cmd: str, value: Any = None) -> str | None:
        if value is None:
            return self.query(cmd + "?").strip('"')
        self.write(f"{cmd} {self._str(value)}")
        return None

    @staticmethod
    def _arb(value: Any) -> str:
        if isinstance(value, int):
            return str(value)
        s = str(value).strip().upper()
        return s if s.startswith("ARB") or s.isdigit() else s

    @staticmethod
    def _surge_type(value: Any) -> str:
        if isinstance(value, int):
            return "SQU" if value == 0 else "SIN"
        return "SQU" if str(value).strip().upper() in ("SQU", "0") else "SIN"

    # -- AC input detection ------------------------------------------------

    def acin_detection(self, value: Any = None) -> bool | None:
        """``:SYSTem:ACIN:DETection`` - set or query AC input detection."""
        if value is None:
            return self.query_bool(":SYSTem:ACIN:DETection?")
        self.write(f":SYSTem:ACIN:DETection {self._bool(value)}")
        return None

    # -- arbitrary edit ----------------------------------------------------

    def arbitrary_builtin(self, value: BuiltinFunction | str | None = None) -> str | None:
        """``:SYSTem:ARBitrary:EDIT:BUILtin`` - built-in arbitrary edit function."""
        if value is None:
            return self.query(":SYSTem:ARBitrary:EDIT:BUILtin?")
        self.write(f":SYSTem:ARBitrary:EDIT:BUILtin {self._enum(value, BuiltinFunction)}")
        return None

    def arbitrary_surge(
        self,
        wave_type: Any = None,
        acv: Any = None,
        site: Any = None,
    ) -> tuple[str, float, float] | None:
        """``:SYSTem:ARBitrary:EDIT:SURGe`` - surge wave type/ACV/site parameters."""
        cmd = ":SYSTem:ARBitrary:EDIT:SURGe"
        if wave_type is None and acv is None and site is None:
            tokens = self.query_csv(cmd + "?")
            return (tokens[0], float(tokens[1]), float(tokens[2]))
        self.write(f"{cmd} {self._surge_type(wave_type)},{self._int(acv)},{self._int(site)}")
        return None

    def arbitrary_stair(self, value: Any = None) -> int | None:
        """``:SYSTem:ARBitrary:EDIT:STAir`` - stair count (1-100)."""
        if value is None:
            return self.query_int(":SYSTem:ARBitrary:EDIT:STAir?")
        self.write(f":SYSTem:ARBitrary:EDIT:STAir {self._int(value)}")
        return None

    def arbitrary_cfactor2(self, value: Any = None) -> float | None:
        """``:SYSTem:ARBitrary:EDIT:CFACtor2`` - CF-2 crest factor (1.5-2.0)."""
        if value is None:
            return self.query_float(":SYSTem:ARBitrary:EDIT:CFACtor2?")
        self.write(f":SYSTem:ARBitrary:EDIT:CFACtor2 {self._num(value)}")
        return None

    def arbitrary_cfactor1(self, value: Any = None) -> float | None:
        """``:SYSTem:ARBitrary:EDIT:CFACtor1`` - CF-1 crest factor (1.1-10.0)."""
        if value is None:
            return self.query_float(":SYSTem:ARBitrary:EDIT:CFACtor1?")
        self.write(f":SYSTem:ARBitrary:EDIT:CFACtor1 {self._num(value)}")
        return None

    def arbitrary_clip(self, value: Any = None) -> float | None:
        """``:SYSTem:ARBitrary:EDIT:CLIP`` - clip ratio (0.0-1.0)."""
        if value is None:
            return self.query_float(":SYSTem:ARBitrary:EDIT:CLIP?")
        self.write(f":SYSTem:ARBitrary:EDIT:CLIP {self._num(value)}")
        return None

    def arbitrary_store(self, target: Any) -> None:
        """``:SYSTem:ARBitrary:EDIT:STORe`` - save built-in data to ARB1-16."""
        self.write(f":SYSTem:ARBitrary:EDIT:STORe {self._arb(target)}")

    def arbitrary_triangle(self, value: Any = None) -> int | None:
        """``:SYSTem:ARBitrary:EDIT:TRIangle`` - triangle symmetry (0-100%)."""
        if value is None:
            return self.query_int(":SYSTem:ARBitrary:EDIT:TRIangle?")
        self.write(f":SYSTem:ARBitrary:EDIT:TRIangle {self._int(value)}")
        return None

    def arbitrary_dip(self, st_phs: Any = None, sp_phs: Any = None, end_phs: Any = None) -> tuple[float, float, float] | None:
        """``:SYSTem:ARBitrary:EDIT:DIP`` - DIP wave phase parameters (HF only)."""
        cmd = ":SYSTem:ARBitrary:EDIT:DIP"
        if st_phs is None and sp_phs is None and end_phs is None:
            tokens = self.query_csv(cmd + "?")
            return (float(tokens[0]), float(tokens[1]), float(tokens[2]))
        self.write(f"{cmd} {self._num(st_phs)},{self._num(sp_phs)},{self._num(end_phs)}")
        return None

    def arbitrary_lfring(
        self,
        acv: Any = None,
        amp: Any = None,
        base_f: Any = None,
        ring_f: Any = None,
        decay: Any = None,
        st_phs: Any = None,
        end_phs: Any = None,
        ring_phs: Any = None,
    ) -> tuple[float, ...] | None:
        """``:SYSTem:ARBitrary:EDIT:LFRing`` - LFRing wave parameters (HF only)."""
        cmd = ":SYSTem:ARBitrary:EDIT:LFRing"
        args = (acv, amp, base_f, ring_f, decay, st_phs, end_phs, ring_phs)
        if all(a is None for a in args):
            tokens = self.query_csv(cmd + "?")
            return tuple(float(t) for t in tokens)
        self.write(
            f"{cmd} "
            + ",".join(
                [
                    self._num(acv),
                    self._int(amp),
                    self._num(base_f),
                    self._num(ring_f),
                    self._num(decay),
                    self._num(st_phs),
                    self._num(end_phs),
                    self._num(ring_phs),
                ]
            )
        )
        return None

    def arbitrary_ripple(self, times: Any = None, vdc: Any = None, level: Any = None) -> tuple[int, int, int] | None:
        """``:SYSTem:ARBitrary:EDIT:RIPPle`` - DC ripple parameters."""
        cmd = ":SYSTem:ARBitrary:EDIT:RIPPle"
        if times is None and vdc is None and level is None:
            tokens = self.query_csv(cmd + "?")
            return (int(tokens[0]), int(tokens[1]), int(tokens[2]))
        self.write(f"{cmd} {self._int(times)},{self._int(vdc)},{self._int(level)}")
        return None

    def arbitrary_store_apply(self, target: Any) -> None:
        """``:SYSTem:ARBitrary:EDIT:STORe:APPLy`` - save built-in data and apply it."""
        self.write(f":SYSTem:ARBitrary:EDIT:STORe:APPLy {self._arb(target)}")

    # -- beeper ------------------------------------------------------------

    def beeper_state(self, value: Any = None) -> bool | None:
        """``:SYSTem:BEEPer:STATe`` - buzzer on/off."""
        if value is None:
            return self.query_bool(":SYSTem:BEEPer:STATe?")
        self.write(f":SYSTem:BEEPer:STATe {self._bool(value)}")
        return None

    # -- communication -----------------------------------------------------

    def gpib_address(self, value: Any = None) -> int | None:
        """``:SYSTem:COMMunicate:GPIB[:SELF]:ADDRess`` - GPIB address (0-30)."""
        if value is None:
            return self.query_int(":SYSTem:COMMunicate:GPIB:ADDRess?")
        self.write(f":SYSTem:COMMunicate:GPIB:ADDRess {self._int(value)}")
        return None

    def lan_dhcp(self, value: Any = None) -> bool | None:
        """``:SYSTem:COMMunicate:LAN:DHCP`` - DHCP on/off."""
        if value is None:
            return self.query_bool(":SYSTem:COMMunicate:LAN:DHCP?")
        self.write(f":SYSTem:COMMunicate:LAN:DHCP {self._bool(value)}")
        return None

    def lan_dns(self, value: Any = None) -> str | None:
        return self._str_get_set(":SYSTem:COMMunicate:LAN:DNS", value)

    def lan_gateway(self, value: Any = None) -> str | None:
        return self._str_get_set(":SYSTem:COMMunicate:LAN:GATeway", value)

    def lan_ip(self, value: Any = None) -> str | None:
        return self._str_get_set(":SYSTem:COMMunicate:LAN:IPADdress", value)

    def lan_mac(self) -> str:
        """``:SYSTem:COMMunicate:LAN:MAC?`` - unit MAC address."""
        return self.query(":SYSTem:COMMunicate:LAN:MAC?")

    def lan_subnet_mask(self, value: Any = None) -> str | None:
        return self._str_get_set(":SYSTem:COMMunicate:LAN:SMASk", value)

    def remote_state(self, value: RemoteState | str | None = None) -> RemoteState | None:
        """``:SYSTem:COMMunicate:RLSTate`` - local/remote control state."""
        if value is None:
            return self.query_enum(":SYSTem:COMMunicate:RLSTate?", RemoteState)
        self.write(f":SYSTem:COMMunicate:RLSTate {self._enum(value, RemoteState)}")
        return None

    def serial_baud(self, value: Any = None) -> int | None:
        """``:SYSTem:COMMunicate:SERial:TRANsmit:BAUD`` - UART baud rate."""
        cmd = ":SYSTem:COMMunicate:SERial:TRANsmit:BAUD"
        if value is None:
            return self.query_int(cmd + "?")
        self.write(f"{cmd} {self._int(value)}")
        return None

    def serial_bits(self, value: Any = None) -> int | None:
        """``:SYSTem:COMMunicate:SERial:TRANsmit:BITS`` - data bits (0=7, 1=8)."""
        cmd = ":SYSTem:COMMunicate:SERial:TRANsmit:BITS"
        if value is None:
            return self.query_int(cmd + "?")
        self.write(f"{cmd} {self._int(value)}")
        return None

    def serial_parity(self, value: SerialParity | int | str | None = None) -> SerialParity | None:
        """``:SYSTem:COMMunicate:SERial:TRANsmit:PARity`` - UART parity."""
        cmd = ":SYSTem:COMMunicate:SERial:TRANsmit:PARity"
        if value is None:
            code = self.query_int(cmd + "?")
            if code in (0, 1, 2):
                return SerialParity(("NONE", "ODD", "EVEN")[code])
            return None
        if isinstance(value, int):
            keyword = ("NONE", "ODD", "EVEN")[value]
        else:
            keyword = self._enum(value, SerialParity)
        self.write(f"{cmd} {keyword}")
        return None

    def serial_stop_bits(self, value: Any = None) -> int | None:
        """``:SYSTem:COMMunicate:SERial:TRANsmit:SBITs`` - stop bits (0=1, 1=2)."""
        cmd = ":SYSTem:COMMunicate:SERial:TRANsmit:SBITs"
        if value is None:
            return self.query_int(cmd + "?")
        self.write(f"{cmd} {self._int(value)}")
        return None

    def tcpip_control(self) -> int:
        """``:SYSTem:COMMunicate:TCPip:CONTrol?`` - socket port number (2268)."""
        return self.query_int_required(":SYSTem:COMMunicate:TCPip:CONTrol?")

    def usb_front_state(self) -> int:
        """``:SYSTem:COMMunicate:USB:FRONt:STATe?`` - front USB-A port state."""
        return self.query_int_required(":SYSTem:COMMunicate:USB:FRONt:STATe?")

    def usb_rear_state(self) -> int:
        """``:SYSTem:COMMunicate:USB:REAR:STATe?`` - rear USB-B port state."""
        return self.query_int_required(":SYSTem:COMMunicate:USB:REAR:STATe?")

    # -- configuration -----------------------------------------------------

    def config_mode(self, value: ConfigMode | int | str | None = None) -> ConfigMode | None:
        """``:SYSTem:CONFigure[:MODE]`` - test mode (CONT/SEQ/SIM)."""
        if value is None:
            return self.query_enum(":SYSTem:CONFigure?", ConfigMode)
        self.write(f":SYSTem:CONFigure {self._enum(value, ConfigMode)}")
        return None

    def extio_state(self, value: Any = None) -> bool | None:
        """``:SYSTem:CONFigure:EXTio[:STATe]`` - external control on/off."""
        if value is None:
            return self.query_bool(":SYSTem:CONFigure:EXTio?")
        self.write(f":SYSTem:CONFigure:EXTio {self._bool(value)}")
        return None

    def trigger_output_width(self, value: Any = None) -> float | None:
        """``:SYSTem:CONFigure:TRIGger:OUTPut:WIDTh`` - trigger output width."""
        if value is None:
            return self.query_float(":SYSTem:CONFigure:TRIGger:OUTPut:WIDTh?")
        self.write(f":SYSTem:CONFigure:TRIGger:OUTPut:WIDTh {self._num(value)}")
        return None

    def trigger_output_source(self, value: TriggerSource | str | None = None) -> TriggerSource | None:
        """``:SYSTem:CONFigure:TRIGger:OUTPut:SOURce`` - trigger output source."""
        if value is None:
            return self.query_enum(":SYSTem:CONFigure:TRIGger:OUTPut:SOURce?", TriggerSource)
        self.write(f":SYSTem:CONFigure:TRIGger:OUTPut:SOURce {self._enum(value, TriggerSource)}")
        return None

    # -- error / misc ------------------------------------------------------

    def error(self) -> SCPIError:
        """``:SYSTem:ERRor?`` - pop the last error from the error queue."""
        raw = self.query(":SYSTem:ERRor?")
        code_s, _, message = raw.partition(",")
        return SCPIError(int(float(code_s.strip())), message.strip().strip('"'))

    def error_enable(self) -> None:
        """``:SYSTem:ERRor:ENABle`` - clear the error queue and enable error messages."""
        self.write(":SYSTem:ERRor:ENABle")

    def hold_state(self, value: Any = None) -> bool | None:
        """``:SYSTem:HOLD:STATe`` - freeze hold on/off."""
        if value is None:
            return self.query_bool(":SYSTem:HOLD:STATe?")
        self.write(f":SYSTem:HOLD:STATe {self._bool(value)}")
        return None

    def ipk_hold_time(self, value: Any = None) -> int | None:
        """``:SYSTem:IPKHold:TIME`` - Ipeak hold time (1-60000 ms)."""
        if value is None:
            return self.query_int(":SYSTem:IPKHold:TIME?")
        self.write(f":SYSTem:IPKHold:TIME {self._int(value)}")
        return None

    def key_lock(self, value: Any = None) -> bool | None:
        """``:SYSTem:KLOCk`` - front-panel key lock."""
        if value is None:
            return self.query_bool(":SYSTem:KLOCk?")
        self.write(f":SYSTem:KLOCk {self._bool(value)}")
        return None

    def reboot(self) -> None:
        """``:SYSTem:REBoot`` - reboot the instrument."""
        self.write(":SYSTem:REBoot")

    def slew_mode(self, value: SlewMode | int | str | None = None) -> SlewMode | None:
        """``:SYSTem:SLEW:MODE`` - slew mode (TIME/SLOPE)."""
        if value is None:
            return self.query_enum(":SYSTem:SLEW:MODE?", SlewMode)
        self.write(f":SYSTem:SLEW:MODE {self._enum(value, SlewMode)}")
        return None

    def voltage_unit(self, value: VoltageUnit | int | str | None = None) -> VoltageUnit | None:
        """``:SYSTem:VUNit`` - voltage unit for TRI/ARB (RMS/P-P)."""
        if value is None:
            return self.query_enum(":SYSTem:VUNit?", VoltageUnit)
        self.write(f":SYSTem:VUNit {self._enum(value, VoltageUnit)}")
        return None

    def interlock(self, value: Any = None) -> bool | None:
        """``:SYSTem:INTerlock`` - interlock on/off (external control only)."""
        if value is None:
            return self.query_bool(":SYSTem:INTerlock?")
        self.write(f":SYSTem:INTerlock {self._bool(value)}")
        return None

    def slope_mode(self, value: SlopeMode | int | str | None = None) -> SlopeMode | None:
        """``:SYSTem:SLOPe:MODE`` - slope speed (SLOW/FAST)."""
        if value is None:
            return self.query_enum(":SYSTem:SLOPe:MODE?", SlopeMode)
        self.write(f":SYSTem:SLOPe:MODE {self._enum(value, SlopeMode)}")
        return None
