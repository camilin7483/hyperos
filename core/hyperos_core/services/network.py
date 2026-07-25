import logging
import socket
import subprocess
from typing import Optional

from hyperos_core.domain.models import NetworkInfo

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 5
DEFAULT_HOSTS = (
    ("one.one.one.one", 443),
    ("8.8.8.8", 53),
    ("google.com", 443),
)


class NetworkService:
    def __init__(self, hosts: tuple[tuple[str, int], ...] = DEFAULT_HOSTS) -> None:
        self._hosts = hosts
        self._connected: Optional[bool] = None

    def check_connectivity(self) -> bool:
        for host, port in self._hosts:
            if self._try_connect(host, port):
                self._connected = True
                return True
        self._connected = False
        return False

    def _try_connect(self, host: str, port: int) -> bool:
        try:
            with socket.create_connection((host, port), timeout=DEFAULT_TIMEOUT):
                return True
        except (socket.gaierror, socket.timeout, OSError) as e:
            logger.debug("Connection to %s:%d failed: %s", host, port, e)
            return False

    def get_network_interfaces(self) -> list[NetworkInfo]:
        interfaces = []
        try:
            result = subprocess.run(
                ["ip", "-o", "addr", "show"],
                capture_output=True, text=True, timeout=5,
            )
            current_iface = ""
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 4:
                    iface = parts[1].rstrip(":")
                    addr = parts[3] if parts[2] == "inet" else ""
                    mac = ""
                    state = ""
                    interfaces.append(NetworkInfo(
                        interface=iface,
                        ip_address=addr.split("/")[0] if addr else "",
                        mac_address=mac,
                        connected="UP" in line.upper(),
                    ))
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not get network interfaces: %s", e)
        return interfaces

    @property
    def is_connected(self) -> bool:
        if self._connected is None:
            return self.check_connectivity()
        return self._connected
