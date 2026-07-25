import logging, sys, json
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from hyper_assistant.ui.main_window import MainWindow
from hyperos_core.ui.styles import load_stylesheet


class PluginEngine:
    def __init__(self) -> None:
        self._plugins: dict[str, dict] = {}
        self._load_plugins()

    def _load_plugins(self) -> None:
        plugin_dir = Path.home() / ".config" / "hyperos" / "assistant-plugins"
        if plugin_dir.exists():
            for f in plugin_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text())
                    self._plugins[data.get("name", f.stem)] = data
                except Exception as e:
                    logging.getLogger(__name__).debug("Failed to load plugin %s: %s", f, e)

    def process(self, query: str) -> str:
        query_lower = query.lower()
        for name, plugin in self._plugins.items():
            keywords = plugin.get("keywords", [])
            if any(k in query_lower for k in keywords):
                return plugin.get("response", f"Plugin '{name}' matched but no response defined.")
        return self._fallback(query)

    def _fallback(self, query: str) -> str:
        query_lower = query.lower()
        if "time" in query_lower or "date" in query_lower:
            import datetime
            return f"It's {datetime.datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}."
        if "help" in query_lower or "what can you" in query_lower:
            return ("I can help with: system information, time/date, "
                    "application launching, and plugins. Ask me anything!")
        if "hello" in query_lower or "hi" in query_lower:
            return "Hello! How can I help you with HyperOS today?"
        return "I'm not sure how to help with that. Try asking about system status, time, or check your installed plugins."


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    app.setApplicationName("Hyper Assistant")
    app.setStyleSheet(load_stylesheet())
    engine = PluginEngine()
    window = MainWindow(engine)
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
