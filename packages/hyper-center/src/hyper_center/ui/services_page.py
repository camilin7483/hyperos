import logging
from typing import Optional

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QLabel, QPushButton,
                               QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from hyperos_core.domain.models import ServiceInfo
from hyperos_core.services.service_manager import ServiceManager

logger = logging.getLogger(__name__)


class _ServicesWorker(QObject):
    services_ready = Signal(list)
    finished = Signal()

    def __init__(self, manager: ServiceManager) -> None:
        super().__init__()
        self._manager = manager

    def run(self) -> None:
        services = self._manager.list_services()
        self.services_ready.emit(services)
        self.finished.emit()


class ServicesPage(QWidget):
    def __init__(self, service_manager: ServiceManager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._service_manager = service_manager
        self._services: list[ServiceInfo] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(12)

        title = QLabel("System Services")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Manage systemd services")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        btn_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.setObjectName("primaryButton")
        self._refresh_btn.clicked.connect(self.load_services)
        btn_layout.addWidget(self._refresh_btn)

        self._start_btn = QPushButton("Start")
        self._start_btn.setObjectName("secondaryButton")
        self._start_btn.clicked.connect(self._start_service)
        btn_layout.addWidget(self._start_btn)

        self._stop_btn = QPushButton("Stop")
        self._stop_btn.setObjectName("secondaryButton")
        self._stop_btn.clicked.connect(self._stop_service)
        btn_layout.addWidget(self._stop_btn)

        self._restart_btn = QPushButton("Restart")
        self._restart_btn.setObjectName("secondaryButton")
        self._restart_btn.clicked.connect(self._restart_service)
        btn_layout.addWidget(self._restart_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Service", "State", "Enabled", "Description"])
        self._tree.setAlternatingRowColors(False)
        self._tree.setRootIsDecorated(False)
        self._tree.setSortingEnabled(True)
        self._tree.header().setStretchLastSection(True)
        self._tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._tree)

    def load_services(self) -> None:
        self._thread = QThread(self)
        self._worker = _ServicesWorker(self._service_manager)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.services_ready.connect(self._on_services_ready)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_services_ready(self, services: list) -> None:
        self._services = services
        self._tree.clear()
        for svc in services:
            state_color = "active" if svc.running else "inactive"
            enabled = "enabled" if svc.enabled else "disabled"
            item = QTreeWidgetItem([svc.name, state_color, enabled, svc.description])
            self._tree.addTopLevelItem(item)

    def _start_service(self) -> None:
        selected = self._tree.currentItem()
        if selected:
            name = selected.text(0)
            self._service_manager.start(name)
            self.load_services()

    def _stop_service(self) -> None:
        selected = self._tree.currentItem()
        if selected:
            name = selected.text(0)
            self._service_manager.stop(name)
            self.load_services()

    def _restart_service(self) -> None:
        selected = self._tree.currentItem()
        if selected:
            name = selected.text(0)
            self._service_manager.restart(name)
            self.load_services()
