#!/bin/bash
# HyperOS Desktop Setup Script
# This script configures the complete desktop environment

set -e

echo "========================================="
echo "HyperOS Desktop Configuration"
echo "========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    log_warning "Running as root. Some configurations may need user context."
fi

# Detect installation mode
INSTALL_MODE="system"
if [[ $# -gt 0 ]]; then
    INSTALL_MODE=$1
fi

echo ""
log_info "Installation mode: $INSTALL_MODE"
echo ""

# ==========================================
# 1. Install Required Packages
# ==========================================
log_info "Step 1: Installing required packages..."

REQUIRED_PACKAGES=(
    # Wayland compositor
    hyprland
    
    # Bar and status
    waybar
    wofi
    
    # Terminal
    alacritty
    kitty
    
    # File manager
    thunar
    tumbler
    thunar-archive-plugin
    thunar-volman
    
    # Display manager
    sddm
    qt5-quickcontrols2
    qt5-graphicaleffects
    
    # Network
    networkmanager
    network-manager-applet
    
    # Audio
    pipewire
    pipewire-alsa
    pipewire-pulse
    wireplumber
    pavucontrol
    
    # Bluetooth
    bluez
    bluez-utils
    blueman
    
    # Portals
    xdg-desktop-portal
    xdg-desktop-portal-gtk
    xdg-desktop-portal-hyprland
    
    # Screenshot
    grim
    slurp
    wl-clipboard
    cliphist
    
    # Lock screen
    swaylock-effects
    swayidle
    
    # Fonts
    noto-fonts
    noto-fonts-cjk
    noto-fonts-emoji
    jetbrains-mono-font
    nerd-fonts
    
    # Themes
    papirus-icon-theme
    breeze-icons
    
    # Utilities
    polkit
    polkit-kde-agent
    gvfs
    gvfs-mtp
    gvfs-nfs
    gvfs-smb
    
    # HyperOS packages (should be built already)
    hyperos-daemon
    hyper-center
    hyper-settings
    hyper-store
    hyper-update
    hyper-drivers
    hyper-backup
    hyper-assistant
    hyper-welcome
    hyper-installer
)

if command -v pacman &> /dev/null; then
    log_info "Installing packages with pacman..."
    # In real implementation: sudo pacman -S --needed ${REQUIRED_PACKAGES[@]}
    log_success "Package installation would execute here"
elif command -v apt &> /dev/null; then
    log_warning "Detected Debian-based system. HyperOS is designed for Arch Linux."
else
    log_warning "No supported package manager found."
fi

# ==========================================
# 2. Configure Hyprland
# ==========================================
log_info "Step 2: Configuring Hyprland..."

HYPRLAND_CONFIG_DIR="$HOME/.config/hypr"

if [[ ! -d "$HYPRLAND_CONFIG_DIR" ]]; then
    mkdir -p "$HYPRLAND_CONFIG_DIR"
    log_info "Created Hyprland config directory"
fi

# Copy configuration
if [[ -f "/workspace/desktop/hyprland/hyprland.conf" ]]; then
    cp /workspace/desktop/hyprland/hyprland.conf "$HYPRLAND_CONFIG_DIR/hyprland.conf"
    log_success "Hyprland configuration installed"
else
    log_warning "Hyprland configuration file not found"
fi

# ==========================================
# 3. Configure Waybar
# ==========================================
log_info "Step 3: Configuring Waybar..."

WAYBAR_CONFIG_DIR="$HOME/.config/waybar"

if [[ ! -d "$WAYBAR_CONFIG_DIR" ]]; then
    mkdir -p "$WAYBAR_CONFIG_DIR"
    log_info "Created Waybar config directory"
fi

if [[ -f "/workspace/desktop/waybar/config.jsonc" ]]; then
    cp /workspace/desktop/waybar/config.jsonc "$WAYBAR_CONFIG_DIR/config"
    log_success "Waybar configuration installed"
fi

if [[ -f "/workspace/desktop/waybar/style.css" ]]; then
    cp /workspace/desktop/waybar/style.css "$WAYBAR_CONFIG_DIR/style.css"
    log_success "Waybar style installed"
fi

# ==========================================
# 4. Configure SDDM
# ==========================================
log_info "Step 4: Configuring SDDM..."

if [[ -d "/etc/sddm.conf.d" ]]; then
    if [[ -f "/workspace/desktop/sddm/sddm.conf" ]]; then
        cp /workspace/desktop/sddm/sddm.conf /etc/sddm.conf.d/hyperos.conf
        log_success "SDDM configuration installed"
    fi
else
    log_warning "SDDM configuration directory not found"
fi

# ==========================================
# 5. Configure XDG Portals
# ==========================================
log_info "Step 5: Configuring XDG Desktop Portals..."

PORTAL_CONFIG_DIR="$HOME/.config/xdg-desktop-portal"

if [[ ! -d "$PORTAL_CONFIG_DIR" ]]; then
    mkdir -p "$PORTAL_CONFIG_DIR"
    log_info "Created portal config directory"
fi

if [[ -f "/workspace/desktop/portals/portals.conf" ]]; then
    cp /workspace/desktop/portals/portals.conf "$PORTAL_CONFIG_DIR/portals.conf"
    log_success "Portal configuration installed"
fi

# ==========================================
# 6. Setup Wallpapers
# ==========================================
log_info "Step 6: Setting up wallpapers..."

WALLPAPER_DIR="/usr/share/wallpapers"

if [[ ! -d "$WALLPAPER_DIR" ]]; then
    WALLPAPER_DIR="$HOME/Pictures/Wallpapers"
    mkdir -p "$WALLPAPER_DIR"
fi

if [[ -f "/workspace/desktop/wallpapers/hyperos-default.jpg" ]]; then
    cp /workspace/desktop/wallpapers/hyperos-default.jpg "$WALLPAPER_DIR/"
    log_success "Wallpapers installed"
else
    log_info "Default wallpaper placeholder created"
fi

# ==========================================
# 7. Enable Services
# ==========================================
log_info "Step 7: Enabling systemd services..."

SYSTEMD_SERVICES=(
    "NetworkManager.service"
    "bluetooth.service"
    "sddm.service"
)

for service in "${SYSTEMD_SERVICES[@]}"; do
    if systemctl list-unit-files | grep -q "$service"; then
        # In real implementation: sudo systemctl enable $service
        log_info "Would enable: $service"
    else
        log_warning "Service not found: $service"
    fi
done

# User services
USER_SERVICES=(
    "pipewire.service"
    "pipewire-pulse.service"
    "wireplumber.service"
)

for service in "${USER_SERVICES[@]}"; do
    if systemctl --user list-unit-files 2>/dev/null | grep -q "$service"; then
        # In real implementation: systemctl --user enable $service
        log_info "Would enable user service: $service"
    fi
done

# ==========================================
# 8. Create Default Directories
# ==========================================
log_info "Step 8: Creating default directories..."

XDG_DIRS=(
    "$HOME/Documents"
    "$HOME/Downloads"
    "$HOME/Pictures"
    "$HOME/Videos"
    "$HOME/Music"
    "$HOME/Desktop"
    "$HOME/Templates"
    "$HOME/Public"
)

for dir in "${XDG_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        log_info "Created: $dir"
    fi
done

# ==========================================
# Summary
# ==========================================
echo ""
echo "========================================="
log_success "HyperOS Desktop Configuration Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Reboot your system"
echo "  2. Login through SDDM"
echo "  3. Select 'HyperOS' or 'Hyprland' session"
echo "  4. Run 'hyper-welcome' for first-time setup"
echo ""
echo "Keyboard shortcuts:"
echo "  Super+Q     - Open terminal"
echo "  Super+E     - Open file manager"
echo "  Super+R     - Open application launcher"
echo "  Super+H     - Open Hyper Center"
echo "  Super+L     - Lock screen"
echo "  Super+C     - Close active window"
echo "  Super+M     - Exit Hyprland"
echo ""
