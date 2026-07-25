"""Domain models for Hyper Welcome."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConnectivityStatus:
    """Represents the internet connectivity state of the system."""

    connected: bool = False
    method: str = "unknown"


@dataclass
class SystemInfo:
    """Aggregated system information for the welcome screen."""

    cpu: str = "Unknown"
    cpu_cores: int = 0
    ram_total: str = "Unknown"
    ram_percent: float = 0.0
    gpu: str = "Unknown"
    storage_total: str = "Unknown"
    storage_percent: float = 0.0
    kernel: str = "Unknown"
    desktop: str = "Hyprland"
    os_name: str = "HyperOS"
    os_version: str = "0.1.0"
    hostname: str = "hyperos"
    uptime: str = "Unknown"

    def to_dict(self) -> dict:
        return {
            "cpu": self.cpu,
            "cpu_cores": self.cpu_cores,
            "ram_total": self.ram_total,
            "ram_percent": self.ram_percent,
            "gpu": self.gpu,
            "storage_total": self.storage_total,
            "storage_percent": self.storage_percent,
            "kernel": self.kernel,
            "desktop": self.desktop,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "hostname": self.hostname,
            "uptime": self.uptime,
        }
