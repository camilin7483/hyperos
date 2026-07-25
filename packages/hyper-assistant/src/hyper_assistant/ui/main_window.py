import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget)


class AssistantBubble(QWidget):
    def __init__(self, text: str, is_user: bool = False) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setObjectName("pageSubtitle")
        if is_user:
            label.setStyleSheet("color: #00AEEF; font-weight: bold; font-size: 13px;")
        else:
            label.setStyleSheet("color: #E0E0E0; font-size: 13px;")
        if is_user:
            layout.addStretch()
        layout.addWidget(label)
        if not is_user:
            layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self, engine) -> None:
        super().__init__()
        self._engine = engine
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("Hyper Assistant")
        self.resize(600, 500)
        layout = QVBoxLayout()

        title = QLabel("Hyper Assistant")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Ask me anything about your system")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        self._chat = QListWidget()
        self._chat.setObjectName("hyperCard")
        layout.addWidget(self._chat, 1)

        self._add_bubble("Hello! I'm your HyperOS assistant. How can I help?", False)

        input_layout = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Type your question here...")
        self._input.returnPressed.connect(self._send)
        input_layout.addWidget(self._input)

        send = QPushButton("Send")
        send.setObjectName("primaryButton")
        send.clicked.connect(self._send)
        input_layout.addWidget(send)

        layout.addLayout(input_layout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _add_bubble(self, text: str, is_user: bool) -> None:
        item = QListWidgetItem()
        bubble = AssistantBubble(text, is_user)
        item.setSizeHint(bubble.sizeHint())
        self._chat.addItem(item)
        self._chat.setItemWidget(item, bubble)
        self._chat.scrollToBottom()

    def _send(self) -> None:
        text = self._input.text().strip()
        if not text:
            return
        self._add_bubble(text, True)
        self._input.clear()
        response = self._engine.process(text)
        self._add_bubble(response, False)
