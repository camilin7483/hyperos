import logging
import subprocess
from typing import Optional

from PySide6.QtCore import Qt, QProcess
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QSlider,
                               QStackedWidget, QVBoxLayout, QWidget)

from hyperos_core.widgets.sidebar import Sidebar

logger = logging.getLogger(__name__)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 680
WINDOW_TITLE = "Hyper Settings"


class SettingsPage(QWidget):
    def __init__(self, title: str, description: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        t = QLabel(title)
        t.setObjectName("pageTitle")
        layout.addWidget(t)

        d = QLabel(description)
        d.setObjectName("pageSubtitle")
        layout.addWidget(d)

        self._content = QVBoxLayout()
        self._content.setSpacing(12)
        layout.addLayout(self._content)
        layout.addStretch()

    def add_widget(self, widget: QWidget) -> None:
        self._content.addWidget(widget)


class AppearancePage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Appearance", "Customize the look and feel of HyperOS")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QComboBox, QPushButton

        theme = QComboBox()
        theme.addItems(["HyperOS Dark", "HyperOS Light", "System Default"])
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Theme"))
        wl.addWidget(theme, 1)
        self.add_widget(w)

        wallpaper_btn = QPushButton("Change Wallpaper")
        wallpaper_btn.setObjectName("secondaryButton")
        wallpaper_btn.clicked.connect(lambda: QProcess.startDetached("hyprpaper"))
        self.add_widget(wallpaper_btn)


class DisplayPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Display", "Screen resolution and brightness settings")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QPushButton, QSlider

        brightness = QSlider(Qt.Orientation.Horizontal)
        brightness.setRange(10, 100)
        brightness.setValue(80)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Brightness"))
        wl.addWidget(brightness, 1)
        self.add_widget(w)

        calibrate = QPushButton("Calibrate Display")
        calibrate.setObjectName("secondaryButton")
        self.add_widget(calibrate)


class AudioPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Audio", "Volume, input and output devices")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QPushButton, QSlider

        volume = QSlider(Qt.Orientation.Horizontal)
        volume.setRange(0, 100)
        volume.setValue(75)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Volume"))
        wl.addWidget(volume, 1)
        self.add_widget(w)

        mixer = QPushButton("Open Audio Mixer")
        mixer.setObjectName("secondaryButton")
        mixer.clicked.connect(lambda: QProcess.startDetached("pavucontrol"))
        self.add_widget(mixer)


class NetworkPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Network", "WiFi, Ethernet and VPN settings")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QPushButton

        nm = QPushButton("Open Network Manager")
        nm.setObjectName("primaryButton")
        nm.clicked.connect(lambda: QProcess.startDetached("nm-connection-editor"))
        self.add_widget(nm)

        wifi = QPushButton("Select WiFi Network")
        wifi.setObjectName("secondaryButton")
        wifi.clicked.connect(lambda: QProcess.startDetached("nmcli", ["device", "wifi", "list"]))
        self.add_widget(wifi)


class PowerPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Power", "Battery and power management")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QComboBox, QSlider

        timeout = QSlider(Qt.Orientation.Horizontal)
        timeout.setRange(1, 30)
        timeout.setValue(5)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Sleep after (min)"))
        wl.addWidget(timeout, 1)
        self.add_widget(w)


class KeyboardPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Keyboard", "Keyboard layout and shortcuts")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QComboBox, QPushButton

        layout = QComboBox()
        layout.addItems(["US", "US (International)", "ES", "DE", "FR", "JP"])
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Layout"))
        wl.addWidget(layout, 1)
        self.add_widget(w)

        shortcuts = QPushButton("Configure Shortcuts")
        shortcuts.setObjectName("secondaryButton")
        self.add_widget(shortcuts)


class MousePage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Mouse", "Pointer speed and behavior")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QCheckBox, QSlider

        speed = QSlider(Qt.Orientation.Horizontal)
        speed.setRange(-10, 10)
        speed.setValue(0)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Speed"))
        wl.addWidget(speed, 1)
        self.add_widget(w)

        natural = QCheckBox("Natural scrolling")
        self.add_widget(natural)

        tap = QCheckBox("Tap to click")
        self.add_widget(tap)


class UsersPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Users", "User accounts and passwords")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QPushButton

        add = QPushButton("Add User")
        add.setObjectName("primaryButton")
        self.add_widget(add)

        pw = QPushButton("Change Password")
        pw.setObjectName("secondaryButton")
        pw.clicked.connect(lambda: QProcess.startDetached("passwd"))
        self.add_widget(pw)


class LanguagePage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Language", "System language and regional settings")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QComboBox

        lang = QComboBox()
        lang.addItems(["English (US)", "Español (CO)", "Français", "Deutsch", "日本語"])
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Language"))
        wl.addWidget(lang, 1)
        self.add_widget(w)

        fmt = QComboBox()
        fmt.addItems(["US (12h, °F)", "Metric (24h, °C)", "Custom"])
        w2 = QWidget()
        w2l = QHBoxLayout(w2)
        w2l.setContentsMargins(0, 0, 0, 0)
        w2l.addWidget(QLabel("Format"))
        w2l.addWidget(fmt, 1)
        self.add_widget(w2)


class PrivacyPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Privacy", "Privacy and security settings")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QCheckBox

        self.add_widget(QCheckBox("Disable screen locking"))
        self.add_widget(QCheckBox("Disable telemetry"))
        self.add_widget(QCheckBox("Enable firewall"))
        self.add_widget(QCheckBox("Disable Bluetooth discovery"))
        self.add_widget(QCheckBox("Clear clipboard on lock"))


class AccessibilityPage(SettingsPage):
    def __init__(self) -> None:
        super().__init__("Accessibility", "Accessibility features")
        self._setup()

    def _setup(self) -> None:
        from PySide6.QtWidgets import QCheckBox, QSlider

        self.add_widget(QCheckBox("Screen reader"))
        self.add_widget(QCheckBox("Sticky keys"))

        size = QSlider(Qt.Orientation.Horizontal)
        size.setRange(100, 200)
        size.setValue(100)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(QLabel("Font size"))
        wl.addWidget(size, 1)
        self.add_widget(w)

        self.add_widget(QCheckBox("High contrast mode"))
        self.add_widget(QCheckBox("Reduce animations"))


PAGES = {
    "appearance": ("Appearance", AppearancePage),
    "display": ("Display", DisplayPage),
    "audio": ("Audio", AudioPage),
    "network": ("Network", NetworkPage),
    "power": ("Power", PowerPage),
    "keyboard": ("Keyboard", KeyboardPage),
    "mouse": ("Mouse & Touchpad", MousePage),
    "users": ("Users", UsersPage),
    "language": ("Language", LanguagePage),
    "privacy": ("Privacy & Security", PrivacyPage),
    "accessibility": ("Accessibility", AccessibilityPage),
}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._setup_central_widget()

    def _setup_window(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(800, 500)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

    def _setup_central_widget(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._stack = QStackedWidget()

        for key, (label, page_cls) in PAGES.items():
            self._sidebar.add_section(key, label)
            self._stack.addWidget(page_cls())

        self._sidebar.section_changed.connect(self._on_section_changed)
        self._sidebar.select("appearance")

        layout.addWidget(self._sidebar)
        layout.addWidget(self._stack, 1)

    def _on_section_changed(self, section: str) -> None:
        keys = list(PAGES.keys())
        if section in keys:
            self._stack.setCurrentIndex(keys.index(section))
