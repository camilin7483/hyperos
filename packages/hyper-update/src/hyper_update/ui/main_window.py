import logging, subprocess
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget)

from hyperos_core.services.pacman import PacmanService

logger = logging.getLogger(__name__)


class _UpdateWorker(QObject):
    output = Signal(str)
    finished = Signal(bool)

    def __init__(self, cmd: list[str]) -> None:
        super().__init__()
        self._cmd = cmd

    def run(self) -> None:
        try:
            result = subprocess.run(self._cmd, capture_output=True, text=True, timeout=300)
            self.output.emit(result.stdout + result.stderr)
            self.finished.emit(result.returncode == 0)
        except Exception as e:
            self.output.emit(f"Error: {e}")
            self.finished.emit(False)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._pacman = PacmanService(sudo=True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Hyper Update")
        self.resize(800, 600)
        layout = QVBoxLayout()

        title = QLabel("System Update")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        self._check_btn = QPushButton("Check Updates")
        self._check_btn.setObjectName("primaryButton")
        self._check_btn.clicked.connect(self._check_updates)
        btn_layout.addWidget(self._check_btn)

        self._update_btn = QPushButton("Update All")
        self._update_btn.setObjectName("dangerButton")
        self._update_btn.clicked.connect(self._update_system)
        btn_layout.addWidget(self._update_btn)

        self._sync_btn = QPushButton("Sync Databases")
        self._sync_btn.setObjectName("secondaryButton")
        self._sync_btn.clicked.connect(self._sync_dbs)
        btn_layout.addWidget(self._sync_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setObjectName("hyperCard")
        layout.addWidget(self._output, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _check_updates(self) -> None:
        self._output.append("Checking for updates...")
        count = self._pacman.get_update_count()
        if count > 0:
            self._output.append(f"Found {count} update(s) available.")
        else:
            self._output.append("System is up to date.")

    def _update_system(self) -> None:
        self._run_cmd(["sudo", "pacman", "-Syu", "--noconfirm"])

    def _sync_dbs(self) -> None:
        self._run_cmd(["sudo", "pacman", "-Sy"])

    def _run_cmd(self, cmd: list[str]) -> None:
        self._output.clear()
        self._output.append(f"Running: {' '.join(cmd)}\n")
        self._thread = QThread(self)
        self._worker = _UpdateWorker(cmd)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.output.connect(lambda t: self._output.append(t))
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()
