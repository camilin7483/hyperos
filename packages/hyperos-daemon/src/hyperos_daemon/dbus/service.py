"""D-Bus service for HyperOS daemon."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hyperos_daemon.daemon import HyperOSDaemon

logger = logging.getLogger(__name__)

# D-Bus service configuration
DBUS_SERVICE_NAME = "org.hyperos.Daemon"
DBUS_OBJECT_PATH = "/org/hyperos/Daemon"
DBUS_INTERFACE = "org.hyperos.Daemon"


class DBusService:
    """D-Bus service exposing HyperOS daemon functionality.
    
    This class registers with the system D-Bus and exposes methods
    for GUI applications to interact with system services safely.
    """
    
    def __init__(self, daemon: "HyperOSDaemon") -> None:
        self.daemon = daemon
        self._connection = None
        self._registration = None
        
        try:
            import dbus
            import dbus.service
            import dbus.mainloop.glib
            from gi.repository import GLib
            
            # Setup main loop
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            self._main_loop = GLib.MainLoop()
            
            # Get system bus
            self._bus = dbus.SystemBus()
            
            # Request name
            self._name = dbus.service.BusName(DBUS_SERVICE_NAME, self._bus)
            
            logger.info("D-Bus service registered as %s", DBUS_SERVICE_NAME)
            
        except ImportError as e:
            logger.error("D-Bus dependencies not available: %s", e)
            raise
    
    def run(self) -> None:
        """Run the D-Bus main loop."""
        if self._main_loop:
            logger.info("Starting D-Bus main loop")
            self._main_loop.run()
    
    def stop(self) -> None:
        """Stop the D-Bus main loop."""
        if self._main_loop:
            self._main_loop.quit()
            logger.info("D-Bus main loop stopped")
    
    def disconnect(self) -> None:
        """Disconnect from D-Bus."""
        self.stop()
        if hasattr(self, '_name') and self._name:
            self._name = None


class DaemonObject(dbus.service.Object):
    """D-Bus object implementing HyperOS daemon methods."""
    
    def __init__(self, daemon: "HyperOSDaemon", bus=None, object_path=None):
        if bus is None:
            bus = dbus.SystemBus()
        if object_path is None:
            object_path = DBUS_OBJECT_PATH
        
        super().__init__(bus, object_path)
        self.daemon = daemon
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="s")
    def GetVersion(self) -> str:
        """Return daemon version."""
        return "0.1.0"
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="b")
    def IsRunning(self) -> bool:
        """Check if daemon is running."""
        return self.daemon.is_running
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="a{sv}")
    def GetSystemInfo(self) -> dict:
        """Get system information."""
        # TODO: Implement actual system info retrieval
        return {
            "hostname": "hyperos",
            "kernel": "unknown",
            "distribution": "HyperOS",
        }
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="s", out_signature="b")
    def InstallPackage(self, package_name: str) -> bool:
        """Install a package (requires authorization)."""
        logger.info("Install package requested: %s", package_name)
        # TODO: Implement with polkit authorization
        return False
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="s", out_signature="b")
    def RemovePackage(self, package_name: str) -> bool:
        """Remove a package (requires authorization)."""
        logger.info("Remove package requested: %s", package_name)
        # TODO: Implement with polkit authorization
        return False
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="b")
    def UpdateSystem(self) -> bool:
        """Update the system (requires authorization)."""
        logger.info("System update requested")
        # TODO: Implement with polkit authorization
        return False
    
    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="a{sv}")
    def GetHardwareInfo(self) -> dict:
        """Get hardware information."""
        # TODO: Implement actual hardware detection
        return {
            "cpu": "unknown",
            "memory": 0,
            "gpu": "unknown",
        }
