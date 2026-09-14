from __future__ import annotations

import pytest

from gw_instek_asr import InvalidValueError, OutputMode, VoltageRange, Waveform
from gw_instek_asr._types import as_bool, as_enum, fmt_enum, fmt_number


def test_as_enum_accepts_many_forms():
    assert as_enum(0, OutputMode) == OutputMode.ACDC_INT
    assert as_enum("ACDC-INT", OutputMode) == OutputMode.ACDC_INT
    assert as_enum("dc_int", OutputMode) == OutputMode.DC_INT
    assert as_enum("TRI", Waveform) == Waveform.TRI
    assert as_enum("100", VoltageRange) == VoltageRange.RANGE_100
    assert as_enum("AUTO", VoltageRange) == VoltageRange.AUTO


def test_as_enum_invalid():
    with pytest.raises(InvalidValueError):
        as_enum("bogus", OutputMode)
    with pytest.raises(InvalidValueError):
        as_enum(True, OutputMode)


def test_fmt_enum():
    assert fmt_enum("ACDC-INT", OutputMode) == "0"
    assert fmt_enum(VoltageRange.AUTO, VoltageRange) == "2"


def test_as_bool():
    assert as_bool("ON") is True
    assert as_bool("0") is False
    assert as_bool(1) is True
    with pytest.raises(InvalidValueError):
        as_bool("maybe")


def test_fmt_number():
    assert fmt_number(150.0) == "150.0"
    assert fmt_number(60) == "60.0"
    assert fmt_number("MIN") == "MIN"
    assert fmt_number("maximum") == "MAX"
