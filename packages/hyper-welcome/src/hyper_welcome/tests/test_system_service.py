"""Tests for SystemService."""

import platform
from unittest.mock import patch, mock_open

import pytest

from hyper_welcome.services.system_service import SystemService


class TestSystemService:
    """Test suite for SystemService."""

    def setup_method(self) -> None:
        self.service = SystemService()

    def test_collect_returns_system_info(self) -> None:
        info = self.service.collect()
        assert info is not None
        assert info.cpu is not None
        assert isinstance(info.cpu_cores, int)
        assert isinstance(info.ram_percent, float)
        assert info.kernel == platform.release()

    def test_get_cpu_name_from_proc(self) -> None:
        cpu_data = "model name : Intel(R) Core(TM) i7-10700K\n"
        with patch("builtins.open", mock_open(read_data=cpu_data)):
            result = self.service._get_cpu_name()
            assert "Intel" in result
            assert "i7" in result

    def test_get_cpu_name_fallback_on_error(self) -> None:
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("platform.processor", return_value="armv8"):
                result = self.service._get_cpu_name()
                assert result == "armv8"

    def test_get_cpu_cores(self) -> None:
        cores = self.service._get_cpu_cores()
        assert cores >= 1

    def test_get_ram_info(self) -> None:
        mem_data = "MemTotal:       16384000 kB\nMemAvailable:   8192000 kB\n"
        with patch("builtins.open", mock_open(read_data=mem_data)):
            total, percent = self.service._get_ram_info()
            assert "GB" in total
            assert 0 <= percent <= 100

    def test_get_ram_info_returns_unknown_on_error(self) -> None:
        with patch("builtins.open", side_effect=FileNotFoundError):
            total, percent = self.service._get_ram_info()
            assert total == "Unknown"
            assert percent == 0.0

    def test_get_kernel_version(self) -> None:
        version = self.service._get_kernel_version()
        assert len(version) > 0
        assert "." in version

    def test_detect_desktop_from_env(self) -> None:
        with patch.dict("os.environ", {"XDG_CURRENT_DESKTOP": "KDE"}, clear=True):
            result = self.service._detect_desktop()
            assert result == "KDE"

    def test_detect_desktop_default(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = self.service._detect_desktop()
            assert result == "Hyprland"

    def test_get_os_info_from_os_release(self) -> None:
        os_data = 'NAME="HyperOS"\nVERSION_ID="0.1.0"\n'
        with patch("builtins.open", mock_open(read_data=os_data)):
            name, version = self.service._get_os_info()
            assert name == "HyperOS"
            assert version == "0.1.0"

    def test_get_uptime(self) -> None:
        with patch("builtins.open", mock_open(read_data="123456.78 98765.43\n")):
            uptime = self.service._get_uptime()
            assert "d" in uptime or "h" in uptime or "m" in uptime

    def test_get_hostname(self) -> None:
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.read_text", return_value="myhost\n"):
                hostname = self.service._get_hostname()
                assert hostname == "myhost"

    def test_get_storage_info(self) -> None:
        total, percent = self.service._get_storage_info()
        assert "GB" in total
        assert 0 <= percent <= 100
