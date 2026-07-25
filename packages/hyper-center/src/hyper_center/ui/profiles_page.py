import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton, QVBoxLayout,
                               QWidget)

from hyperos_core.domain.models import PowerProfile
from hyperos_core.services.power import PowerService

logger = logging.getLogger(__name__)


class ProfileCard(QWidget):
    def __init__(self, profile: PowerProfile, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._profile = profile
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("infoCard")
        self.setMinimumHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        name = QLabel(self._profile.label)
        name.setObjectName("cardTitle")
        layout.addWidget(name)

        desc = QLabel(self._profile.description)
        desc.setObjectName("cardRowLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        details = QLabel(
            f"Governor: {self._profile.cpu_governor}  |  "
            f"Swappiness: {self._profile.swappiness}  |  "
            f"Screen: {self._profile.screen_timeout}s"
        )
        details.setObjectName("cardRowValue")
        layout.addWidget(details)

        if self._profile.is_active:
            active_label = QLabel("Active")
            active_label.setStyleSheet("color: #00C853; font-weight: bold; font-size: 12px;")
            layout.addWidget(active_label)


class ProfilesPage(QWidget):
    def __init__(self, power_service: PowerService, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._power_service = power_service
        self._cards: list[ProfileCard] = []
        self._setup_ui()
        self._load_profiles()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Performance Profiles")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Switch between power and performance modes")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._grid = QGridLayout()
        self._grid.setSpacing(12)
        layout.addLayout(self._grid)
        layout.addStretch()

    def _load_profiles(self) -> None:
        profiles = self._power_service.get_profiles()
        for i, profile in enumerate(profiles):
            card = ProfileCard(profile)
            self._cards.append(card)
            row, col = divmod(i, 2)
            self._grid.addWidget(card, row, col)
