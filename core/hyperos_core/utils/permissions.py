import os
import subprocess
from pathlib import Path


def check_sudo() -> bool:
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def require_sudo() -> bool:
    if os.geteuid() == 0:
        return True
    return check_sudo()


def ensure_config_dir(path: Path, mode: int = 0o700) -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(mode)


def write_secure(path: Path, data: str, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
    path.chmod(mode)
