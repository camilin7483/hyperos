"""Welcome page widget — the main content of the Hyper Welcome application."""

import logging
from typing import Optional

from PySide6.QtCore import QObject, QProcess, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from hyper_welcome.domain.models import SystemInfo, ConnectivityStatus
from hyper_welcome.services.system_service import SystemService
from hyper_welcome.services.network_service import NetworkService
from hyper_welcome.widgets.info_card import InfoCard
from hyper_welcome.widgets.status_indicator import StatusIndicator
from hyper_welcome.widgets.action_button import ActionButton

logger = logging.getLogger(__name__)

HYPEROS_VERSION = "0.1.0"
HYPEROS_BRAND = "#00AEEF"


class _SystemWorker(QObject):
    """Background worker for collecting system info and checking connectivity."""

    system_info_ready = Signal(SystemInfo)
    connectivity_ready = Signal(ConnectivityStatus)

    def __init__(
        self,
        system_service: SystemService,
        network_service: NetworkService,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._system_service = system_service
        self._network_service = network_service

    def run(self) -> None:
        info = self._system_service.collect()
        self.system_info_ready.emit(info)
        status = self._network_service.check_connectivity()
        self.connectivity_ready.emit(status)


class WelcomePage(QWidget):
    """Main welcome page widget displayed after first boot."""

    def __init__(
        self,
        system_service: SystemService,
        network_service: NetworkService,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._system_service = system_service
        self._network_service = network_service
        self._info_cards: list[InfoCard] = []
        self._worker_thread: Optional[QThread] = None
        self._worker: Optional[_SystemWorker] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._build_header(content_layout)
        self._build_system_grid(content_layout)
        self._build_actions(content_layout)

        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _build_header(self, parent: QVBoxLayout) -> None:
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        title = QLabel("Welcome to HyperOS")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)

        subtitle = QLabel("Arch Linux · Hyprland · Performance First")
        subtitle.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle)

        version = QLabel(f"Version {HYPEROS_VERSION}")
        version.setObjectName("versionLabel")
        header_layout.addWidget(version)

        self._status_indicator = StatusIndicator()
        header_layout.addWidget(self._status_indicator)

        parent.addWidget(header)

    def _build_system_grid(self, parent: QVBoxLayout) -> None:
        section = QLabel("System Information")
        section.setObjectName("sectionTitle")
        parent.addWidget(section)

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(8)
        grid.setContentsMargins(0, 0, 0, 0)

        info_items = [
            ("CPU", "", "\U0001F5A5"),
            ("RAM", "", "\U0001F4BE"),
            ("GPU", "", "\U0001F3AE"),
            ("Storage", "", "\U0001F4C0"),
            ("Kernel", "", "\U00002699"),
            ("Desktop", "", "\U0001F4BB"),
        ]

        for i, (label, value, icon) in enumerate(info_items):
            card = InfoCard(label, value, icon)
            self._info_cards.append(card)
            row, col = divmod(i, 3)
            grid.addWidget(card, row, col)

        parent.addWidget(grid_widget)

    def _build_actions(self, parent: QVBoxLayout) -> None:
        section = QLabel("Getting Started")
        section.setObjectName("sectionTitle")
        parent.addWidget(section)

        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        buttons_data = [
            ("Open Hyper Center", False, "hyper-center"),
            ("Install Software", False, "hyper-store"),
            ("Documentation", False, "https://hyperos.org/docs"),
            ("GitHub", False, "https://github.com/hyperos/hyperos"),
            ("Settings", False, "hyper-settings"),
        ]

        for text, primary, target in buttons_data:
            btn = ActionButton(text, primary=primary)
            btn.clicked.connect(lambda checked=False, t=target: self._handle_action(t))
            actions_layout.addWidget(btn)

        exit_btn = ActionButton("Exit", primary=True)
        exit_btn.clicked.connect(self._on_exit_clicked)
        actions_layout.addWidget(exit_btn)

        parent.addWidget(actions_widget)

    @staticmethod
    def _handle_action(target: str) -> None:
        if target.startswith("http://") or target.startswith("https://"):
            QDesktopServices.openUrl(QUrl(target))
        else:
            QProcess.startDetached(target)

    def populate(self) -> None:
        """Load system information and check connectivity in a background thread."""
        logger.info("Populating system information...")

        self._worker_thread = QThread(self)
        self._worker = _SystemWorker(
            self._system_service,
            self._network_service,
        )
        self._worker.moveToThread(self._worker_thread)

        self._worker_thread.started.connect(self._worker.run)
        self._worker.system_info_ready.connect(self._on_system_info_ready)
        self._worker.connectivity_ready.connect(self._on_connectivity_ready)
        self._worker.connectivity_ready.connect(self._cleanup_worker)
        self._worker_thread.start()

    def _on_system_info_ready(self, info: SystemInfo) -> None:
        card_values = [
            (0, self._format_cpu(info)),
            (1, f"{info.ram_total} ({info.ram_percent}% used)"),
            (2, info.gpu),
            (3, f"{info.storage_total} ({info.storage_percent}% used)"),
            (4, info.kernel),
            (5, info.desktop),
        ]
        for card_index, value in card_values:
            if card_index < len(self._info_cards):
                self._info_cards[card_index].set_value(value)

    def _on_connectivity_ready(self, status: ConnectivityStatus) -> None:
        self._status_indicator.set_connected(status.connected)
        if status.connected:
            logger.info("Internet connectivity: connected")
        else:
            logger.info("Internet connectivity: not connected")

    def _cleanup_worker(self) -> None:
        if self._worker_thread is not None:
            self._worker_thread.quit()
            self._worker_thread.wait()
        self._worker = None
        self._worker_thread = None

    def stop(self) -> None:
        """Stop the background worker thread if running."""
        if self._worker_thread is not None and self._worker_thread.isRunning():
            self._worker_thread.quit()
            self._worker_thread.wait(2000)
        self._worker = None
        self._worker_thread = None

    def _on_exit_clicked(self) -> None:
        logger.info("Exit requested by user")
        window = self.window()
        if window is not None:
            window.close()

    @staticmethod
    def _format_cpu(info: SystemInfo) -> str:
        if info.cpu_cores > 0:
            return f"{info.cpu} ({info.cpu_cores} cores)"
        return info.cpu
