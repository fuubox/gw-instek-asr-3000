"""Literal contracts for wrappers not covered by the focused subsystem tests."""

from __future__ import annotations

import pytest

from gw_instek_asr import (
    ConfigMode,
    PhaseState,
    RemoteState,
    SerialParity,
    SimulationStep,
    SlewMode,
    SlopeMode,
    SyncSource,
    THDFormat,
    TriggerSource,
    VoltageRange,
    VoltageUnit,
    Waveform,
)


@pytest.mark.parametrize(
    ("method", "args", "write", "reply", "result", "query"),
    [
        ("standard_event_status_enable", (7,), b"*ESE 7\n", "7", 7, b"*ESE?\n"),
        ("service_request_enable", (5,), b"*SRE 5\n", "5", 5, b"*SRE?\n"),
        ("operation_enable", (3,), b":STATus:OPERation:ENABle 3\n", "3", 3, b":STATus:OPERation:ENABle?\n"),
        ("operation_ntransition", (4,), b":STATus:OPERation:NTRansition 4\n", "4", 4, b":STATus:OPERation:NTRansition?\n"),
        ("operation_ptransition", (5,), b":STATus:OPERation:PTRansition 5\n", "5", 5, b":STATus:OPERation:PTRansition?\n"),
        ("questionable_enable", (3,), b":STATus:QUEStionable:ENABle 3\n", "3", 3, b":STATus:QUEStionable:ENABle?\n"),
        (
            "questionable_ntransition",
            (4,),
            b":STATus:QUEStionable:NTRansition 4\n",
            "4",
            4,
            b":STATus:QUEStionable:NTRansition?\n",
        ),
        (
            "questionable_ptransition",
            (5,),
            b":STATus:QUEStionable:PTRansition 5\n",
            "5",
            5,
            b":STATus:QUEStionable:PTRansition?\n",
        ),
        ("warning_enable", (3,), b":STATus:WARNing:ENABle 3\n", "3", 3, b":STATus:WARNing:ENABle?\n"),
        ("warning_ntransition", (4,), b":STATus:WARNing:NTRansition 4\n", "4", 4, b":STATus:WARNing:NTRansition?\n"),
        ("warning_ptransition", (5,), b":STATus:WARNing:PTRansition 5\n", "5", 5, b":STATus:WARNing:PTRansition?\n"),
        ("lock_enable", (3,), b":STATus:LOCK:ENABle 3\n", "3", 3, b":STATus:LOCK:ENABle?\n"),
        ("lock_ntransition", (4,), b":STATus:LOCK:NTRansition 4\n", "4", 4, b":STATus:LOCK:NTRansition?\n"),
        ("lock_ptransition", (5,), b":STATus:LOCK:PTRansition 5\n", "5", 5, b":STATus:LOCK:PTRansition?\n"),
        ("current_limit_peak_high", (2,), b":CURRent:LIMit:PEAK:HIGH 2.0\n", "2.5", 2.5, b":CURRent:LIMit:PEAK:HIGH?\n"),
        ("current_limit_peak_low", (1,), b":CURRent:LIMit:PEAK:LOW 1.0\n", "1.5", 1.5, b":CURRent:LIMit:PEAK:LOW?\n"),
        ("current_limit_rms", (3,), b":CURRent:LIMit:RMS 3.0\n", "3.5", 3.5, b":CURRent:LIMit:RMS?\n"),
        ("current_limit_peak_mode", (True,), b":CURRent:LIMit:PEAK:MODE ON\n", "1", True, b":CURRent:LIMit:PEAK:MODE?\n"),
        ("current_limit_rms_mode", (False,), b":CURRent:LIMit:RMS:MODE OFF\n", "0", False, b":CURRent:LIMit:RMS:MODE?\n"),
        ("frequency_limit_high", (60,), b":FREQuency:LIMit:HIGH 60.0\n", "61", 61.0, b":FREQuency:LIMit:HIGH?\n"),
        ("frequency_limit_low", (40,), b":FREQuency:LIMit:LOW 40.0\n", "39", 39.0, b":FREQuency:LIMit:LOW?\n"),
        ("frequency", (50,), b":FREQuency 50.0\n", "51", 51.0, b":FREQuency?\n"),
        ("start_phase", (10,), b":PHASe:STARt 10.0\n", "11", 11.0, b":PHASe:STARt?\n"),
        ("stop_phase", (20,), b":PHASe:STOP 20.0\n", "21", 21.0, b":PHASe:STOP?\n"),
        ("sync_phase", (30,), b":PHASe:SYNC 30.0\n", "31", 31.0, b":PHASe:SYNC?\n"),
        ("voltage_limit_rms", (100,), b":VOLTage:LIMit:RMS 100.0\n", "101", 101.0, b":VOLTage:LIMit:RMS?\n"),
        ("voltage_limit_peak", (200,), b":VOLTage:LIMit:PEAK 200.0\n", "201", 201.0, b":VOLTage:LIMit:PEAK?\n"),
        ("voltage_limit_high", (220,), b":VOLTage:LIMit:HIGH 220.0\n", "221", 221.0, b":VOLTage:LIMit:HIGH?\n"),
        ("voltage_limit_low", (80,), b":VOLTage:LIMit:LOW 80.0\n", "81", 81.0, b":VOLTage:LIMit:LOW?\n"),
        ("voltage_offset", (2,), b":VOLTage:OFFSet 2.0\n", "3", 3.0, b":VOLTage:OFFSet?\n"),
        ("voltage", (120,), b":VOLTage 120.0\n", "121", 121.0, b":VOLTage?\n"),
        ("sensing", (True,), b":MEASure:CONFigure:SENSing ON\n", "1", True, b":MEASure:CONFigure:SENSing?\n"),
        ("gain", (2,), b":INPut:GAIN 2.0\n", "2.5", 2.5, b":INPut:GAIN?\n"),
        ("sync_source", (SyncSource.EXT,), b":INPut:SYNC:SOURce 1\n", "1", SyncSource.EXT, b":INPut:SYNC:SOURce?\n"),
        ("start_phase_state", (PhaseState.FIXED,), b":PHASe:STARt:STATe 1\n", "1", PhaseState.FIXED, b":PHASe:STARt:STATe?\n"),
        ("stop_phase_state", (PhaseState.FREE,), b":PHASe:STOP:STATe 0\n", "0", PhaseState.FREE, b":PHASe:STOP:STATe?\n"),
        ("waveform", (Waveform.SIN,), b":FUNCtion 16\n", "16", Waveform.SIN, b":FUNCtion?\n"),
        ("thd_format", (THDFormat.CSA,), b":FUNCtion:THD:FORMat 1\n", "1", THDFormat.CSA, b":FUNCtion:THD:FORMat?\n"),
        ("voltage_range", (VoltageRange.AUTO,), b":VOLTage:RANGe 2\n", "2", VoltageRange.AUTO, b":VOLTage:RANGe?\n"),
        ("acin_detection", (True,), b":SYSTem:ACIN:DETection ON\n", "1", True, b":SYSTem:ACIN:DETection?\n"),
        ("beeper_state", (False,), b":SYSTem:BEEPer:STATe OFF\n", "0", False, b":SYSTem:BEEPer:STATe?\n"),
        ("gpib_address", (12,), b":SYSTem:COMMunicate:GPIB:ADDRess 12\n", "12", 12, b":SYSTem:COMMunicate:GPIB:ADDRess?\n"),
        ("lan_dhcp", (True,), b":SYSTem:COMMunicate:LAN:DHCP ON\n", "1", True, b":SYSTem:COMMunicate:LAN:DHCP?\n"),
        (
            "lan_dns",
            ("1.1.1.1",),
            b':SYSTem:COMMunicate:LAN:DNS "1.1.1.1"\n',
            '"1.1.1.1"',
            "1.1.1.1",
            b":SYSTem:COMMunicate:LAN:DNS?\n",
        ),
        (
            "lan_gateway",
            ("10.0.0.1",),
            b':SYSTem:COMMunicate:LAN:GATeway "10.0.0.1"\n',
            '"10.0.0.1"',
            "10.0.0.1",
            b":SYSTem:COMMunicate:LAN:GATeway?\n",
        ),
        (
            "lan_ip",
            ("10.0.0.2",),
            b':SYSTem:COMMunicate:LAN:IPADdress "10.0.0.2"\n',
            '"10.0.0.2"',
            "10.0.0.2",
            b":SYSTem:COMMunicate:LAN:IPADdress?\n",
        ),
        (
            "lan_subnet_mask",
            ("255.255.255.0",),
            b':SYSTem:COMMunicate:LAN:SMASk "255.255.255.0"\n',
            '"255.255.255.0"',
            "255.255.255.0",
            b":SYSTem:COMMunicate:LAN:SMASk?\n",
        ),
        (
            "remote_state",
            (RemoteState.REMOTE,),
            b":SYSTem:COMMunicate:RLSTate REMOTE\n",
            "REMOTE",
            RemoteState.REMOTE,
            b":SYSTem:COMMunicate:RLSTate?\n",
        ),
        (
            "serial_baud",
            (9600,),
            b":SYSTem:COMMunicate:SERial:TRANsmit:BAUD 9600\n",
            "9600",
            9600,
            b":SYSTem:COMMunicate:SERial:TRANsmit:BAUD?\n",
        ),
        (
            "serial_bits",
            (1,),
            b":SYSTem:COMMunicate:SERial:TRANsmit:BITS 1\n",
            "1",
            1,
            b":SYSTem:COMMunicate:SERial:TRANsmit:BITS?\n",
        ),
        (
            "serial_parity",
            (SerialParity.EVEN,),
            b":SYSTem:COMMunicate:SERial:TRANsmit:PARity EVEN\n",
            "2",
            SerialParity.EVEN,
            b":SYSTem:COMMunicate:SERial:TRANsmit:PARity?\n",
        ),
        (
            "serial_stop_bits",
            (1,),
            b":SYSTem:COMMunicate:SERial:TRANsmit:SBITs 1\n",
            "1",
            1,
            b":SYSTem:COMMunicate:SERial:TRANsmit:SBITs?\n",
        ),
        ("config_mode", (ConfigMode.SIM,), b":SYSTem:CONFigure 2\n", "2", ConfigMode.SIM, b":SYSTem:CONFigure?\n"),
        ("extio_state", (True,), b":SYSTem:CONFigure:EXTio ON\n", "1", True, b":SYSTem:CONFigure:EXTio?\n"),
        (
            "trigger_output_width",
            (1.5,),
            b":SYSTem:CONFigure:TRIGger:OUTPut:WIDTh 1.5\n",
            "2.5",
            2.5,
            b":SYSTem:CONFigure:TRIGger:OUTPut:WIDTh?\n",
        ),
        (
            "trigger_output_source",
            (TriggerSource.NONE,),
            b":SYSTem:CONFigure:TRIGger:OUTPut:SOURce NONE\n",
            "NONE",
            TriggerSource.NONE,
            b":SYSTem:CONFigure:TRIGger:OUTPut:SOURce?\n",
        ),
        ("hold_state", (False,), b":SYSTem:HOLD:STATe OFF\n", "0", False, b":SYSTem:HOLD:STATe?\n"),
        ("ipk_hold_time", (100,), b":SYSTem:IPKHold:TIME 100\n", "101", 101, b":SYSTem:IPKHold:TIME?\n"),
        ("key_lock", (True,), b":SYSTem:KLOCk ON\n", "1", True, b":SYSTem:KLOCk?\n"),
        ("slew_mode", (SlewMode.SLOPE,), b":SYSTem:SLEW:MODE 1\n", "1", SlewMode.SLOPE, b":SYSTem:SLEW:MODE?\n"),
        ("voltage_unit", (VoltageUnit.PP,), b":SYSTem:VUNit 1\n", "1", VoltageUnit.PP, b":SYSTem:VUNit?\n"),
        ("interlock", (True,), b":SYSTem:INTerlock ON\n", "1", True, b":SYSTem:INTerlock?\n"),
        ("slope_mode", (SlopeMode.FAST,), b":SYSTem:SLOPe:MODE 1\n", "1", SlopeMode.FAST, b":SYSTem:SLOPe:MODE?\n"),
    ],
)
def test_remaining_get_set_contracts(instrument, transport, method, args, write, reply, result, query):
    getattr(instrument, method)(*args)
    assert transport.sent[-1] == write
    transport.queue_line(reply)
    assert getattr(instrument, method)() == result
    assert transport.sent[-1] == query


@pytest.mark.parametrize(
    ("method", "args", "expected"),
    [
        ("operation_complete", (), b"*OPC\n"),
        ("error_enable", (), b":SYSTem:ERRor:ENABle\n"),
        ("reboot", (), b":SYSTem:REBoot\n"),
        ("arbitrary_store", ("ARB3",), b":SYSTem:ARBitrary:EDIT:STORe ARB3\n"),
        ("arbitrary_store_apply", (3,), b":SYSTem:ARBitrary:EDIT:STORe:APPLy 3\n"),
    ],
)
def test_remaining_write_only_contracts(instrument, transport, method, args, expected):
    getattr(instrument, method)(*args)
    assert transport.sent[-1] == expected


@pytest.mark.parametrize(
    ("method", "reply", "result", "expected"),
    [
        ("standard_event_status", "8", 8, b"*ESR?\n"),
        ("status_byte", "16", 16, b"*STB?\n"),
        ("tcpip_control", "2268", 2268, b":SYSTem:COMMunicate:TCPip:CONTrol?\n"),
        ("usb_front_state", "1", 1, b":SYSTem:COMMunicate:USB:FRONt:STATe?\n"),
        ("usb_rear_state", "0", 0, b":SYSTem:COMMunicate:USB:REAR:STATe?\n"),
    ],
)
def test_remaining_query_only_contracts(instrument, transport, method, reply, result, expected):
    transport.queue_line(reply)
    assert getattr(instrument, method)() == result
    assert transport.sent[-1] == expected


@pytest.mark.parametrize(
    ("method", "reply", "result", "expected"),
    [
        ("current_rms", "1.2", 1.2, b":MEASure:CURRent?\n"),
        ("current_harmonic_rms", "1,2", [1.0, 2.0], b":MEASure:CURRent:HARMonic?\n"),
        ("current_harmonic_ratio", "3,4", [3.0, 4.0], b":MEASure:CURRent:HARMonic:RATio?\n"),
        ("voltage_harmonic_ratio", "5,6", [5.0, 6.0], b":MEASure:VOLTage:HARMonic:RATio?\n"),
        ("voltage_harmonic_rms", "7,8", [7.0, 8.0], b":MEASure:VOLTage:HARMonic?\n"),
        ("current_repeat_count", "1,2", ["1", "2"], b":SIMulation:CREPeat:COUNt?\n"),
        ("current_jump_count", "1,2", ["1", "2"], b":SEQuence:CJUMp:CNT?\n"),
        ("sequence_current_time", "1,2", [1, 2], b":SEQuence:CTIMe?\n"),
    ],
)
def test_remaining_csv_contracts(instrument, transport, method, reply, result, expected):
    transport.queue_line(reply)
    assert getattr(instrument, method)() == result
    assert transport.sent[-1] == expected


def test_remaining_typed_status_and_simulation_contracts(instrument, transport):
    transport.queue_line("2")
    assert instrument.sequence_current_step() == 2
    assert transport.sent[-1] == b":SEQuence:CSTep?\n"
    transport.queue_line("3")
    assert instrument.simulation_current_step() is SimulationStep.ABNORMAL
    assert transport.sent[-1] == b":SIMulation:CSTep?\n"


@pytest.mark.parametrize(
    ("method", "args", "write", "reply", "result", "query"),
    [
        ("output_relay", (True,), b":OUTPut:RELay ON\n", "0", False, b":OUTPut:RELay?\n"),
        (
            "initial_start_phase",
            (10,),
            b":SIMulation:INITial:PHASe:STARt 10.0\n",
            "11",
            11.0,
            b":SIMulation:INITial:PHASe:STARt?\n",
        ),
        ("initial_stop_phase", (20,), b":SIMulation:INITial:PHASe:STOP 20.0\n", "21", 21.0, b":SIMulation:INITial:PHASe:STOP?\n"),
        ("normal_frequency", (50,), b":SIMulation:NORMal1:FREQuency 50.0\n", "51", 51.0, b":SIMulation:NORMal1:FREQuency?\n"),
        ("normal_voltage", (120,), b":SIMulation:NORMal1:VOLTage 120.0\n", "121", 121.0, b":SIMulation:NORMal1:VOLTage?\n"),
        (
            "arbitrary_builtin",
            ("TRIangle",),
            b":SYSTem:ARBitrary:EDIT:BUILtin TRIangle\n",
            "TRIangle",
            "TRIangle",
            b":SYSTem:ARBitrary:EDIT:BUILtin?\n",
        ),
        ("arbitrary_stair", (4,), b":SYSTem:ARBitrary:EDIT:STAir 4\n", "5", 5, b":SYSTem:ARBitrary:EDIT:STAir?\n"),
        (
            "arbitrary_cfactor2",
            (1.5,),
            b":SYSTem:ARBitrary:EDIT:CFACtor2 1.5\n",
            "1.6",
            1.6,
            b":SYSTem:ARBitrary:EDIT:CFACtor2?\n",
        ),
        ("arbitrary_cfactor1", (2,), b":SYSTem:ARBitrary:EDIT:CFACtor1 2.0\n", "2.1", 2.1, b":SYSTem:ARBitrary:EDIT:CFACtor1?\n"),
        ("arbitrary_clip", (0.5,), b":SYSTem:ARBitrary:EDIT:CLIP 0.5\n", "0.6", 0.6, b":SYSTem:ARBitrary:EDIT:CLIP?\n"),
        ("arbitrary_triangle", (50,), b":SYSTem:ARBitrary:EDIT:TRIangle 50\n", "51", 51, b":SYSTem:ARBitrary:EDIT:TRIangle?\n"),
        (
            "arbitrary_surge",
            ("SQU", 2, 3),
            b":SYSTem:ARBitrary:EDIT:SURGe SQU,2,3\n",
            "SIN,4,5",
            ("SIN", 4.0, 5.0),
            b":SYSTem:ARBitrary:EDIT:SURGe?\n",
        ),
        (
            "arbitrary_dip",
            (1, 2, 3),
            b":SYSTem:ARBitrary:EDIT:DIP 1.0,2.0,3.0\n",
            "1,2,3",
            (1.0, 2.0, 3.0),
            b":SYSTem:ARBitrary:EDIT:DIP?\n",
        ),
        (
            "arbitrary_ripple",
            (1, 2, 3),
            b":SYSTem:ARBitrary:EDIT:RIPPle 1,2,3\n",
            "4,5,6",
            (4, 5, 6),
            b":SYSTem:ARBitrary:EDIT:RIPPle?\n",
        ),
        (
            "arbitrary_lfring",
            (1, 2, 3, 4, 5, 6, 7, 8),
            b":SYSTem:ARBitrary:EDIT:LFRing 1.0,2,3.0,4.0,5.0,6.0,7.0,8.0\n",
            "1,2,3,4,5,6,7,8",
            (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0),
            b":SYSTem:ARBitrary:EDIT:LFRing?\n",
        ),
    ],
)
def test_remaining_simulation_and_arbitrary_contracts(instrument, transport, method, args, write, reply, result, query):
    getattr(instrument, method)(*args)
    assert transport.sent[-1] == write
    transport.queue_line(reply)
    assert getattr(instrument, method)() == result
    assert transport.sent[-1] == query


def test_lan_mac_contract(instrument, transport):
    transport.queue_line("00:11:22:33:44:55")
    assert instrument.lan_mac() == "00:11:22:33:44:55"
    assert transport.sent[-1] == b":SYSTem:COMMunicate:LAN:MAC?\n"
