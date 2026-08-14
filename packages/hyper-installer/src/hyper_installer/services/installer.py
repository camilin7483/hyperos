"""
HyperOS Installer Service - Real Installation Implementation
Handles disk partitioning, formatting, pacstrap, and system configuration
"""

import logging
import subprocess
import os
import time
from typing import Callable, Optional, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class InstallConfig:
    """Installation configuration"""
    target_disk: str
    filesystem: str = "btrfs"
    encrypt: bool = False
    username: str = ""
    password: str = ""
    hostname: str = "hyperos"
    language: str = "en_US.UTF-8"
    timezone: str = "America/New_York"
    keyboard: str = "us"
    packages: list = field(default_factory=lambda: [
        "base", "linux", "linux-firmware", "systemd", "networkmanager",
        "pipewire", "pipewire-pulse", "pipewire-alsa", "wireplumber",
        "bluetooth", "bluez", "bluez-utils", "sddm", "qt6-wayland",
        "hyprland", "waybar", "dunst", "polkit-kde-agent", "xdg-desktop-portal-gtk",
        "hyper-center", "hyper-settings", "hyper-store", "hyper-update",
        "hyper-drivers", "hyper-backup", "hyper-welcome", "hyper-tools"
    ])
    
    @property
    def efi_partition(self) -> str:
        return f"{self.target_disk}1"
    
    @property
    def root_partition(self) -> str:
        return f"{self.target_disk}2" if not self.encrypt else f"{self.target_disk}3"
    
    @property
    def swap_partition(self) -> str:
        return f"{self.target_disk}3" if not self.encrypt else f"{self.target_disk}4"


class HyperInstaller:
    """Real HyperOS installer with actual disk operations"""
    
    def __init__(self, config: dict):
        self.config = InstallConfig(**config)
        self.on_progress: Optional[Callable[[int, str], None]] = None
        self._mount_point = "/mnt"
        
    def _report(self, percent: int, message: str):
        """Report progress to UI"""
        logger.info(f"[{percent}%] {message}")
        if self.on_progress:
            self.on_progress(percent, message)
    
    def _run(self, cmd: list, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
        """Run command with error handling"""
        logger.debug(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd, 
                check=check, 
                capture_output=capture, 
                text=True,
                timeout=300
            )
            if capture:
                logger.debug(f"Output: {result.stdout}")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e}")
            raise
    
    def _is_uefi(self) -> bool:
        """Check if system is UEFI"""
        return os.path.exists("/sys/firmware/efi/efivars")
    
    def _partition_disk(self):
        """Create GPT partitions using parted"""
        self._report(5, f"Partitioning {self.config.target_disk}...")
        
        # Wipe existing partition table
        self._run(["wipefs", "-af", self.config.target_disk])
        
        # Create GPT partition table
        self._run(["parted", self.config.target_disk, "--script", "mklabel gpt"])
        
        # Create EFI partition (512MB)
        self._run([
            "parted", self.config.target_disk, "--script",
            "mkpart primary fat32 1MiB 513MiB",
            "set 1 esp on",
            "set 1 boot on"
        ])
        
        # Create root partition (remaining space minus swap)
        self._run([
            "parted", self.config.target_disk, "--script",
            "mkpart primary ext4 513MiB -8GiB"
        ])
        
        # Create swap partition (8GB)
        self._run([
            "parted", self.config.target_disk, "--script",
            "mkpart primary linux-swap -8GiB 100%"
        ])
        
        # Wait for kernel to recognize partitions
        self._run(["partprobe", self.config.target_disk], check=False)
        time.sleep(2)
        
        self._report(10, "Partitioning complete")
    
    def _format_partitions(self):
        """Format partitions with appropriate filesystems"""
        self._report(15, "Formatting partitions...")
        
        # Format EFI partition
        self._run(["mkfs.vfat", "-F32", f"{self.config.target_disk}1"])
        
        # Format root partition
        if self.config.filesystem == "btrfs":
            self._run(["mkfs.btrfs", "-f", f"{self.config.target_disk}2"])
        else:
            self._run(["mkfs.ext4", "-F", f"{self.config.target_disk}2"])
        
        # Format swap
        self._run(["mkswap", f"{self.config.target_disk}3"])
        
        self._report(20, "Formatting complete")
    
    def _mount_filesystems(self):
        """Mount partitions for installation"""
        self._report(25, "Mounting filesystems...")
        
        # Create mount point
        os.makedirs(self._mount_point, exist_ok=True)
        
        # Mount root
        if self.config.filesystem == "btrfs":
            self._run(["mount", f"{self.config.target_disk}2", self._mount_point])
            # Create subvolumes for btrfs
            self._run(["btrfs", "subvolume", "create", f"{self._mount_point}/@"], check=False)
            self._run(["btrfs", "subvolume", "create", f"{self._mount_point}/@home"], check=False)
            self._run(["umount", self._mount_point])
            self._run(["mount", "-o", "subvol=@", f"{self.config.target_disk}2", self._mount_point])
            os.makedirs(f"{self._mount_point}/home", exist_ok=True)
            self._run(["mount", "-o", "subvol=@home", f"{self.config.target_disk}2", f"{self._mount_point}/home"])
        else:
            self._run(["mount", f"{self.config.target_disk}2", self._mount_point])
            os.makedirs(f"{self._mount_point}/home", exist_ok=True)
        
        # Mount EFI
        os.makedirs(f"{self._mount_point}/boot", exist_ok=True)
        self._run(["mount", f"{self.config.target_disk}1", f"{self._mount_point}/boot"])
        
        # Enable swap
        self._run(["swapon", f"{self.config.target_disk}3"])
        
        self._report(30, "Filesystems mounted")
    
    def _install_base_system(self):
        """Install base Arch Linux system using pacstrap"""
        self._report(35, "Installing base system...")
        
        self._run([
            "pacstrap", "-K", self._mount_point,
            *self.config.packages
        ])
        
        self._report(50, "Base system installed")
    
    def _generate_fstab(self):
        """Generate fstab file"""
        self._report(55, "Generating fstab...")
        self._run(["genfstab", "-U", self._mount_point, ">>", f"{self._mount_point}/etc/fstab"], shell=True)
        self._report(60, "fstab generated")
    
    def _configure_system(self):
        """Configure installed system"""
        self._report(65, "Configuring system...")
        
        # Set timezone
        self._run(["arch-chroot", self._mount_point, "ln", "-sf", f"/usr/share/zoneinfo/{self.config.timezone}", "/etc/localtime"])
        
        # Set locale
        with open(f"{self._mount_point}/etc/locale.gen", "w") as f:
            f.write(f"{self.config.language} UTF-8\n")
        self._run(["arch-chroot", self._mount_point, "locale-gen"])
        with open(f"{self._mount_point}/etc/locale.conf", "w") as f:
            f.write(f"LANG={self.config.language}\n")
        
        # Set hostname
        with open(f"{self._mount_point}/etc/hostname", "w") as f:
            f.write(f"{self.config.hostname}\n")
        with open(f"{self._mount_point}/etc/hosts", "w") as f:
            f.write("127.0.0.1 localhost\n::1 localhost\n127.0.1.1 {self.config.hostname}.localdomain {self.config.hostname}\n")
        
        # Set root password
        self._run(["echo", f"root:{self.config.password}", "|", "chpasswd"], input=f"root:{self.config.password}", check=False)
        
        # Create user
        self._run(["arch-chroot", self._mount_point, "useradd", "-m", "-G", "wheel,audio,video,storage,power,input", "-s", "/bin/bash", self.config.username])
        self._run(["echo", f"{self.config.username}:{self.config.password}", "|", "chpasswd"], input=f"{self.config.username}:{self.config.password}", check=False)
        
        # Enable sudo for wheel group
        self._run(["sed", "-i", "s/# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/", f"{self._mount_point}/etc/sudoers"])
        
        self._report(75, "System configured")
    
    def _install_bootloader(self):
        """Install systemd-boot bootloader"""
        self._report(80, "Installing bootloader...")
        
        if self._is_uefi():
            # Install systemd-boot
            self._run(["arch-chroot", self._mount_point, "bootctl", "install"])
            
            # Create boot entry
            boot_entry = f"""
title   HyperOS
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options root=PARTUUID=$(blkid -s PARTUUID -o value {self.config.root_partition}) rw quiet splash
"""
            os.makedirs(f"{self._mount_point}/boot/loader/entries", exist_ok=True)
            with open(f"{self._mount_point}/boot/loader/entries/hyperos.conf", "w") as f:
                f.write(boot_entry)
            
            # Set default boot entry
            with open(f"{self._mount_point}/boot/loader/loader.conf", "w") as f:
                f.write("default hyperos.conf\ntimeout 3\n")
        else:
            # BIOS fallback - install GRUB
            self._run(["arch-chroot", self._mount_point, "grub-install", "--target=i386-pc", self.config.target_disk])
            self._run(["arch-chroot", self._mount_point, "grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
        
        self._report(90, "Bootloader installed")
    
    def _finalize(self):
        """Finalize installation"""
        self._report(95, "Finalizing installation...")
        
        # Unmount everything
        self._run(["swapoff", "-a"])
        self._run(["umount", "-R", self._mount_point])
        
        self._report(100, "Installation completed successfully!")
    
    def install(self) -> Tuple[bool, str]:
        """Main installation method"""
        try:
            logger.info(f"Starting installation on {self.config.target_disk}")
            
            # Validate configuration
            if not self.config.target_disk.startswith("/dev/"):
                return False, "Invalid target disk"
            
            if not os.path.exists(self.config.target_disk):
                return False, f"Disk {self.config.target_disk} not found"
            
            # Execute installation steps
            self._partition_disk()
            self._format_partitions()
            self._mount_filesystems()
            self._install_base_system()
            self._generate_fstab()
            self._configure_system()
            self._install_bootloader()
            self._finalize()
            
            return True, "Installation completed successfully"
            
        except Exception as e:
            logger.exception("Installation failed")
            return False, f"Installation failed: {str(e)}"
