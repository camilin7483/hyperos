import logging
from typing import Optional

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from hyperos_core.domain.models import SystemInfo
from hyperos_core.services.system import SystemService
from hyperos_core.services.network import NetworkService
from hyperos_core.services.pacman import PacmanService
from hyperos_core.services.service_manager import ServiceManager
from hyperos_core.services.hardware import HardwareService
from hyperos_core.services.power import PowerService
from hyperos_core.widgets.sidebar import Sidebar

from hyper_center.ui.dashboard_page import DashboardPage
from hyper_center.ui.system_page import SystemPage
from hyper_center.ui.packages_page import PackagesPage
from hyper_center.ui.services_page import ServicesPage
from hyper_center.ui.network_page import NetworkPage
from hyper_center.ui.storage_page import StoragePage
from hyper_center.ui.profiles_page import ProfilesPage

logger = logging.getLogger(__name__)

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Hyper Center"


class _DataWorker(QObject):
    data_ready = Signal(SystemInfo)
    finished = Signal()

    def __init__(self, system_service: SystemService) -> None:
        super().__init__()
        self._system_service = system_service

    def run(self) -> None:
        info = self._system_service.collect()
        self.data_ready.emit(info)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._system_service = SystemService()
        self._network_service = NetworkService()
        self._pacman_service = PacmanService()
        self._service_manager = ServiceManager()
        self._hardware_service = HardwareService()
        self._power_service = PowerService()

        self._setup_window()
        self._setup_central_widget()
        self._collect_data()

    def _setup_window(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(900, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

    def _setup_central_widget(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._setup_sidebar()
        layout.addWidget(self._sidebar)

        self._stack = QStackedWidget()
        layout.addWidget(self._stack, 1)

        self._dashboard_page = DashboardPage()
        self._system_page = SystemPage()
        self._packages_page = PackagesPage(self._pacman_service)
        self._services_page = ServicesPage(self._service_manager)
        self._network_page = NetworkPage(self._network_service)
        self._storage_page = StoragePage()
        self._profiles_page = ProfilesPage(self._power_service)

        self._stack.addWidget(self._dashboard_page)     # 0
        self._stack.addWidget(self._system_page)         # 1
        self._stack.addWidget(self._packages_page)       # 2
        self._stack.addWidget(self._services_page)       # 3
        self._stack.addWidget(self._network_page)        # 4
        self._stack.addWidget(self._storage_page)        # 5
        self._stack.addWidget(self._profiles_page)       # 6

    def _setup_sidebar(self) -> None:
        self._sidebar.add_section("dashboard", "Dashboard")
        self._sidebar.add_section("system", "System")
        self._sidebar.add_section("packages", "Packages")
        self._sidebar.add_section("services", "Services")
        self._sidebar.add_section("network", "Network")
        self._sidebar.add_section("storage", "Storage")
        self._sidebar.add_section("profiles", "Profiles")
        self._sidebar.section_changed.connect(self._on_section_changed)
        self._sidebar.select("dashboard")

    def _on_section_changed(self, section: str) -> None:
        index_map = {
            "dashboard": 0, "system": 1, "packages": 2,
            "services": 3, "network": 4, "storage": 5, "profiles": 6,
        }
        idx = index_map.get(section, 0)
        self._stack.setCurrentIndex(idx)

    def _collect_data(self) -> None:
        self._thread = QThread(self)
        self._worker = _DataWorker(self._system_service)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.data_ready.connect(self._on_data_ready)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

        self._packages_page.load_packages()
        self._services_page.load_services()

    def _on_data_ready(self, info: SystemInfo) -> None:
        self._dashboard_page.update_info(info)
        self._system_page.update_info(info)
        self._storage_page.update_info(info)
        self._network_page.update_info(info)
        logger.info("System info loaded")

    def closeEvent(self, event) -> None:
        try:
            if hasattr(self, '_thread') and self._thread is not None:
                if self._thread.isRunning():
                    self._thread.quit()
                    self._thread.wait(2000)
        except RuntimeError:
            pass
        super().closeEvent(event)
