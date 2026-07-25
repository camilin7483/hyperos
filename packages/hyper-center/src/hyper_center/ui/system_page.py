import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from hyperos_core.domain.models import SystemInfo
from hyperos_core.widgets.card import Card

logger = logging.getLogger(__name__)


class SystemPage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._cards: list[Card] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("System Information")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Detailed hardware and software information")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(12)

        self._cpu_card = Card("CPU")
        self._cpu_card.add_row("Model", "-")
        self._cpu_card.add_row("Cores", "-")
        self._cpu_card.add_row("Usage", "-")
        grid.addWidget(self._cpu_card, 0, 0)
        self._cards.append(self._cpu_card)

        self._ram_card = Card("Memory")
        self._ram_card.add_row("Total", "-")
        self._ram_card.add_row("Used", "-")
        self._ram_card.add_row("Usage", "-")
        self._ram_card.add_row("Swap", "-")
        grid.addWidget(self._ram_card, 0, 1)
        self._cards.append(self._ram_card)

        self._gpu_card = Card("Graphics")
        self._gpu_card.add_row("GPU", "-")
        self._gpu_card.add_row("Driver", "-")
        grid.addWidget(self._gpu_card, 0, 2)
        self._cards.append(self._gpu_card)

        self._os_card = Card("Operating System")
        self._os_card.add_row("OS", "-")
        self._os_card.add_row("Version", "-")
        self._os_card.add_row("Kernel", "-")
        self._os_card.add_row("Hostname", "-")
        grid.addWidget(self._os_card, 1, 0)
        self._cards.append(self._os_card)

        self._uptime_card = Card("Uptime & Load")
        self._uptime_card.add_row("Uptime", "-")
        self._uptime_card.add_row("Processes", "-")
        self._uptime_card.add_row("Desktop", "-")
        grid.addWidget(self._uptime_card, 1, 1)
        self._cards.append(self._uptime_card)

        layout.addLayout(grid)
        layout.addStretch()

    def update_info(self, info: SystemInfo) -> None:
        self._cpu_card.setParent(None)
        self._cpu_card = Card("CPU")
        self._cpu_card.add_row("Model", info.cpu)
        self._cpu_card.add_row("Cores", str(info.cpu_cores))
        self._cpu_card.add_row("Usage", f"{info.cpu_usage}%")

        self._ram_card = Card("Memory")
        self._ram_card.add_row("Total", info.ram_total)
        self._ram_card.add_row("Used", info.ram_used)
        self._ram_card.add_row("Usage", f"{info.ram_percent}%")
        self._ram_card.add_row("Swap", info.swap_total)

        self._gpu_card = Card("Graphics")
        self._gpu_card.add_row("GPU", info.gpu)

        self._os_card = Card("Operating System")
        self._os_card.add_row("OS", info.os_name)
        self._os_card.add_row("Version", info.os_version)
        self._os_card.add_row("Kernel", info.kernel)
        self._os_card.add_row("Hostname", info.hostname)

        self._uptime_card = Card("Uptime & Load")
        self._uptime_card.add_row("Uptime", info.uptime)
        self._uptime_card.add_row("Processes", str(info.processes))
        self._uptime_card.add_row("Desktop", info.desktop)
