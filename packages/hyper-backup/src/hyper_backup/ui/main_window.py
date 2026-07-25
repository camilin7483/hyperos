import logging, subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget)

logger = logging.getLogger(__name__)


def _run_cmd(cmd: list[str]) -> tuple[str, bool]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr, result.returncode == 0
    except Exception as e:
        return str(e), False


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()
        self._check_snapshots()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Hyper Backup")
        self.resize(800, 600)
        layout = QVBoxLayout()

        title = QLabel("Backup Manager")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Btrfs snapshots and system restore points")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        btn_layout = QHBoxLayout()
        self._create_btn = QPushButton("Create Snapshot")
        self._create_btn.setObjectName("primaryButton")
        self._create_btn.clicked.connect(self._create_snapshot)
        btn_layout.addWidget(self._create_btn)

        self._list_btn = QPushButton("List Snapshots")
        self._list_btn.setObjectName("secondaryButton")
        self._list_btn.clicked.connect(self._list_snapshots)
        btn_layout.addWidget(self._list_btn)

        self._restore_btn = QPushButton("Restore")
        self._restore_btn.setObjectName("dangerButton")
        btn_layout.addWidget(self._restore_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setObjectName("hyperCard")
        layout.addWidget(self._output, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _check_snapshots(self) -> None:
        self._output.append("Checking for Btrfs snapshots...")
        out, ok = _run_cmd(["sudo", "snapper", "list", "--disable-hints"])
        if ok:
            self._output.append(out)
        else:
            self._output.append("No snapper config found or not a Btrfs system.")
            self._output.append("Hyper Backup requires Btrfs and snapper.")

    def _create_snapshot(self) -> None:
        self._output.clear()
        self._output.append("Creating snapshot...")
        out, ok = _run_cmd(["sudo", "snapper", "-c", "root", "create", "-d", "Hyper Backup"])
        self._output.append(out)
        if ok:
            self._output.append("Snapshot created.")
        self._list_snapshots()

    def _list_snapshots(self) -> None:
        self._output.clear()
        out, ok = _run_cmd(["sudo", "snapper", "-c", "root", "list", "--disable-hints"])
        self._output.append(out if ok else "No snapshots found or snapper not configured.")
