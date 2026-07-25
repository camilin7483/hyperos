from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class Card(QFrame):
    def __init__(self, title: str = "", parent: Optional[QFrame] = None) -> None:
        super().__init__(parent)
        self._title = title
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("hyperCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        if self._title:
            title_label = QLabel(self._title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)

        self._content_layout = QVBoxLayout()
        self._content_layout.setSpacing(4)
        layout.addLayout(self._content_layout)

    def add_row(self, label: str, value: str) -> None:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 2, 0, 2)
        row_layout.setSpacing(8)

        lbl = QLabel(label)
        lbl.setObjectName("cardRowLabel")
        row_layout.addWidget(lbl)

        val = QLabel(value)
        val.setObjectName("cardRowValue")
        val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row_layout.addWidget(val, 1)

        self._content_layout.addWidget(row)


class MetricCard(QFrame):
    def __init__(self, label: str, value: str = "", icon: str = "", parent: Optional[QFrame] = None) -> None:
        super().__init__(parent)
        self._label = label
        self._value = value
        self._icon = icon
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("infoCard")
        self.setMinimumHeight(72)
        self.setMaximumHeight(92)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        if self._icon:
            icon_label = QLabel(self._icon)
            icon_label.setObjectName("infoCardIcon")
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setFixedSize(36, 36)
            layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title = QLabel(self._label)
        title.setObjectName("infoCardLabel")
        text_layout.addWidget(title)

        self._value_label = QLabel(self._value)
        self._value_label.setObjectName("infoCardValue")
        self._value_label.setWordWrap(False)
        text_layout.addWidget(self._value_label)

        layout.addLayout(text_layout, 1)

    def set_value(self, value: str) -> None:
        self._value = value
        self._value_label.setText(value)
