#!/usr/bin/env bash
# shellcheck disable=SC2086,SC2329
# Automated script for HyperOS Live Environment
# This script runs on first boot of the Live ISO

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Wait for network to be ready
log_info "Waiting for network connectivity..."
for i in {1..30}; do
    if ping -c 1 -W 1 archlinux.org &>/dev/null; then
        log_info "Network is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        log_warn "Network not ready after 30 seconds, continuing anyway"
    fi
    sleep 1
done

# Update mirrorlist for better download speeds
if command -v reflector &>/dev/null; then
    log_info "Updating mirrorlist..."
    reflector --country 'United States' --age 12 --protocol https --sort rate --save /etc/pacman.d/mirrorlist 2>/dev/null || true
fi

# Set up HyperOS local repository in live environment
REPO_DIR="/run/archiso/airootfs/repo"
if [ -d "$REPO_DIR" ]; then
    log_info "Setting up HyperOS local repository..."
    
    # Add hyperos repo to pacman.conf if not already present
    if ! grep -q "\[hyperos\]" /etc/pacman.conf; then
        cat >> /etc/pacman.conf << 'EOF'

[hyperos]
SigLevel = Optional TrustAll
Server = file:///run/archiso/airootfs/repo
EOF
        log_info "HyperOS repository added to pacman.conf"
    fi
    
    # Update package database
    pacman -Sy --noconfirm 2>/dev/null || true
fi

# Enable NetworkManager
log_info "Enabling NetworkManager..."
systemctl enable NetworkManager.service
systemctl start NetworkManager.service

# Enable Bluetooth
if command -v bluetoothctl &>/dev/null; then
    log_info "Enabling Bluetooth service..."
    systemctl enable bluetooth.service
    systemctl start bluetooth.service
fi

# Enable audio services
log_info "Starting audio services..."
systemctl --user daemon-reexec 2>/dev/null || true
systemctl --user enable pipewire.socket 2>/dev/null || true
systemctl --user enable pipewire-pulse.socket 2>/dev/null || true
systemctl --user enable wireplumber.service 2>/dev/null || true

# Copy default configurations to root user
log_info "Setting up default configurations..."
if [ -d "/etc/skel/.config" ]; then
    cp -r /etc/skel/.config/* /root/.config/ 2>/dev/null || true
fi

# Set proper permissions
chmod 755 /root/.config 2>/dev/null || true

# Welcome message
cat << 'EOF'

╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   Welcome to HyperOS Live Environment!                ║
║                                                       ║
║   • Network: NetworkManager enabled                   ║
║   • Audio: PipeWire configured                        ║
║   • Desktop: Hyprland ready                           ║
║   • Installer: Run 'hyper-installer' to install       ║
║                                                       ║
║   Type 'hyper-welcome' to see the welcome screen      ║
║   Type 'hyper-center' to open system center           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝

EOF

log_info "Live environment setup complete!"

# Launch HyperOS Welcome automatically (optional)
# Uncomment the following line to auto-launch on boot
# hyper-welcome &

exit 0
