#!/usr/bin/env bash
# Test HyperOS ISO in QEMU virtual machine
# This script automates testing the ISO without needing physical hardware

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Configuration
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$WORKSPACE_DIR/build"
VERSION=$(cat "$WORKSPACE_DIR/VERSION" 2>/dev/null || echo "0.5.0")
ISO_NAME="hyperos-${VERSION}-x86_64.iso"
ISO_PATH="$BUILD_DIR/$ISO_NAME"

# QEMU settings
RAM_SIZE="4G"
CPU_CORES="2"
DISK_SIZE="20G"
DISK_FILE="/tmp/hyperos-test-disk.qcow2"
UEFI_CODE="/usr/share/ovmf/x64/OVMF_CODE.fd"
UEFI_VARS="/usr/share/ovmf/x64/OVMF_VARS.fd"
UEFI_VARS_TMP="/tmp/hyperos-ovmf-vars.fd"

# Check if ISO exists
check_iso() {
    log_step "Checking for ISO file..."
    
    if [ ! -f "$ISO_PATH" ]; then
        log_error "ISO not found: $ISO_PATH"
        log_error "Build the ISO first with: ./iso/build-iso.sh"
        exit 1
    fi
    
    log_info "ISO found: $ISO_PATH ($(du -h "$ISO_PATH" | cut -f1))"
}

# Prepare test disk
prepare_disk() {
    log_step "Preparing test disk..."
    
    # Remove old disk if exists
    rm -f "$DISK_FILE" "$UEFI_VARS_TMP"
    
    # Create new disk
    qemu-img create -f qcow2 "$DISK_FILE" "$DISK_SIZE" > /dev/null
    
    # Copy UEFI variables
    if [ -f "$UEFI_VARS" ]; then
        cp "$UEFI_VARS" "$UEFI_VARS_TMP"
        log_info "Test disk created: $DISK_FILE ($DISK_SIZE)"
    else
        log_warn "UEFI variables not found, UEFI boot may not work"
    fi
}

# Run QEMU
run_qemu() {
    log_step "Starting QEMU virtual machine..."
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   HyperOS VM Test Environment                         ║"
    echo "║                                                       ║"
    echo "║   ISO: $ISO_NAME"
    echo "║   RAM: $RAM_SIZE"
    echo "║   CPU: $CPU_CORES cores"
    echo "║   Disk: $DISK_SIZE (temporary)"
    echo "║                                                       ║"
    echo "║   Controls:                                           ║"
    echo "║   - Ctrl+Alt+G: Release mouse                         ║"
    echo "║   - Ctrl+Alt+U: Switch to fullscreen                  ║"
    echo "║   - Ctrl+Alt+F: Toggle window mode                    ║"
    echo "║                                                       ║"
    echo "║   Closing the VM window will exit the test            ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Determine QEMU command based on available features
    local qemu_cmd="qemu-system-x86_64"
    
    if ! command -v "$qemu_cmd" &>/dev/null; then
        log_error "QEMU not found. Install with: sudo pacman -S qemu-base"
        exit 1
    fi
    
    # Build QEMU command
    local qemu_args=(
        "$qemu_cmd"
        -enable-kvm  # Hardware acceleration if available
        -m "$RAM_SIZE"
        -smp "$CPU_CORES"
        "-drive if=pflash,format=raw,readonly=on,file=$UEFI_CODE"
        "-drive if=pflash,format=raw,file=$UEFI_VARS_TMP"
        -cdrom "$ISO_PATH"
        -hda "$DISK_FILE"
        -boot d  # Boot from CD-ROM first
        -usb
        -device usb-tablet
        -device usb-kbd
        -vga virtio
        "-display gtk,gl=on"  # GPU acceleration if available
        "-netdev user,id=net0"
        "-device virtio-net-pci,netdev=net0"
        -soundhw hda  # Audio
    )
    
    # Check if KVM is available
    if [ ! -e "/dev/kvm" ]; then
        log_warn "KVM not available, running without hardware acceleration"
        # Remove -enable-kvm from args
        qemu_args=("${qemu_args[@]/-enable-kvm/}")
    fi
    
    # Run QEMU
    "${qemu_args[@]}" || {
        log_error "QEMU failed to start"
        exit 1
    }
}

# Cleanup
cleanup() {
    log_step "Cleaning up..."
    
    rm -f "$DISK_FILE" "$UEFI_VARS_TMP"
    
    log_info "Cleanup complete"
}

# Show test checklist
show_checklist() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║   HyperOS ISO Test Checklist                          ║"
    echo "╠═══════════════════════════════════════════════════════╣"
    echo "║                                                       ║"
    echo "║   Boot Tests:                                         ║"
    echo "║   □ ISO boots to GRUB/systemd-boot menu               ║"
    echo "║   □ Live environment loads                            ║"
    echo "║   □ No kernel panics or critical errors               ║"
    echo "║                                                       ║"
    echo "║   Desktop Tests:                                      ║"
    echo "║   □ Hyprland starts automatically                     ║"
    echo "║   □ Waybar is visible and functional                  ║"
    echo "║   □ Keyboard shortcuts work (SUPER+D, SUPER+Return)   ║"
    echo "║   □ Windows can be moved and resized                  ║"
    echo "║                                                       ║"
    echo "║   Hardware Tests:                                     ║"
    echo "║   □ Network connectivity (WiFi/Ethernet)              ║"
    echo "║   □ Audio playback works                              ║"
    echo "║   □ Display resolution is correct                     ║"
    echo "║                                                       ║"
    echo "║   Application Tests:                                  ║"
    echo "║   □ hyper-welcome launches                            ║"
    echo "║   □ hyper-center shows system info                    ║"
    echo "║   □ hyper-installer can be launched                   ║"
    echo "║   □ Terminal (kitty) opens                            ║"
    echo "║                                                       ║"
    echo "║   Installation Tests (optional):                      ║"
    echo "║   □ Installer detects disks                           ║"
    echo "║   □ Installation completes successfully               ║"
    echo "║   □ System reboots after installation                 ║"
    echo "║   □ Installed system boots correctly                  ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
}

# Main execution
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   HyperOS ISO Tester v$VERSION                         ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    check_iso
    prepare_disk
    show_checklist
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    run_qemu
}

# Run main function
main "$@"
