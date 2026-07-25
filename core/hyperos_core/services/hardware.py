import logging
import subprocess

logger = logging.getLogger(__name__)


class HardwareService:
    def detect_gpu_driver(self) -> str:
        try:
            result = subprocess.run(
                ["lspci", "-nn"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.splitlines():
                lower = line.lower()
                if "vga" in lower or "3d" in lower:
                    if "nvidia" in lower:
                        return "nvidia"
                    elif "amd" in lower or "advanced micro devices" in lower:
                        return "amd"
                    elif "intel" in lower:
                        return "intel"
                    elif "vmware" in lower or "qxl" in lower or "virtio" in lower:
                        return "vmware"
            return "unknown"
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not detect GPU driver: %s", e)
        return "unknown"

    def is_nvidia_prime(self) -> bool:
        try:
            result = subprocess.run(
                ["prime-select", "query"],
                capture_output=True, text=True, timeout=5,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def get_nvidia_version(self) -> str:
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        return ""

    def get_kernel_modules(self) -> list[str]:
        try:
            result = subprocess.run(
                ["lsmod"],
                capture_output=True, text=True, timeout=5,
            )
            modules = []
            for line in result.stdout.splitlines()[1:]:
                parts = line.split()
                if parts:
                    modules.append(parts[0])
            return modules
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not list kernel modules: %s", e)
        return []

    def is_module_loaded(self, module: str) -> bool:
        return module in self.get_kernel_modules()

    def get_firmware_info(self) -> list[str]:
        try:
            result = subprocess.run(
                ["fwupdmgr", "get-devices", "--json"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                devices = []
                for device in data.get("Devices", []):
                    devices.append(f"{device.get('Name', 'Unknown')} - {device.get('Version', '?')}")
                return devices
        except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError) as e:
            logger.debug("Could not get firmware info: %s", e)
        return []

    def detect_bluetooth(self) -> bool:
        try:
            result = subprocess.run(
                ["hciconfig"],
                capture_output=True, text=True, timeout=5,
            )
            return "UP" in result.stdout.upper()
        except FileNotFoundError:
            try:
                result = subprocess.run(
                    ["bluetoothctl", "show"],
                    capture_output=True, text=True, timeout=5,
                )
                return result.returncode == 0
            except FileNotFoundError:
                return False
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not detect bluetooth: %s", e)
        return False

    def detect_printers(self) -> list[str]:
        try:
            result = subprocess.run(
                ["lpstat", "-p"],
                capture_output=True, text=True, timeout=10,
            )
            printers = []
            for line in result.stdout.splitlines():
                if line.startswith("printer"):
                    parts = line.split()
                    if len(parts) >= 2:
                        printers.append(parts[1])
            return printers
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not detect printers: %s", e)
        return []

    def get_cpu_governor(self) -> str:
        try:
            result = subprocess.run(
                ["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not get CPU governor: %s", e)
        return "unknown"

    def get_thermal_zones(self) -> list[dict]:
        zones = []
        try:
            import glob
            for path in sorted(glob.glob("/sys/class/thermal/thermal_zone*")):
                try:
                    with open(f"{path}/type") as f:
                        zone_type = f.read().strip()
                    with open(f"{path}/temp") as f:
                        temp = int(f.read().strip()) / 1000
                    zones.append({"type": zone_type, "temperature": temp})
                except (FileNotFoundError, PermissionError, ValueError):
                    pass
        except Exception as e:
            logger.debug("Could not read thermal zones: %s", e)
        return zones
