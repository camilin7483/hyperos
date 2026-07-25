import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QLabel, QProgressBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from hyperos_core.domain.models import SystemInfo
from hyperos_core.widgets.card import Card

logger = logging.getLogger(__name__)


class StoragePage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Storage")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Disk usage and storage devices")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._root_card = Card("Root (/)")
        self._root_card.add_row("Total", "Loading...")
        self._root_card.add_row("Used", "Loading...")
        self._root_card.add_row("Usage", "Loading...")
        layout.addWidget(self._root_card)

        self._progress = QProgressBar()
        self._progress.setMinimum(0)
        self._progress.setMaximum(100)
        self._progress.setValue(0)
        self._progress.setTextVisible(True)
        layout.addWidget(self._progress)

        layout.addStretch()

    def update_info(self, info: SystemInfo) -> None:
        self._root_card = Card("Root (/)")
        self._root_card.add_row("Total", info.storage_total)
        self._root_card.add_row("Used", info.storage_used)
        self._root_card.add_row("Usage", f"{info.storage_percent}%")
        self._progress.setValue(int(info.storage_percent))
        self._progress.setFormat(f"{info.storage_percent}% used")
