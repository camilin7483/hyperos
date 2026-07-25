STYLESHEET = """
/* HyperOS Dark Theme */

QMainWindow, QWidget {
    background-color: #1A1A1A;
    color: #E0E0E0;
    font-family: "Noto Sans", "DejaVu Sans", sans-serif;
    font-size: 13px;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #141414;
    border-right: 1px solid #2D2D2D;
}

QLabel#sidebarLogo {
    color: #00AEEF;
    font-size: 18px;
    font-weight: bold;
    padding: 8px 12px;
}

QPushButton#sidebarButton {
    background-color: transparent;
    color: #AAAAAA;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    text-align: left;
    font-size: 13px;
}

QPushButton#sidebarButton:hover {
    background-color: #2D2D2D;
    color: #FFFFFF;
}

QPushButton#sidebarButton:checked {
    background-color: #00AEEF;
    color: #000000;
    font-weight: bold;
}

QFrame#sidebarSeparator {
    color: #2D2D2D;
    max-height: 1px;
    margin: 8px 12px;
}

/* Cards */
QFrame#hyperCard {
    background-color: #2D2D2D;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
}

QFrame#hyperCard:hover {
    border: 1px solid #00AEEF;
}

QLabel#cardTitle {
    color: #FFFFFF;
    font-size: 14px;
    font-weight: bold;
}

QLabel#cardRowLabel {
    color: #888888;
    font-size: 12px;
}

QLabel#cardRowValue {
    color: #E0E0E0;
    font-size: 12px;
}

/* Info Card (metric display) */
QFrame#infoCard {
    background-color: #2D2D2D;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
}

QFrame#infoCard:hover {
    border: 1px solid #00AEEF;
}

QLabel#infoCardLabel {
    color: #888888;
    font-size: 9px;
}

QLabel#infoCardValue {
    color: #FFFFFF;
    font-size: 12px;
    font-weight: bold;
}

QLabel#infoCardIcon {
    color: #00AEEF;
    font-size: 18px;
    font-weight: bold;
}

/* Buttons */
QPushButton {
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
}

QPushButton#primaryButton {
    background-color: #00AEEF;
    color: #000000;
    border: none;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #33C4FF;
}

QPushButton#primaryButton:pressed {
    background-color: #0099D6;
}

QPushButton#secondaryButton {
    background-color: #2D2D2D;
    color: #E0E0E0;
    border: 1px solid #3A3A3A;
}

QPushButton#secondaryButton:hover {
    background-color: #3A3A3A;
    border: 1px solid #00AEEF;
}

QPushButton#secondaryButton:pressed {
    background-color: #4A4A4A;
}

QPushButton#dangerButton {
    background-color: #FF5252;
    color: #FFFFFF;
    border: none;
    font-weight: bold;
}

QPushButton#dangerButton:hover {
    background-color: #FF7070;
}

/* Header */
QLabel#pageTitle {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: bold;
}

QLabel#pageSubtitle {
    color: #AAAAAA;
    font-size: 13px;
}

/* Tables (QTreeWidget / QTableWidget) */
QTreeWidget, QTableWidget {
    background-color: #2D2D2D;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
    gridline-color: #3A3A3A;
    selection-background-color: #00AEEF;
    selection-color: #000000;
}

QHeaderView::section {
    background-color: #141414;
    color: #888888;
    border: none;
    padding: 8px;
    font-size: 12px;
    font-weight: bold;
}

/* Scroll areas */
QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollBar:vertical {
    background-color: #1A1A1A;
    width: 8px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3A3A3A;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Line edits */
QLineEdit, QComboBox, QSpinBox {
    background-color: #2D2D2D;
    border: 1px solid #3A3A3A;
    border-radius: 6px;
    padding: 6px 12px;
    color: #E0E0E0;
    font-size: 13px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #00AEEF;
}

/* Progress bars */
QProgressBar {
    background-color: #2D2D2D;
    border: 1px solid #3A3A3A;
    border-radius: 4px;
    text-align: center;
    font-size: 11px;
    color: #E0E0E0;
}

QProgressBar::chunk {
    background-color: #00AEEF;
    border-radius: 3px;
}

/* Tabs */
QTabWidget::pane {
    background-color: #1A1A1A;
    border: none;
    border-top: 1px solid #2D2D2D;
}

QTabBar::tab {
    background-color: #141414;
    color: #888888;
    border: none;
    padding: 8px 16px;
    font-size: 13px;
}

QTabBar::tab:selected {
    color: #00AEEF;
    border-bottom: 2px solid #00AEEF;
    background-color: #1A1A1A;
}

QTabBar::tab:hover {
    color: #E0E0E0;
}

/* Checkboxes */
QCheckBox {
    spacing: 8px;
    color: #E0E0E0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #3A3A3A;
    border-radius: 4px;
    background-color: #2D2D2D;
}

QCheckBox::indicator:checked {
    background-color: #00AEEF;
    border-color: #00AEEF;
}

/* Sliders */
QSlider::groove:horizontal {
    height: 6px;
    background-color: #2D2D2D;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    background-color: #00AEEF;
    margin: -6px 0;
}

QSlider::sub-page:horizontal {
    background-color: #00AEEF;
    border-radius: 3px;
}
"""


def load_stylesheet() -> str:
    return STYLESHEET
