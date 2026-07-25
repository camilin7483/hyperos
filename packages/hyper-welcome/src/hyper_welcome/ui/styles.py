"""HyperOS dark theme stylesheet."""

STYLESHEET = """
/* HyperOS Dark Theme */

QMainWindow {
    background-color: #1A1A1A;
}

QWidget {
    background-color: #1A1A1A;
    color: #E0E0E0;
    font-family: "Noto Sans", "DejaVu Sans", sans-serif;
}

QLabel#titleLabel {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: bold;
}

QLabel#subtitleLabel {
    color: #AAAAAA;
    font-size: 13px;
}

QLabel#versionLabel {
    color: #00AEEF;
    font-size: 12px;
    font-weight: bold;
}

QLabel#sectionTitle {
    color: #FFFFFF;
    font-size: 14px;
    font-weight: bold;
    padding-bottom: 4px;
}

QLabel#statusLabel {
    font-size: 12px;
}

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
    text-transform: uppercase;
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

QPushButton#actionButton {
    background-color: #2D2D2D;
    color: #E0E0E0;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#actionButton:hover {
    background-color: #3A3A3A;
    border: 1px solid #00AEEF;
}

QPushButton#actionButton:pressed {
    background-color: #4A4A4A;
}

QPushButton#actionButtonPrimary {
    background-color: #00AEEF;
    color: #000000;
    border: none;
    border-radius: 8px;
    padding: 8px 24px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#actionButtonPrimary:hover {
    background-color: #33C4FF;
}

QPushButton#actionButtonPrimary:pressed {
    background-color: #0099D6;
}

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

QScrollBar:horizontal {
    background-color: #1A1A1A;
    height: 0px;
}
"""


def load_stylesheet() -> str:
    """Return the HyperOS dark theme stylesheet."""
    return STYLESHEET
