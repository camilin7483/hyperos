import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QWidget)

from hyperos_core.services.pacman import PacmanService

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._pacman = PacmanService(sudo=True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Hyper Store")
        self.resize(900, 650)
        layout = QVBoxLayout()

        title = QLabel("Hyper Store")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search packages (press Enter)...")
        self._search_input.returnPressed.connect(self._search)
        search_layout.addWidget(self._search_input)

        self._search_btn = QPushButton("Search")
        self._search_btn.setObjectName("primaryButton")
        self._search_btn.clicked.connect(self._search)
        search_layout.addWidget(self._search_btn)

        self._installed_btn = QPushButton("Show Installed")
        self._installed_btn.setObjectName("secondaryButton")
        self._installed_btn.clicked.connect(self._show_installed)
        search_layout.addWidget(self._installed_btn)

        layout.addLayout(search_layout)

        action_layout = QHBoxLayout()
        self._install_btn = QPushButton("Install")
        self._install_btn.setObjectName("primaryButton")
        self._install_btn.clicked.connect(self._install_pkg)
        action_layout.addWidget(self._install_btn)

        self._remove_btn = QPushButton("Remove")
        self._remove_btn.setObjectName("dangerButton")
        self._remove_btn.clicked.connect(self._remove_pkg)
        action_layout.addWidget(self._remove_btn)

        self._status_label = QLabel("")
        action_layout.addWidget(self._status_label, 1)
        layout.addLayout(action_layout)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Package", "Version", "Repository", "Status"])
        self._tree.setRootIsDecorated(False)
        self._tree.setSortingEnabled(True)
        self._tree.header().setStretchLastSection(True)
        self._tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        layout.addWidget(self._tree, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _search(self) -> None:
        query = self._search_input.text().strip()
        if not query:
            return
        self._status_label.setText("Searching...")
        self._tree.clear()
        try:
            results = self._pacman.search_packages(query)
            for pkg in results[:100]:
                item = QTreeWidgetItem([pkg.name, pkg.version, pkg.repository or "", "Available"])
                self._tree.addTopLevelItem(item)
            self._status_label.setText(f"Found {len(results)} packages")
        except Exception as e:
            self._status_label.setText(f"Search failed: {e}")

    def _show_installed(self) -> None:
        self._status_label.setText("Loading...")
        self._tree.clear()
        try:
            pkgs = self._pacman.get_installed_packages()
            for pkg in pkgs:
                item = QTreeWidgetItem([pkg.name, pkg.version, pkg.repository or "", "Installed"])
                self._tree.addTopLevelItem(item)
            self._status_label.setText(f"{len(pkgs)} packages installed")
        except Exception as e:
            self._status_label.setText(f"Failed: {e}")

    def _install_pkg(self) -> None:
        selected = self._tree.currentItem()
        if selected:
            name = selected.text(0)
            self._status_label.setText(f"Installing {name}...")
            ok = self._pacman.install(name)
            self._status_label.setText(f"{'Installed' if ok else 'Failed'}: {name}")
            if ok:
                self._show_installed()

    def _remove_pkg(self) -> None:
        selected = self._tree.currentItem()
        if selected:
            name = selected.text(0)
            self._status_label.setText(f"Removing {name}...")
            ok = self._pacman.remove(name)
            self._status_label.setText(f"{'Removed' if ok else 'Failed'}: {name}")
            if ok:
                self._show_installed()
