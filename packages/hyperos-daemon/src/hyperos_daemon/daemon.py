"""Main daemon class for HyperOS."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class HyperOSDaemon:
    """Central daemon for HyperOS system operations.
    
    This daemon provides:
    - Hardware detection and monitoring
    - Package management operations
    - System configuration
    - D-Bus API for GUI applications
    - Centralized logging
    - Security validation
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        use_dbus: bool = True,
    ) -> None:
        self.config_path = config_path or Path("/etc/hyperos/daemon.conf")
        self.use_dbus = use_dbus
        self._running = False
        
        # Initialize services
        self._dbus_service: Optional[object] = None
        self._hardware_service: Optional[object] = None
        self._package_service: Optional[object] = None
        self._system_service: Optional[object] = None
        
    def start(self) -> None:
        """Start the daemon and all services."""
        logger.info("Starting HyperOS daemon...")
        
        # Load configuration
        self._load_config()
        
        # Initialize D-Bus if enabled
        if self.use_dbus:
            self._init_dbus()
        
        # Initialize services
        self._init_services()
        
        self._running = True
        logger.info("HyperOS daemon started successfully")
        
        # Main loop (when using D-Bus, this blocks)
        if self.use_dbus and self._dbus_service:
            self._run_main_loop()
    
    def stop(self) -> None:
        """Stop the daemon and cleanup resources."""
        logger.info("Stopping HyperOS daemon...")
        self._running = False
        
        # Cleanup services
        self._cleanup_services()
        
        # Cleanup D-Bus
        if self._dbus_service:
            self._cleanup_dbus()
        
        logger.info("HyperOS daemon stopped")
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            logger.info("Loading configuration from %s", self.config_path)
            # TODO: Implement config loading
        else:
            logger.info("Using default configuration")
    
    def _init_dbus(self) -> None:
        """Initialize D-Bus service."""
        try:
            from hyperos_daemon.dbus.service import DBusService
            self._dbus_service = DBusService(self)
            logger.info("D-Bus service initialized")
        except ImportError as e:
            logger.warning("D-Bus not available: %s", e)
            self._dbus_service = None
    
    def _init_services(self) -> None:
        """Initialize all daemon services."""
        from hyperos_daemon.services.hardware import HardwareService
        from hyperos_daemon.services.package import PackageService
        from hyperos_daemon.services.system import SystemService
        
        self._hardware_service = HardwareService()
        self._package_service = PackageService()
        self._system_service = SystemService()
        
        logger.info("Services initialized: hardware, package, system")
    
    def _cleanup_services(self) -> None:
        """Cleanup all services."""
        # TODO: Implement proper cleanup
        pass
    
    def _cleanup_dbus(self) -> None:
        """Cleanup D-Bus connection."""
        if self._dbus_service and hasattr(self._dbus_service, 'disconnect'):
            self._dbus_service.disconnect()
    
    def _run_main_loop(self) -> None:
        """Run the main event loop."""
        if self._dbus_service and hasattr(self._dbus_service, 'run'):
            self._dbus_service.run()
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def hardware_service(self):
        return self._hardware_service
    
    @property
    def package_service(self):
        return self._package_service
    
    @property
    def system_service(self):
        return self._system_service
