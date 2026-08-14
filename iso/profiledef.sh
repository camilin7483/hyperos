#!/usr/bin/env bash
# Profile definition for HyperOS ISO
# Built on top of Arch Linux with Hyprland and HyperOS applications

source /usr/share/archiso/configs/default/profiledef.sh

# Override default values
iso_name="hyperos"
iso_label="HYPEROS_$(date +%Y%m)"
iso_publisher="HyperOS Team <https://hyperos.dev>"
iso_application="HyperOS Live/Install Environment"
iso_version="$(cat /workspace/VERSION 2>/dev/null || echo '0.5.0')"
install_dir="arch"
buildmodes=('iso')
bootmodes=('bios.syslinux.mbr' 'bios.syslinux.raid' 'efi-x64.grub' 'efi-x64.systemd-boot')
arch="x86_64"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
file_permissions=(
    ["/root"]="750"
    ["/etc/shadow"]="000"
    ["/etc/gshadow"]="000"
    ["/root/.automated_script.sh"]="755"
)

# Custom packages from local repository
# These will be added by the build script
packages_x86_64=(
    # Base system
    base
    linux
    linux-firmware
    systemd
    systemd-sysvcompat
    
    # Bootloader
    efibootmgr
    grub
    os-prober
    
    # Filesystems
    btrfs
    dosfstools
    e2fsprogs
    f2fs-tools
    lvm2
    mdadm
    xfsprogs
    
    # Network
    networkmanager
    network-manager-applet
    iwd
    wpa_supplicant
    dnsmasq
    
    # Audio
    pipewire
    pipewire-alsa
    pipewire-pulse
    pipewire-jack
    wireplumber
    pavucontrol
    
    # Bluetooth
    bluez
    bluez-utils
    blueman
    
    # Graphics & Wayland
    mesa
    vulkan-radeon
    vulkan-intel
    vulkan-nouveau
    libva
    libva-utils
    vaapi-intel-driver
    intel-media-driver
    nvidia-dkms
    nvidia-utils
    nvidia-settings
    xf86-video-amdgpu
    xf86-video-ati
    xf86-video-nouveau
    xf86-video-vesa
    
    # Hyprland & Desktop
    hyprland
    waybar
    kitty
    dolphin
    sddm
    qt5-wayland
    qt6-wayland
    
    # XDG Portals
    xdg-desktop-portal
    xdg-desktop-portal-hyprland
    xdg-desktop-portal-gtk
    
    # Fonts
    noto-fonts
    noto-fonts-cjk
    noto-fonts-emoji
    ttf-dejavu
    ttf-liberation
    ttf-jetbrains-mono
    
    # Utilities
    vim
    nano
    git
    wget
    curl
    htop
    neofetch
    file-roller
    archinstall
    pacman-contrib
    reflector
    
    # HyperOS Applications (will be installed from local repo)
    # hyper-center
    # hyper-settings
    # hyper-store
    # hyper-update
    # hyper-drivers
    # hyper-backup
    # hyper-assistant
    # hyper-welcome
    # hyper-installer
    # hyper-cli
    # hyperos-daemon
)

# Packages to remove from the base profile
remove_packages=(
    usb_modesetting
    wvdial
    rp-pppoe
    ppp
    pptpclient
    openconnect
    networkmanager-openconnect
    networkmanager-openvpn
    networkmanager-pptp
    networkmanager-vpnc
)

# Hooks for customization
airootfs_file="airootfs"
hooks=(
    "90-mkinitcpio-remove-defaults.hook"
)
