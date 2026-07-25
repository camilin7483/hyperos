import logging
import subprocess
from typing import Optional

from hyperos_core.domain.models import PowerProfile
from hyperos_core.domain.enums import PowerProfileType

logger = logging.getLogger(__name__)

PROFILES = {
    PowerProfileType.BALANCED: PowerProfile(
        name="balanced", label="Balanced",
        description="Default power profile for daily use",
        cpu_governor="schedutil", swappiness=60,
        screen_timeout=300, performance_mode="balanced",
    ),
    PowerProfileType.PERFORMANCE: PowerProfile(
        name="performance", label="Performance",
        description="Maximum performance for demanding tasks",
        cpu_governor="performance", swappiness=10,
        screen_timeout=600, performance_mode="performance",
    ),
    PowerProfileType.POWER_SAVE: PowerProfile(
        name="powersave", label="Power Saver",
        description="Battery saving mode for maximum efficiency",
        cpu_governor="powersave", swappiness=100,
        screen_timeout=120, performance_mode="powersave",
    ),
    PowerProfileType.GAMING: PowerProfile(
        name="gaming", label="Gaming",
        description="Optimized for gaming with reduced latency",
        cpu_governor="performance", swappiness=10,
        screen_timeout=0, performance_mode="gaming",
    ),
}


class PowerService:
    def get_profiles(self) -> list[PowerProfile]:
        profiles = []
        current = self.get_current_governor()
        for profile_type, profile in PROFILES.items():
            p = PowerProfile(
                name=profile.name,
                label=profile.label,
                description=profile.description,
                cpu_governor=profile.cpu_governor,
                swappiness=profile.swappiness,
                screen_timeout=profile.screen_timeout,
                performance_mode=profile.performance_mode,
                is_active=profile.cpu_governor == current,
            )
            profiles.append(p)
        return profiles

    def get_current_governor(self) -> str:
        try:
            result = subprocess.run(
                ["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not get current governor: %s", e)
        return "schedutil"

    def apply_profile(self, profile: PowerProfileType) -> bool:
        p = PROFILES.get(profile)
        if not p:
            return False
        try:
            subprocess.run(
                ["sudo", "sh", "-c",
                 f"echo {p.cpu_governor} | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null"],
                capture_output=True, text=True, timeout=10,
            )
            logger.info("Applied power profile: %s", p.name)
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error("Failed to apply profile %s: %s", p.name, e)
        return False

    def get_battery_status(self) -> Optional[dict]:
        try:
            import glob
            for path in glob.glob("/sys/class/power_supply/BAT*"):
                with open(f"{path}/capacity") as f:
                    capacity = int(f.read().strip())
                with open(f"{path}/status") as f:
                    status = f.read().strip()
                return {"capacity": capacity, "status": status}
        except (FileNotFoundError, PermissionError, ValueError) as e:
            logger.debug("Could not read battery info: %s", e)
        return None

    def set_screen_brightness(self, percent: int) -> bool:
        try:
            subprocess.run(
                ["brightnessctl", "set", f"{percent}%"],
                capture_output=True, text=True, timeout=5,
            )
            return True
        except FileNotFoundError:
            try:
                with open("/sys/class/backlight/*/brightness", "w") as f:
                    pass
            except (FileNotFoundError, PermissionError):
                pass
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug("Could not set brightness: %s", e)
        return False
