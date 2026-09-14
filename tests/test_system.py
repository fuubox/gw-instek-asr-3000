from __future__ import annotations

from gw_instek_asr import ConfigMode, RemoteState, SCPIError, SerialParity


def test_beeper(instrument, transport):
    instrument.beeper_state(True)
    assert transport.sent[-1] == b":SYSTem:BEEPer:STATe ON\n"


def test_gpib_address(instrument, transport):
    instrument.gpib_address(15)
    assert transport.sent[-1] == b":SYSTem:COMMunicate:GPIB:ADDRess 15\n"
    transport.queue_line("15")
    assert instrument.gpib_address() == 15


def test_lan_dhcp(instrument, transport):
    instrument.lan_dhcp(True)
    assert transport.sent[-1] == b":SYSTem:COMMunicate:LAN:DHCP ON\n"


def test_lan_ip(instrument, transport):
    instrument.lan_ip("172.16.5.111")
    assert transport.sent[-1] == b':SYSTem:COMMunicate:LAN:IPADdress "172.16.5.111"\n'
    transport.queue_line('"172.16.5.111"')
    assert instrument.lan_ip() == "172.16.5.111"


def test_tcpip_control(instrument, transport):
    transport.queue_line("2268")
    assert instrument.tcpip_control() == 2268


def test_config_mode(instrument, transport):
    instrument.config_mode(ConfigMode.SEQ)
    assert transport.sent[-1] == b":SYSTem:CONFigure 1\n"
    transport.queue_line("SEQ")
    assert instrument.config_mode() == ConfigMode.SEQ


def test_remote_state(instrument, transport):
    instrument.remote_state(RemoteState.REMOTE)
    assert transport.sent[-1] == b":SYSTem:COMMunicate:RLSTate REMOTE\n"


def test_serial_parity(instrument, transport):
    instrument.serial_parity(SerialParity.EVEN)
    assert transport.sent[-1] == b":SYSTem:COMMunicate:SERial:TRANsmit:PARity EVEN\n"
    transport.queue_line("+2")
    assert instrument.serial_parity() == SerialParity.EVEN


def test_error(instrument, transport):
    transport.queue_line('-100, "Command error"')
    err = instrument.error()
    assert err == SCPIError(-100, "Command error")
    assert transport.sent[-1] == b":SYSTem:ERRor?\n"


def test_key_lock(instrument, transport):
    instrument.key_lock(True)
    assert transport.sent[-1] == b":SYSTem:KLOCk ON\n"
