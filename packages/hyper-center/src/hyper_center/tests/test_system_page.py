from PySide6.QtWidgets import QApplication
import pytest

from hyperos_core.domain.models import SystemInfo
from hyper_center.ui.dashboard_page import DashboardPage
from hyper_center.ui.system_page import SystemPage


@pytest.fixture(scope="session")
def app():
    return QApplication([])


def test_dashboard_page_creation(app):
    page = DashboardPage()
    assert page is not None


def test_system_page_creation(app):
    page = SystemPage()
    assert page is not None


def test_dashboard_update(app):
    page = DashboardPage()
    info = SystemInfo(cpu="Test CPU", ram_total="8 GB", ram_percent=50.0)
    page.update_info(info)


def test_system_page_update(app):
    page = SystemPage()
    info = SystemInfo(
        cpu="Test CPU", cpu_cores=8, cpu_usage=25.0,
        ram_total="16 GB", ram_used="8 GB", ram_percent=50.0,
        gpu="Test GPU", kernel="6.0.0",
        os_name="HyperOS", os_version="0.1.0",
        hostname="test", uptime="1h", processes=128,
        desktop="Hyprland",
    )
    page.update_info(info)
