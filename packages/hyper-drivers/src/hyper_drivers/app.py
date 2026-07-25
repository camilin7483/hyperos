import logging, sys
from PySide6.QtWidgets import QApplication
from hyper_drivers.ui.main_window import MainWindow
from hyperos_core.ui.styles import load_stylesheet

def main() -> int:
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    app.setApplicationName("Hyper Drivers")
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
