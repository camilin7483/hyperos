"""Status indicator widget for connectivity display."""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class StatusDot(QWidget):
    """A small colored dot indicating a status."""

    def __init__(self, color: str = "#555555", size: int = 12, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        self._dot_size = size
        self.setFixedSize(size + 4, size + 4)

    def set_color(self, color: str) -> None:
        """Change the dot color."""
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the colored dot."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        offset = 2
        painter.drawEllipse(offset, offset, self._dot_size, self._dot_size)


class StatusIndicator(QWidget):
    """A widget that shows connection status with a colored dot and label."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._dot = StatusDot("#555555")
        layout.addWidget(self._dot)

        self._label = QLabel("Checking connection...")
        self._label.setObjectName("statusLabel")
        layout.addWidget(self._label)

        layout.addStretch()

    def set_connected(self, connected: bool) -> None:
        """Update the indicator to show connected or disconnected state."""
        if connected:
            self._dot.set_color("#00C853")
            self._label.setText("Connected")
            self._label.setStyleSheet("color: #00C853;")
        else:
            self._dot.set_color("#FF5252")
            self._label.setText("No connection")
            self._label.setStyleSheet("color: #FF5252;")
