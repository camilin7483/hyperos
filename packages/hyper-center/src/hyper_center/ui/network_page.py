import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from hyperos_core.domain.models import SystemInfo
from hyperos_core.services.network import NetworkService
from hyperos_core.widgets.card import Card

logger = logging.getLogger(__name__)


class NetworkPage(QWidget):
    def __init__(self, network_service: NetworkService, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._network_service = network_service
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Network")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Network interfaces and connectivity")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._status_label = QLabel("Checking connectivity...")
        self._status_label.setObjectName("cardTitle")
        layout.addWidget(self._status_label)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Interface", "IP Address", "Status"])
        self._tree.setRootIsDecorated(False)
        self._tree.header().setStretchLastSection(True)
        self._tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._tree, 1)

    def update_info(self, info: SystemInfo) -> None:
        connected = self._network_service.check_connectivity()
        status_text = "Connected" if connected else "Disconnected"
        color = "#00C853" if connected else "#FF5252"
        self._status_label.setText(f"Internet: {status_text}")
        self._status_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")

        interfaces = self._network_service.get_network_interfaces()
        self._tree.clear()
        for iface in interfaces:
            item = QTreeWidgetItem([
                iface.interface,
                iface.ip_address or "N/A",
                "Active" if iface.connected else "Inactive",
            ])
            self._tree.addTopLevelItem(item)
