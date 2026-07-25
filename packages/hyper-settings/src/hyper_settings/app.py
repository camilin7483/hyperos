import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from hyper_settings.ui.main_window import MainWindow
from hyperos_core.ui.styles import load_stylesheet

logger = logging.getLogger(__name__)
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level, format=LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S", handlers=[logging.StreamHandler(sys.stderr)])


def create_app(argv: list[str] | None = None) -> QApplication:
    app = QApplication(argv or sys.argv)
    app.setApplicationName("Hyper Settings")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("HyperOS")
    app.setStyleSheet(load_stylesheet())
    return app


def main() -> int:
    setup_logging()
    logger.info("Starting Hyper Settings v0.1.0")
    app = create_app()
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
