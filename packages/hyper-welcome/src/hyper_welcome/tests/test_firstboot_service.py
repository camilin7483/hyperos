"""Tests for FirstBootService."""

import json
from pathlib import Path

import pytest

from hyper_welcome.domain.enums import FirstBootState
from hyper_welcome.services.firstboot_service import FirstBootService


class TestFirstBootService:
    """Test suite for FirstBootService."""

    def setup_method(self) -> None:
        self.tmp_path = Path("/tmp/hyper_welcome_test_state.json")
        if self.tmp_path.exists():
            self.tmp_path.unlink()
        self.service = FirstBootService(state_path=self.tmp_path)

    def teardown_method(self) -> None:
        if self.tmp_path.exists():
            self.tmp_path.unlink()

    def test_default_state_is_pending(self) -> None:
        state = self.service.get_state()
        assert state == FirstBootState.PENDING

    def test_mark_completed_changes_state(self) -> None:
        self.service.mark_completed()
        state = self.service.get_state()
        assert state == FirstBootState.COMPLETED

    def test_mark_skipped_changes_state(self) -> None:
        self.service.mark_skipped()
        state = self.service.get_state()
        assert state == FirstBootState.SKIPPED

    def test_disable_permanently(self) -> None:
        self.service.disable()
        state = self.service.get_state()
        assert state == FirstBootState.DISABLED

    def test_reset_returns_to_pending(self) -> None:
        self.service.mark_completed()
        self.service.reset()
        state = self.service.get_state()
        assert state == FirstBootState.PENDING

    def test_is_first_boot_returns_true_when_pending(self) -> None:
        assert self.service.is_first_boot() is True

    def test_is_first_boot_returns_false_when_completed(self) -> None:
        self.service.mark_completed()
        assert self.service.is_first_boot() is False

    def test_state_file_contains_valid_json(self) -> None:
        self.service.mark_completed()
        assert self.tmp_path.exists()
        data = json.loads(self.tmp_path.read_text())
        assert data["state"] == "completed"
        assert data["version"] == 1

    def test_corrupted_state_file_returns_pending(self) -> None:
        self.tmp_path.write_text("invalid json")
        state = self.service.get_state()
        assert state == FirstBootState.PENDING
