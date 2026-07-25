"""Service for collecting system information."""

import logging
import os
import platform
import subprocess
from pathlib import Path

from hyper_welcome.domain.models import SystemInfo

logger = logging.getLogger(__name__)

HOSTNAME_PATH = Path("/etc/hostname")
OS_RELEASE_PATH = Path("/etc/os-release")
CPU_INFO_PATH = "/proc/cpuinfo"
MEM_INFO_PATH = "/proc/meminfo"


class SystemService:
    """Collects and provides system information."""

    def __init__(self) -> None:
        self._info: SystemInfo = SystemInfo()

    def collect(self) -> SystemInfo:
        """Gather all system information and return it."""
        try:
            self._info.cpu = self._get_cpu_name()
            self._info.cpu_cores = self._get_cpu_cores()
            self._info.ram_total, self._info.ram_percent = self._get_ram_info()
            self._info.gpu = self._get_gpu_name()
            self._info.storage_total, self._info.storage_percent = self._get_storage_info()
            self._info.kernel = self._get_kernel_version()
            self._info.desktop = self._detect_desktop()
            self._info.os_name, self._info.os_version = self._get_os_info()
            self._info.hostname = self._get_hostname()
            self._info.uptime = self._get_uptime()
        except Exception as e:
            logger.exception("Failed to collect system info: %s", e)
        return self._info

    def _get_cpu_name(self) -> str:
        try:
            with open(CPU_INFO_PATH) as f:
                for line in f:
                    if line.startswith("model name"):
                        return line.split(":")[1].strip()
        except (FileNotFoundError, PermissionError) as e:
            logger.debug("Could not read CPU info: %s", e)
        return platform.processor() or "Unknown"

    def _get_cpu_cores(self) -> int:
        try:
            return os.cpu_count() or 0
        except Exception as e:
            logger.debug("Could not count CPUs: %s", e)
            return 0

    def _get_ram_info(self) -> tuple[str, float]:
        try:
            with open(MEM_INFO_PATH) as f:
                lines = f.readlines()

            total_kb = 0
            available_kb = 0
            for line in lines:
                if line.startswith("MemTotal:"):
                    total_kb = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    available_kb = int(line.split()[1])

            if total_kb > 0:
                total_gb = total_kb / (1024 * 1024)
                used_percent = ((total_kb - available_kb) / total_kb) * 100
                return f"{total_gb:.1f} GB", round(used_percent, 1)
        except (FileNotFoundError, IndexError, ValueError) as e:
            logger.debug("Could not read RAM info: %s", e)
        return "Unknown", 0.0

    def _get_gpu_name(self) -> str:
        try:
            result = subprocess.run(
                ["lspci", "-nn"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            for line in result.stdout.splitlines():
                lower = line.lower()
                if any(x in lower for x in ("vga", "3d", "display")):
                    parts = line.split(":", 2)
                    if len(parts) >= 3:
                        gpu_desc = parts[-1].strip()
                        return gpu_desc.split("(rev")[0].strip()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not detect GPU: %s", e)
        return "Unknown"

    def _get_storage_info(self) -> tuple[str, float]:
        try:
            stat = os.statvfs("/")
            total_bytes = stat.f_frsize * stat.f_blocks
            free_bytes = stat.f_frsize * stat.f_bfree
            used_percent = ((total_bytes - free_bytes) / total_bytes) * 100
            total_gb = total_bytes / (1024 ** 3)
            return f"{total_gb:.1f} GB", round(used_percent, 1)
        except Exception as e:
            logger.debug("Could not read storage info: %s", e)
        return "Unknown", 0.0

    def _get_kernel_version(self) -> str:
        return platform.release() or "Unknown"

    def _detect_desktop(self) -> str:
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
        if desktop:
            return desktop
        return "Hyprland"

    def _get_os_info(self) -> tuple[str, str]:
        try:
            if OS_RELEASE_PATH.exists():
                with open(OS_RELEASE_PATH) as f:
                    content = f.read()
                name = ""
                version = ""
                for line in content.splitlines():
                    if line.startswith("NAME="):
                        name = line.split("=", 1)[1].strip().strip('"')
                    elif line.startswith("VERSION_ID="):
                        version = line.split("=", 1)[1].strip().strip('"')
                return name or "HyperOS", version or "rolling"
        except (FileNotFoundError, PermissionError) as e:
            logger.debug("Could not read os-release: %s", e)
        return "HyperOS", "0.1.0"

    def _get_hostname(self) -> str:
        try:
            if HOSTNAME_PATH.exists():
                return HOSTNAME_PATH.read_text().strip()
        except (FileNotFoundError, PermissionError) as e:
            logger.debug("Could not read hostname: %s", e)
        return platform.node() or "hyperos"

    def _get_uptime(self) -> str:
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.readline().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            parts = []
            if days > 0:
                parts.append(f"{days}d")
            if hours > 0:
                parts.append(f"{hours}h")
            parts.append(f"{minutes}m")
            return " ".join(parts)
        except (FileNotFoundError, ValueError, IndexError) as e:
            logger.debug("Could not read uptime: %s", e)
        return "Unknown"
