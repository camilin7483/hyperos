import logging
import subprocess
from typing import Optional

from hyperos_core.domain.models import ServiceInfo

logger = logging.getLogger(__name__)


class ServiceManager:
    def __init__(self, user_mode: bool = False) -> None:
        self._user_mode = user_mode

    def _cmd(self, args: list[str]) -> list[str]:
        base = ["systemctl"]
        if self._user_mode:
            base.append("--user")
        return base + args

    def list_services(self) -> list[ServiceInfo]:
        services = []
        try:
            result = subprocess.run(
                self._cmd(["-a", "--no-pager", "--type=service", "--no-legend"]),
                capture_output=True, text=True, timeout=15,
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    if ".service" in name:
                        services.append(ServiceInfo(
                            name=name.replace(".service", ""),
                            state=parts[2],
                            running=parts[2] == "active",
                            enabled=len(parts) > 3 and parts[3] == "enabled",
                        ))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to list services: %s", e)
        return services

    def get_service(self, name: str) -> Optional[ServiceInfo]:
        try:
            result = subprocess.run(
                self._cmd(["show", "--no-pager", f"{name}.service"]),
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode != 0:
                return None
            info = ServiceInfo(name=name)
            for line in result.stdout.splitlines():
                if "=" in line:
                    key, val = line.split("=", 1)
                    if key == "Description":
                        info.description = val
                    elif key == "ActiveState":
                        info.state = val
                        info.running = val == "active"
                    elif key == "UnitFileState":
                        info.enabled = val == "enabled"
            return info
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to get service %s: %s", name, e)
        return None

    def start(self, name: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["start", f"{name}.service"]),
                capture_output=True, text=True, timeout=30,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to start %s: %s", name, e)
        return False

    def stop(self, name: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["stop", f"{name}.service"]),
                capture_output=True, text=True, timeout=30,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to stop %s: %s", name, e)
        return False

    def restart(self, name: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["restart", f"{name}.service"]),
                capture_output=True, text=True, timeout=30,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to restart %s: %s", name, e)
        return False

    def enable(self, name: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["enable", f"{name}.service"]),
                capture_output=True, text=True, timeout=30,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to enable %s: %s", name, e)
        return False

    def disable(self, name: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["disable", f"{name}.service"]),
                capture_output=True, text=True, timeout=30,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to disable %s: %s", name, e)
        return False

    def get_failed_services(self) -> list[ServiceInfo]:
        services = []
        try:
            result = subprocess.run(
                self._cmd(["--failed", "--no-legend"]),
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0].replace(".service", "")
                    services.append(ServiceInfo(name=name, state="failed", running=False))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to get failed services: %s", e)
        return services

    def get_journal_logs(self, name: str, lines: int = 50) -> list[str]:
        try:
            result = subprocess.run(
                ["journalctl", "-u", f"{name}.service", "--no-pager", f"-n{lines}"],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.splitlines()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to get logs for %s: %s", name, e)
        return []
