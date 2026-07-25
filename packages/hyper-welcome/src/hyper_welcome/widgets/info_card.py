"""Info card widget for displaying system information."""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class InfoCard(QFrame):
    """A styled card displaying a system information entry."""

    def __init__(
        self,
        label: str,
        value: str = "",
        icon_text: str = "",
        parent: Optional[QFrame] = None,
    ) -> None:
        super().__init__(parent)
        self._label = label
        self._value = value
        self._icon_text = icon_text
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setObjectName("infoCard")
        self.setMinimumHeight(72)
        self.setMaximumHeight(92)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        if self._icon_text:
            icon_label = QLabel(self._icon_text)
            icon_label.setObjectName("infoCardIcon")
            icon_font = QFont("monospace", 18)
            icon_label.setFont(icon_font)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setFixedSize(36, 36)
            layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(self._label)
        title_label.setObjectName("infoCardLabel")
        title_font = QFont("sans-serif", 9)
        title_label.setFont(title_font)
        text_layout.addWidget(title_label)

        self._value_label = QLabel(self._value)
        self._value_label.setObjectName("infoCardValue")
        value_font = QFont("sans-serif", 12, QFont.Weight.Bold)
        self._value_label.setFont(value_font)
        self._value_label.setWordWrap(False)
        text_layout.addWidget(self._value_label)

        layout.addLayout(text_layout, 1)

    def set_value(self, value: str) -> None:
        """Update the displayed value."""
        self._value = value
        self._value_label.setText(value)
