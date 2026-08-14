"""Hardware detection and monitoring service."""

import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class HardwareService:
    """Service for hardware detection and monitoring.
    
    Provides methods to detect and monitor:
    - CPU information
    - Memory usage
    - Storage devices
    - GPU information
    - Network interfaces
    - Battery status
    """
    
    def __init__(self) -> None:
        self._cache: dict = {}
    
    def get_cpu_info(self) -> dict:
        """Get CPU information."""
        try:
            result = subprocess.run(
                ["cat", "/proc/cpuinfo"],
                capture_output=True, text=True, timeout=5
            )
            
            model = "Unknown"
            cores = 0
            
            for line in result.stdout.splitlines():
                if line.startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                elif line.startswith("cpu cores"):
                    cores = int(line.split(":", 1)[1].strip())
                    break
            
            return {
                "model": model,
                "cores": cores,
            }
        except Exception as e:
            logger.error("Failed to get CPU info: %s", e)
            return {"model": "Unknown", "cores": 0}
    
    def get_memory_info(self) -> dict:
        """Get memory information."""
        try:
            result = subprocess.run(
                ["free", "-m"],
                capture_output=True, text=True, timeout=5
            )
            
            lines = result.stdout.splitlines()
            if len(lines) >= 2:
                parts = lines[1].split()
                total = int(parts[1])
                used = int(parts[2])
                free = int(parts[3])
                
                return {
                    "total_mb": total,
                    "used_mb": used,
                    "free_mb": free,
                    "percent_used": round((used / total) * 100, 1) if total > 0 else 0,
                }
        except Exception as e:
            logger.error("Failed to get memory info: %s", e)
        
        return {"total_mb": 0, "used_mb": 0, "free_mb": 0, "percent_used": 0}
    
    def get_storage_info(self) -> list[dict]:
        """Get storage device information."""
        devices = []
        try:
            result = subprocess.run(
                ["lsblk", "-d", "-o", "NAME,SIZE,TYPE,MODEL", "--json"],
                capture_output=True, text=True, timeout=10
            )
            
            import json
            data = json.loads(result.stdout)
            
            for blockdev in data.get("blockdevices", []):
                devices.append({
                    "name": f"/dev/{blockdev.get('name', 'unknown')}",
                    "size": blockdev.get("size", "Unknown"),
                    "type": blockdev.get("type", "Unknown"),
                    "model": blockdev.get("model", "Unknown"),
                })
        except Exception as e:
            logger.error("Failed to get storage info: %s", e)
        
        return devices
    
    def get_gpu_info(self) -> list[dict]:
        """Get GPU information."""
        gpus = []
        
        # Try lspci first
        try:
            result = subprocess.run(
                ["lspci", "-nn"],
                capture_output=True, text=True, timeout=10
            )
            
            for line in result.stdout.splitlines():
                if "VGA" in line or "3D" in line or "Display" in line:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        gpus.append({
                            "id": parts[0].strip(),
                            "name": ":".join(parts[2:]).strip(),
                            "vendor": self._detect_vendor(parts[2]),
                        })
        except Exception as e:
            logger.debug("lspci failed: %s", e)
        
        # If no GPUs found via lspci, try nvidia-smi
        if not gpus:
            try:
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                    capture_output=True, text=True, timeout=5
                )
                for line in result.stdout.splitlines():
                    gpus.append({
                        "id": "nvidia",
                        "name": line.strip(),
                        "vendor": "NVIDIA",
                    })
            except Exception:
                pass
        
        return gpus or [{"id": "unknown", "name": "Unknown", "vendor": "Unknown"}]
    
    def _detect_vendor(self, pci_string: str) -> str:
        """Detect GPU vendor from PCI string."""
        pci_lower = pci_string.lower()
        if "nvidia" in pci_lower:
            return "NVIDIA"
        elif "amd" in pci_lower or "ati" in pci_lower:
            return "AMD"
        elif "intel" in pci_lower:
            return "Intel"
        return "Unknown"
    
    def get_network_interfaces(self) -> list[dict]:
        """Get network interface information."""
        interfaces = []
        try:
            result = subprocess.run(
                ["ip", "-j", "link"],
                capture_output=True, text=True, timeout=5
            )
            
            import json
            data = json.loads(result.stdout)
            
            for iface in data:
                interfaces.append({
                    "name": iface.get("ifname", "unknown"),
                    "state": iface.get("operstate", "unknown"),
                    "type": iface.get("link_type", "unknown"),
                })
        except Exception as e:
            logger.error("Failed to get network interfaces: %s", e)
        
        return interfaces
    
    def get_battery_info(self) -> dict:
        """Get battery information (for laptops)."""
        try:
            result = subprocess.run(
                ["cat", "/sys/class/power_supply/BAT0/capacity"],
                capture_output=True, text=True, timeout=5
            )
            capacity = int(result.stdout.strip())
            
            result = subprocess.run(
                ["cat", "/sys/class/power_supply/BAT0/status"],
                capture_output=True, text=True, timeout=5
            )
            status = result.stdout.strip()
            
            return {
                "present": True,
                "capacity": capacity,
                "status": status,
            }
        except Exception:
            return {"present": False, "capacity": 0, "status": "Unknown"}
    
    def get_all_hardware_info(self) -> dict:
        """Get comprehensive hardware information."""
        return {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "storage": self.get_storage_info(),
            "gpu": self.get_gpu_info(),
            "network": self.get_network_interfaces(),
            "battery": self.get_battery_info(),
        }
