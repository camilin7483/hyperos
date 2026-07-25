import logging, sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from hyper_update.ui.main_window import MainWindow
from hyperos_core.ui.styles import load_stylesheet

logger = logging.getLogger(__name__)

def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    app = QApplication(sys.argv)
    app.setApplicationName("Hyper Update")
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
