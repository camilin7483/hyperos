"""Application entry point for Hyper Welcome."""

import logging
import sys
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from hyper_welcome.services.firstboot_service import FirstBootService
from hyper_welcome.ui.main_window import MainWindow
from hyper_welcome.ui.styles import load_stylesheet

logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stderr),
        ],
    )


def create_app(argv: Optional[list[str]] = None) -> QApplication:
    """Create and configure the QApplication instance."""
    app = QApplication(argv or sys.argv)
    app.setApplicationName("Hyper Welcome")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("HyperOS")

    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)

    return app


def should_show_welcome() -> bool:
    """Determine whether the welcome screen should appear."""
    service = FirstBootService()
    return service.is_first_boot()


def main() -> int:
    """Main entry point for the Hyper Welcome application."""
    setup_logging()
    logger.info("Starting Hyper Welcome v0.1.0")

    if not should_show_welcome():
        logger.info("Welcome already completed. Exiting.")
        return 0

    app = create_app()
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
