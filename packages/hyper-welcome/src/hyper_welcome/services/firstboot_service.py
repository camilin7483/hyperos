"""Service for managing first-boot state."""

import json
import logging
import os
from pathlib import Path

from hyper_welcome.domain.enums import FirstBootState

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "hyperos"
STATE_FILE = CONFIG_DIR / "hyper-welcome.state"


class FirstBootService:
    """Manages whether the welcome screen should appear."""

    def __init__(self, state_path: Path = STATE_FILE) -> None:
        self._state_path = state_path

    def get_state(self) -> FirstBootState:
        """Read the current first-boot state."""
        try:
            if self._state_path.exists():
                data = json.loads(self._state_path.read_text())
                state_str = data.get("state", "completed")
                return FirstBootState[state_str.upper()]
        except (json.JSONDecodeError, KeyError, PermissionError) as e:
            logger.warning("Failed to read first-boot state: %s", e)
        return FirstBootState.PENDING

    def mark_completed(self) -> None:
        """Mark the first-boot flow as completed."""
        self._write_state(FirstBootState.COMPLETED)

    def mark_skipped(self) -> None:
        """Mark the first-boot flow as skipped (will still show next time)."""
        self._write_state(FirstBootState.SKIPPED)

    def reset(self) -> None:
        """Reset the state to pending (for testing/re-enabling)."""
        self._write_state(FirstBootState.PENDING)

    def disable(self) -> None:
        """Permanently disable the welcome screen."""
        self._write_state(FirstBootState.DISABLED)

    def is_first_boot(self) -> bool:
        """Check if this is the first boot (welcome should appear)."""
        state = self.get_state()
        return state == FirstBootState.PENDING

    def _write_state(self, state: FirstBootState) -> None:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            data = {"state": state.name.lower(), "version": 1}
            self._state_path.write_text(json.dumps(data, indent=2))
            os.chmod(self._state_path, 0o600)
            logger.info("First-boot state written: %s", state.name)
        except (OSError, PermissionError) as e:
            logger.error("Failed to write first-boot state: %s", e)
