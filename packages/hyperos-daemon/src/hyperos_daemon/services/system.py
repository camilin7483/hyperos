"""System information and management service."""

import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class SystemService:
    """Service for system information and management.
    
    Provides methods for:
    - System information (hostname, kernel, distribution)
    - Service management (systemd)
    - Power management (shutdown, reboot, suspend)
    - User management
    """
    
    def __init__(self) -> None:
        pass
    
    def get_hostname(self) -> str:
        """Get system hostname."""
        try:
            result = subprocess.run(
                ["hostname"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error("Failed to get hostname: %s", e)
            return "unknown"
    
    def get_kernel_version(self) -> str:
        """Get kernel version."""
        try:
            result = subprocess.run(
                ["uname", "-r"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error("Failed to get kernel version: %s", e)
            return "unknown"
    
    def get_distribution_info(self) -> dict:
        """Get distribution information."""
        info = {
            "name": "HyperOS",
            "version": "0.5.0",
            "id": "hyperos",
            "base": "Arch Linux",
        }
        
        try:
            result = subprocess.run(
                ["cat", "/etc/os-release"],
                capture_output=True, text=True, timeout=5
            )
            
            for line in result.stdout.splitlines():
                if "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip('"')
                    
                    if key == "NAME":
                        info["name"] = val
                    elif key == "VERSION":
                        info["version"] = val
                    elif key == "ID":
                        info["id"] = val
        except Exception as e:
            logger.debug("Could not read os-release: %s", e)
        
        return info
    
    def get_uptime(self) -> str:
        """Get system uptime."""
        try:
            result = subprocess.run(
                ["uptime", "-p"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error("Failed to get uptime: %s", e)
            return "unknown"
    
    def get_systemd_failed_units(self) -> list[dict]:
        """Get list of failed systemd units."""
        failed = []
        try:
            result = subprocess.run(
                ["systemctl", "--failed", "--no-pager", "--plain"],
                capture_output=True, text=True, timeout=10
            )
            
            lines = result.stdout.splitlines()
            # Skip header line
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    failed.append({
                        "unit": parts[0],
                        "load": parts[1] if len(parts) > 1 else "",
                        "active": parts[2] if len(parts) > 2 else "",
                        "sub": parts[3] if len(parts) > 3 else "",
                    })
        except Exception as e:
            logger.debug("Could not get failed units: %s", e)
        
        return failed
    
    def is_service_running(self, service_name: str) -> bool:
        """Check if a systemd service is running."""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() == "active"
        except Exception as e:
            logger.error("Failed to check service %s: %s", service_name, e)
            return False
    
    def start_service(self, service_name: str) -> bool:
        """Start a systemd service."""
        logger.info("Starting service: %s", service_name)
        try:
            result = subprocess.run(
                ["systemctl", "start", service_name],
                capture_output=True, text=True, timeout=30
            )
            success = result.returncode == 0
            if not success:
                logger.error("Failed to start %s: %s", service_name, result.stderr)
            return success
        except Exception as e:
            logger.error("Exception starting %s: %s", service_name, e)
            return False
    
    def stop_service(self, service_name: str) -> bool:
        """Stop a systemd service."""
        logger.info("Stopping service: %s", service_name)
        try:
            result = subprocess.run(
                ["systemctl", "stop", service_name],
                capture_output=True, text=True, timeout=30
            )
            success = result.returncode == 0
            if not success:
                logger.error("Failed to stop %s: %s", service_name, result.stderr)
            return success
        except Exception as e:
            logger.error("Exception stopping %s: %s", service_name, e)
            return False
    
    def enable_service(self, service_name: str) -> bool:
        """Enable a systemd service."""
        logger.info("Enabling service: %s", service_name)
        try:
            result = subprocess.run(
                ["systemctl", "enable", service_name],
                capture_output=True, text=True, timeout=30
            )
            success = result.returncode == 0
            if not success:
                logger.error("Failed to enable %s: %s", service_name, result.stderr)
            return success
        except Exception as e:
            logger.error("Exception enabling %s: %s", service_name, e)
            return False
    
    def shutdown(self) -> bool:
        """Shutdown the system."""
        logger.info("Initiating system shutdown")
        try:
            result = subprocess.run(
                ["systemctl", "poweroff"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to shutdown: %s", e)
            return False
    
    def reboot(self) -> bool:
        """Reboot the system."""
        logger.info("Initiating system reboot")
        try:
            result = subprocess.run(
                ["systemctl", "reboot"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to reboot: %s", e)
            return False
    
    def suspend(self) -> bool:
        """Suspend the system."""
        logger.info("Initiating system suspend")
        try:
            result = subprocess.run(
                ["systemctl", "suspend"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to suspend: %s", e)
            return False
    
    def get_all_system_info(self) -> dict:
        """Get comprehensive system information."""
        return {
            "hostname": self.get_hostname(),
            "kernel": self.get_kernel_version(),
            "distribution": self.get_distribution_info(),
            "uptime": self.get_uptime(),
            "failed_units": self.get_systemd_failed_units(),
        }
