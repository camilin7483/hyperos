import logging
from typing import Optional

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QPushButton, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget)

from hyperos_core.domain.models import PackageInfo
from hyperos_core.services.pacman import PacmanService

logger = logging.getLogger(__name__)


class _PackageWorker(QObject):
    packages_ready = Signal(list)
    count_ready = Signal(int)
    updates_ready = Signal(int)
    finished = Signal()

    def __init__(self, service: PacmanService) -> None:
        super().__init__()
        self._service = service

    def run(self) -> None:
        packages = self._service.get_installed_packages()
        self.packages_ready.emit(packages)
        self.count_ready.emit(len(packages))
        updates = self._service.get_update_count()
        self.updates_ready.emit(updates)
        self.finished.emit()


class PackagesPage(QWidget):
    def __init__(self, pacman_service: PacmanService, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._pacman_service = pacman_service
        self._packages: list[PackageInfo] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(12)

        title = QLabel("Installed Packages")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        self._summary = QLabel("Loading packages...")
        self._summary.setObjectName("pageSubtitle")
        layout.addWidget(self._summary)

        search_layout = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search packages...")
        self._search_input.textChanged.connect(self._filter_packages)
        search_layout.addWidget(self._search_input)

        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.setObjectName("primaryButton")
        self._refresh_btn.clicked.connect(self.load_packages)
        search_layout.addWidget(self._refresh_btn)
        layout.addLayout(search_layout)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Package", "Version", "Size"])
        self._tree.setAlternatingRowColors(False)
        self._tree.setRootIsDecorated(False)
        self._tree.setSortingEnabled(True)
        self._tree.header().setStretchLastSection(True)
        self._tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._tree)

    def load_packages(self) -> None:
        self._summary.setText("Loading packages...")
        self._thread = QThread(self)
        self._worker = _PackageWorker(self._pacman_service)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.packages_ready.connect(self._on_packages_ready)
        self._worker.count_ready.connect(self._on_count_ready)
        self._worker.updates_ready.connect(self._on_updates_ready)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_packages_ready(self, packages: list) -> None:
        self._packages = packages
        self._populate_tree(packages)

    def _on_count_ready(self, count: int) -> None:
        self._total_count = count

    def _on_updates_ready(self, updates: int) -> None:
        summary = f"{self._total_count} packages installed"
        if updates > 0:
            summary += f" | {updates} updates available"
        self._summary.setText(summary)

    def _populate_tree(self, packages: list[PackageInfo]) -> None:
        self._tree.clear()
        for pkg in packages:
            item = QTreeWidgetItem([pkg.name, pkg.version, pkg.size])
            self._tree.addTopLevelItem(item)

    def _filter_packages(self, text: str) -> None:
        self._tree.clear()
        filtered = [p for p in self._packages if text.lower() in p.name.lower()]
        self._populate_tree(filtered)
