import logging, subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QProgressBar, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget)

logger = logging.getLogger(__name__)


class InstallerPage(QWidget):
    def __init__(self, title: str, description: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(16)
        t = QLabel(title)
        t.setObjectName("pageTitle")
        layout.addWidget(t)
        d = QLabel(description)
        d.setObjectName("pageSubtitle")
        layout.addWidget(d)
        self.content = QVBoxLayout()
        self.content.setSpacing(12)
        layout.addLayout(self.content)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("HyperOS Installer")
        self.resize(800, 600)
        self.setMinimumSize(700, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Progress steps
        steps = QWidget()
        steps.setFixedHeight(60)
        steps.setStyleSheet("background-color: #141414;")
        steps_layout = QHBoxLayout(steps)
        steps_layout.setContentsMargins(32, 0, 32, 0)
        self._step_label = QLabel("Step 1/6: Welcome")
        self._step_label.setStyleSheet("color: #00AEEF; font-size: 14px; font-weight: bold;")
        steps_layout.addWidget(self._step_label)
        layout.addWidget(steps)

        self._stack = QStackedWidget()
        self._pages: list[QWidget] = []
        self._current_step = 0

        # Page 1: Welcome
        p1 = InstallerPage("Welcome to HyperOS", "This installer will guide you through setting up HyperOS on your computer.")
        welcome_text = QLabel(
            "HyperOS is an Arch Linux-based distribution focused on performance.\n\n"
            "This installer supports UEFI/GPT with Btrfs or ext4.\n\n"
            "Make sure you have:\n"
            "• At least 20 GB of disk space\n"
            "• An internet connection\n"
            "• A UEFI-capable system"
        )
        welcome_text.setObjectName("pageSubtitle")
        welcome_text.setWordWrap(True)
        p1.content.addWidget(welcome_text)
        self._add_page(p1)

        # Page 2: Disk
        p2 = InstallerPage("Disk Setup", "Select the disk where HyperOS will be installed.")
        disk_layout = QHBoxLayout()
        self._disk_combo = QComboBox()
        self._disk_combo.setMinimumWidth(300)
        disk_layout.addWidget(QLabel("Target Disk:"))
        disk_layout.addWidget(self._disk_combo, 1)
        p2.content.addLayout(disk_layout)
        self._populate_disks()

        fs_layout = QHBoxLayout()
        self._fs_combo = QComboBox()
        self._fs_combo.addItems(["Btrfs (recommended)", "ext4"])
        fs_layout.addWidget(QLabel("Filesystem:"))
        fs_layout.addWidget(self._fs_combo, 1)
        p2.content.addLayout(fs_layout)

        encrypt = QWidget()
        encrypt_layout = QHBoxLayout(encrypt)
        encrypt_layout.setContentsMargins(0, 0, 0, 0)
        from PySide6.QtWidgets import QCheckBox
        self._encrypt_check = QCheckBox("Encrypt system (LUKS)")
        encrypt_layout.addWidget(self._encrypt_check)
        p2.content.addWidget(encrypt)
        self._add_page(p2)

        # Page 3: User
        p3 = InstallerPage("User Setup", "Create your user account.")
        for label, attr in [("Username:", "username"), ("Full Name:", "fullname"), ("Password:", "password")]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            inp = QLineEdit()
            if "password" in attr:
                inp.setEchoMode(QLineEdit.EchoMode.Password)
            row.addWidget(inp, 1)
            p3.content.addLayout(row)
            setattr(self, f"_{attr}_input", inp)

        host_row = QHBoxLayout()
        host_row.addWidget(QLabel("Hostname:"))
        self._hostname_input = QLineEdit("hyperos")
        host_row.addWidget(self._hostname_input, 1)
        p3.content.addLayout(host_row)
        self._add_page(p3)

        # Page 4: Locale
        p4 = InstallerPage("Locale Settings", "Configure language, timezone, and keyboard.")
        for label, attr, items in [("Language:", "lang", ["en_US.UTF-8", "es_CO.UTF-8", "de_DE.UTF-8", "fr_FR.UTF-8"]),
                                    ("Timezone:", "tz", ["America/New_York", "America/Bogota", "Europe/Madrid", "Europe/Berlin", "Asia/Tokyo"]),
                                    ("Keyboard:", "kb", ["us", "es", "de", "fr", "jp"])]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            combo = QComboBox()
            combo.addItems(items)
            row.addWidget(combo, 1)
            p4.content.addLayout(row)
            setattr(self, f"_{attr}_combo", combo)
        self._add_page(p4)

        # Page 5: Install
        p5 = InstallerPage("Install", "Ready to install HyperOS.")
        self._install_info = QLabel("Click 'Install' to begin the installation.")
        self._install_info.setObjectName("pageSubtitle")
        self._install_info.setWordWrap(True)
        p5.content.addWidget(self._install_info)

        self._progress = QProgressBar()
        self._progress.setMinimum(0)
        self._progress.setMaximum(100)
        p5.content.addWidget(self._progress)

        self._install_log = QLabel("")
        self._install_log.setObjectName("cardRowValue")
        self._install_log.setWordWrap(True)
        p5.content.addWidget(self._install_log)
        self._add_page(p5)

        # Page 6: Complete
        p6 = InstallerPage("Installation Complete", "HyperOS has been installed successfully.")
        complete_text = QLabel(
            "You can now reboot into your new HyperOS system.\n\n"
            "• Remove the installation media\n"
            "• The system will boot into HyperOS\n"
            "• Log in with the credentials you created\n\n"
            "Thank you for choosing HyperOS!"
        )
        complete_text.setObjectName("pageSubtitle")
        complete_text.setWordWrap(True)
        p6.content.addWidget(complete_text)
        self._add_page(p6)

        # Navigation
        nav = QWidget()
        nav.setFixedHeight(60)
        nav.setStyleSheet("background-color: #141414;")
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(32, 0, 32, 0)

        self._back_btn = QPushButton("Back")
        self._back_btn.setObjectName("secondaryButton")
        self._back_btn.clicked.connect(self._go_back)
        nav_layout.addWidget(self._back_btn)

        nav_layout.addStretch()

        self._next_btn = QPushButton("Next")
        self._next_btn.setObjectName("primaryButton")
        self._next_btn.clicked.connect(self._go_next)
        nav_layout.addWidget(self._next_btn)

        layout.addWidget(self._stack, 1)
        layout.addWidget(nav)

        self._update_nav()

    def _add_page(self, page: QWidget) -> None:
        self._pages.append(page)
        self._stack.addWidget(page)

    def _populate_disks(self) -> None:
        try:
            result = subprocess.run(
                ["lsblk", "-d", "-o", "NAME,SIZE,MODEL", "--noheadings"],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if parts:
                    name = parts[0]
                    size = parts[1] if len(parts) > 1 else ""
                    label = f"/dev/{name} ({size})"
                    self._disk_combo.addItem(label, f"/dev/{name}")
        except Exception as e:
            logger.error("Failed to list disks: %s", e)
            self._disk_combo.addItem("No disks detected")

    def _update_nav(self) -> None:
        total = len(self._pages)
        self._step_label.setText(f"Step {self._current_step + 1}/{total}: {self._pages[self._current_step].findChildren(QLabel)[0].text()}")
        self._back_btn.setEnabled(self._current_step > 0)
        if self._current_step == total - 1:
            self._next_btn.setText("Finish")
        elif self._current_step == total - 2:
            self._next_btn.setText("Install")
        else:
            self._next_btn.setText("Next")

    def _go_back(self) -> None:
        if self._current_step > 0:
            self._current_step -= 1
            self._stack.setCurrentIndex(self._current_step)
            self._update_nav()

    def _go_next(self) -> None:
        total = len(self._pages)
        if self._current_step == total - 1:
            QApplication.quit()
            return
        if self._current_step == total - 2:
            self._start_install()
            return
        self._current_step += 1
        self._stack.setCurrentIndex(self._current_step)
        self._update_nav()

    def _start_install(self) -> None:
        self._next_btn.setEnabled(False)
        self._back_btn.setEnabled(False)
        self._install_info.setText("Installing HyperOS... This may take several minutes.")
        disk = self._disk_combo.currentData()
        fs = "btrfs" if "Btrfs" in self._fs_combo.currentText() else "ext4"
        encrypt = self._encrypt_check.isChecked()
        username = self._username_input.text()
        hostname = self._hostname_input.text()

        self._progress.setValue(10)
        self._install_log.setText(f"Target: {disk}\nFS: {fs}\nEncryption: {encrypt}\nUser: {username}\nHostname: {hostname}")
        self._progress.setValue(100)
        self._install_log.setText("Installation simulation complete.\n\nIn a real environment, this would:\n1. Partition the disk\n2. Format filesystems\n3. Install base system\n4. Configure bootloader\n5. Create user\n6. Install HyperOS packages")

        self._current_step += 1
        self._stack.setCurrentIndex(self._current_step)
        self._update_nav()
