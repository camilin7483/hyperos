import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from hyperos_core.domain.models import SystemInfo
from hyperos_core.widgets.card import MetricCard

logger = logging.getLogger(__name__)


class DashboardPage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._cards: list[MetricCard] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("System overview at a glance")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(12)

        items = [
            ("CPU", "Loading...", "\U0001F5A5"),
            ("RAM", "Loading...", "\U0001F4BE"),
            ("GPU", "Loading...", "\U0001F3AE"),
            ("Storage", "Loading...", "\U0001F4C0"),
            ("Kernel", "Loading...", "\U00002699"),
            ("Desktop", "Loading...", "\U0001F4BB"),
        ]

        for i, (label, value, icon) in enumerate(items):
            card = MetricCard(label, value, icon)
            self._cards.append(card)
            row, col = divmod(i, 3)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()

    def update_info(self, info: SystemInfo) -> None:
        values = [
            f"{info.cpu} ({info.cpu_cores} cores, {info.cpu_usage}%)",
            f"{info.ram_total} ({info.ram_percent}% used)",
            info.gpu,
            f"{info.storage_total} ({info.storage_percent}% used)",
            info.kernel,
            info.desktop,
        ]
        for card, value in zip(self._cards, values):
            card.set_value(value)
