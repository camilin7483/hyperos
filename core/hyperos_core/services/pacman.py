import json
import logging
import subprocess
from typing import Optional

from hyperos_core.domain.models import PackageInfo

logger = logging.getLogger(__name__)


class PacmanService:
    def __init__(self, sudo: bool = False) -> None:
        self._sudo = sudo

    def _cmd(self, args: list[str]) -> list[str]:
        cmd = ["sudo"] if self._sudo else []
        return cmd + ["pacman"] + args

    def get_installed_packages(self) -> list[PackageInfo]:
        packages = []
        try:
            result = subprocess.run(
                self._cmd(["-Q"]),
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append(PackageInfo(
                        name=parts[0],
                        version=parts[1],
                        installed=True,
                    ))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to list packages: %s", e)
        return packages

    def get_package_count(self) -> int:
        try:
            result = subprocess.run(
                self._cmd(["-Q"]),
                capture_output=True, text=True, timeout=15,
            )
            return len(result.stdout.splitlines())
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to count packages: %s", e)
        return 0

    def get_available_updates(self) -> list[PackageInfo]:
        updates = []
        try:
            result = subprocess.run(
                self._cmd(["-Qu"]),
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    updates.append(PackageInfo(
                        name=parts[0],
                        version=parts[1],
                        installed=True,
                    ))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not check updates: %s", e)
        return updates

    def get_update_count(self) -> int:
        try:
            result = subprocess.run(
                self._cmd(["-Qu"]),
                capture_output=True, text=True, timeout=30,
            )
            count = len([l for l in result.stdout.splitlines() if l.strip()])
            return count
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not check update count: %s", e)
        return 0

    def search_packages(self, query: str) -> list[PackageInfo]:
        results = []
        try:
            result = subprocess.run(
                self._cmd(["-Ss", query]),
                capture_output=True, text=True, timeout=30,
            )
            for line in result.stdout.splitlines():
                if " " in line and "/" in line:
                    parts = line.split()
                    repo_pkg = parts[0].split("/")
                    if len(repo_pkg) >= 2:
                        results.append(PackageInfo(
                            name=repo_pkg[1],
                            version=parts[1] if len(parts) > 1 else "",
                            repository=repo_pkg[0],
                        ))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to search packages: %s", e)
        return results

    def get_package_info(self, name: str) -> Optional[PackageInfo]:
        try:
            result = subprocess.run(
                self._cmd(["-Qi", name]),
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                info = PackageInfo(name=name, installed=True)
                for line in result.stdout.splitlines():
                    if ":" in line:
                        key, val = line.split(":", 1)
                        key = key.strip()
                        val = val.strip()
                        if key == "Version":
                            info.version = val
                        elif key == "Description":
                            info.description = val
                        elif key == "Installed Size":
                            info.size = val
                        elif key == "Repository":
                            info.repository = val
                return info
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not get package info: %s", e)
        return None

    def install(self, package: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["-S", "--noconfirm", package]),
                capture_output=True, text=True, timeout=120,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to install %s: %s", package, e)
        return False

    def remove(self, package: str) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["-R", "--noconfirm", package]),
                capture_output=True, text=True, timeout=60,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to remove %s: %s", package, e)
        return False

    def update_system(self) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["-Syu", "--noconfirm"]),
                capture_output=True, text=True, timeout=300,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to update system: %s", e)
        return False

    def sync_databases(self) -> bool:
        try:
            result = subprocess.run(
                self._cmd(["-Sy"]),
                capture_output=True, text=True, timeout=60,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to sync databases: %s", e)
        return False

    def get_mirror_status(self) -> list[dict]:
        try:
            result = subprocess.run(
                ["curl", "-s", "https://archlinux.org/mirrors/status/json/"],
                capture_output=True, text=True, timeout=15,
            )
            data = json.loads(result.stdout)
            return data.get("urls", [])[:10]
        except Exception as e:
            logger.debug("Could not fetch mirror status: %s", e)
        return []

    def get_package_history(self, package: str) -> list[str]:
        try:
            log_path = "/var/log/pacman.log"
            result = subprocess.run(
                ["grep", f" {package}", log_path],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.splitlines()[-20:]
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not get package history: %s", e)
        return []
