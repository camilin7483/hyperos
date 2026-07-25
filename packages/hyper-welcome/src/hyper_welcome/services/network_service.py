"""Service for checking internet connectivity."""

import logging
import socket
from typing import Optional

from hyper_welcome.domain.models import ConnectivityStatus

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 5
DEFAULT_HOSTS = (
    ("one.one.one.one", 443),
    ("8.8.8.8", 53),
    ("google.com", 443),
)


class NetworkService:
    """Checks internet connectivity by attempting connections to known hosts."""

    def __init__(self, hosts: tuple[tuple[str, int], ...] = DEFAULT_HOSTS) -> None:
        self._hosts = hosts
        self._connected: Optional[bool] = None

    def check_connectivity(self) -> ConnectivityStatus:
        """Attempt to connect to known hosts and return status."""
        for host, port in self._hosts:
            if self._try_connect(host, port):
                self._connected = True
                return ConnectivityStatus(connected=True, method=f"{host}:{port}")
        self._connected = False
        return ConnectivityStatus(connected=False, method="no_reach")

    def _try_connect(self, host: str, port: int) -> bool:
        try:
            with socket.create_connection((host, port), timeout=DEFAULT_TIMEOUT):
                return True
        except (socket.gaierror, socket.timeout, OSError) as e:
            logger.debug("Connection to %s:%d failed: %s", host, port, e)
            return False

    @property
    def is_connected(self) -> bool:
        if self._connected is None:
            return self.check_connectivity().connected
        return self._connected
