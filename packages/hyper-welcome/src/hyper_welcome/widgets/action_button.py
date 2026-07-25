"""Styled action button widget."""

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class ActionButton(QPushButton):
    """A styled button using the HyperOS theme."""

    def __init__(
        self,
        text: str,
        icon: Optional[QIcon] = None,
        primary: bool = False,
        parent: Optional[QPushButton] = None,
    ) -> None:
        super().__init__(text, parent)
        self._primary = primary
        if icon is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        self._apply_style()

    def _apply_style(self) -> None:
        self.setObjectName("actionButtonPrimary" if self._primary else "actionButton")
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
