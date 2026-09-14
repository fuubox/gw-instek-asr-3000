"""Test the hazardous integration-test collection gate without hardware."""

from __future__ import annotations

from types import SimpleNamespace

from tests.integration import conftest


class FakeItem:
    def __init__(self, hazardous: bool) -> None:
        self.hazardous = hazardous
        self.markers = []

    def get_closest_marker(self, name: str):
        return object() if name == "hazardous" and self.hazardous else None

    def add_marker(self, marker) -> None:
        self.markers.append(marker)


def test_host_alone_skips_hazardous_but_keeps_read_only_eligible():
    hazardous = FakeItem(True)
    readonly = FakeItem(False)
    config = SimpleNamespace(getoption=lambda name: False)

    conftest.pytest_collection_modifyitems(config, [readonly, hazardous])

    assert len(hazardous.markers) == 1
    assert len(readonly.markers) == 0


def test_allow_output_enables_hazardous_checklist():
    hazardous = FakeItem(True)
    config = SimpleNamespace(getoption=lambda name: name == "--allow-output")

    conftest.pytest_collection_modifyitems(config, [hazardous])

    assert hazardous.markers == []


def test_non_interactive_does_not_authorize_output():
    hazardous = FakeItem(True)
    config = SimpleNamespace(getoption=lambda name: name == "--non-interactive")

    conftest.pytest_collection_modifyitems(config, [hazardous])

    assert len(hazardous.markers) == 1
