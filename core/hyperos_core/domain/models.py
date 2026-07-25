from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SystemInfo:
    cpu: str = "Unknown"
    cpu_cores: int = 0
    cpu_usage: float = 0.0
    ram_total: str = "Unknown"
    ram_used: str = "Unknown"
    ram_percent: float = 0.0
    gpu: str = "Unknown"
    storage_total: str = "Unknown"
    storage_used: str = "Unknown"
    storage_percent: float = 0.0
    kernel: str = "Unknown"
    desktop: str = "Hyprland"
    os_name: str = "HyperOS"
    os_version: str = "0.1.0"
    hostname: str = "hyperos"
    uptime: str = "Unknown"
    swap_total: str = "Unknown"
    swap_percent: float = 0.0
    processes: int = 0


@dataclass
class NetworkInfo:
    interface: str = ""
    ip_address: str = ""
    mac_address: str = ""
    gateway: str = ""
    dns: str = ""
    speed: str = ""
    connected: bool = False
    type: str = ""
    ssid: str = ""


@dataclass
class StorageInfo:
    device: str = ""
    mount: str = ""
    fstype: str = ""
    total: str = ""
    used: str = ""
    available: str = ""
    percent: float = 0.0


@dataclass
class ServiceInfo:
    name: str = ""
    description: str = ""
    state: str = ""
    enabled: bool = False
    running: bool = False


@dataclass
class PackageInfo:
    name: str = ""
    version: str = ""
    description: str = ""
    size: str = ""
    repository: str = ""
    installed: bool = False


@dataclass
class UserInfo:
    username: str = ""
    uid: int = 0
    gid: int = 0
    shell: str = ""
    home: str = ""
    groups: list[str] = field(default_factory=list)


@dataclass
class PowerProfile:
    name: str = ""
    label: str = ""
    description: str = ""
    cpu_governor: str = "schedutil"
    swappiness: int = 60
    screen_timeout: int = 300
    performance_mode: str = "balanced"
    is_active: bool = False
