"""Main application window for Hyper Welcome."""

import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from hyper_welcome.services.system_service import SystemService
from hyper_welcome.services.network_service import NetworkService
from hyper_welcome.services.firstboot_service import FirstBootService
from hyper_welcome.ui.welcome_page import WelcomePage

logger = logging.getLogger(__name__)

WINDOW_TITLE = "HyperOS Welcome"
WINDOW_WIDTH = 860
WINDOW_HEIGHT = 620


class MainWindow(QMainWindow):
    """Main window for the HyperOS Welcome application."""

    def __init__(
        self,
        system_service: Optional[SystemService] = None,
        network_service: Optional[NetworkService] = None,
        firstboot_service: Optional[FirstBootService] = None,
    ) -> None:
        super().__init__()
        self._system_service = system_service or SystemService()
        self._network_service = network_service or NetworkService()
        self._firstboot_service = firstboot_service or FirstBootService()
        self._setup_window()
        self._setup_central_widget()

    def _setup_window(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

    def _setup_central_widget(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._welcome_page = WelcomePage(
            system_service=self._system_service,
            network_service=self._network_service,
        )
        layout.addWidget(self._welcome_page)

    def showEvent(self, event) -> None:
        """Called when the window is shown. Triggers data population."""
        super().showEvent(event)
        self._welcome_page.populate()

    def closeEvent(self, event) -> None:
        """Called when the window is closed. Stops worker and saves state."""
        self._welcome_page.stop()
        self._firstboot_service.mark_completed()
        logger.info("First-boot completed. Welcome screen will not appear again.")
        super().closeEvent(event)
