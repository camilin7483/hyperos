from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


class SidebarButton(QPushButton):
    def __init__(self, text: str, icon: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("sidebarButton")
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)


class Sidebar(QFrame):
    section_changed = Signal(str)

    def __init__(self, parent: Optional[QFrame] = None) -> None:
        super().__init__(parent)
        self._buttons: list[SidebarButton] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(2)

        logo = QLabel("HyperOS")
        logo.setObjectName("sidebarLogo")
        layout.addWidget(logo)
        layout.addSpacing(16)

        self._sections: list[tuple[str, str]] = []

    def add_section(self, name: str, label: str, icon: str = "") -> None:
        btn = SidebarButton(f"  {label}")
        btn.clicked.connect(lambda: self._on_section_clicked(name, btn))
        self._buttons.append(btn)
        self.layout().addWidget(btn)

    def add_separator(self) -> None:
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("sidebarSeparator")
        self.layout().addWidget(sep)

    def add_spacing(self, space: int = 8) -> None:
        self.layout().addSpacing(space)

    def _on_section_clicked(self, name: str, btn: SidebarButton) -> None:
        for b in self._buttons:
            b.setChecked(b is btn)
        self.section_changed.emit(name)

    def select(self, name: str) -> None:
        for btn in self._buttons:
            if btn.text().strip() == name:
                btn.setChecked(True)
            else:
                btn.setChecked(False)
