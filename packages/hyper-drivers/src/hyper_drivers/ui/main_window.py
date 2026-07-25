import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget)

from hyperos_core.services.hardware import HardwareService
from hyperos_core.widgets.card import Card

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._hardware = HardwareService()
        self._setup_ui()
        self._detect()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Hyper Drivers")
        self.resize(800, 600)
        layout = QVBoxLayout()

        title = QLabel("Driver Manager")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Hardware detection and driver management")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._gpu_card = Card("Graphics Driver")
        self._gpu_card.add_row("Vendor", "Detecting...")
        self._gpu_card.add_row("Driver", "Detecting...")
        self._gpu_card.add_row("NVIDIA Prime", "N/A")
        layout.addWidget(self._gpu_card)

        self._modules_card = Card("Kernel Modules")
        self._modules_card.add_row("Loaded modules", "Detecting...")
        layout.addWidget(self._modules_card)

        self._firmware_card = Card("Firmware")
        self._firmware_card.add_row("Status", "Detecting...")
        layout.addWidget(self._firmware_card)

        self._bluetooth_card = Card("Bluetooth")
        self._bluetooth_card.add_row("Status", "Detecting...")
        layout.addWidget(self._bluetooth_card)

        self._printer_card = Card("Printers")
        self._printer_card.add_row("Detected", "Detecting...")
        layout.addWidget(self._printer_card)

        refresh = QPushButton("Refresh Detection")
        refresh.setObjectName("primaryButton")
        refresh.clicked.connect(self._detect)
        layout.addWidget(refresh)

        layout.addStretch()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _detect(self) -> None:
        vendor = self._hardware.detect_gpu_driver()
        driver_info = ""
        if vendor == "nvidia":
            ver = self._hardware.get_nvidia_version()
            driver_info = f"NVIDIA {ver}" if ver else "NVIDIA (proprietary)"
        elif vendor == "amd":
            driver_info = "AMD (open-source)"
        elif vendor == "intel":
            driver_info = "Intel (open-source)"
        else:
            driver_info = "Unknown (basic VESA)"

        self._gpu_card = Card("Graphics Driver")
        self._gpu_card.add_row("Vendor", vendor.upper())
        self._gpu_card.add_row("Driver", driver_info)
        self._gpu_card.add_row("NVIDIA Prime", "Yes" if self._hardware.is_nvidia_prime() else "No/Unsupported")

        modules = self._hardware.get_kernel_modules()
        self._modules_card = Card("Kernel Modules")
        self._modules_card.add_row("Loaded modules", str(len(modules)))

        firmware = self._hardware.get_firmware_info()
        self._firmware_card = Card("Firmware")
        self._firmware_card.add_row("Status", f"{len(firmware)} device(s) with firmware" if firmware else "No fwupd support")

        bt = self._hardware.detect_bluetooth()
        self._bluetooth_card = Card("Bluetooth")
        self._bluetooth_card.add_row("Status", "Available" if bt else "Not detected")

        printers = self._hardware.detect_printers()
        self._printer_card = Card("Printers")
        self._printer_card.add_row("Detected", str(len(printers)))

        logger.info("Hardware detection complete: vendor=%s, modules=%d, fw=%d, bt=%s, printers=%d",
                     vendor, len(modules), len(firmware), bt, len(printers))
