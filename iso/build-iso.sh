#!/usr/bin/env bash
# Build script for HyperOS ISO using archiso
# This script builds a bootable ISO image with all HyperOS components

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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
ISO_DIR="$SCRIPT_DIR"
BUILD_DIR="$WORKSPACE_DIR/build/iso"
OUTPUT_DIR="$WORKSPACE_DIR/build"
VERSION=$(cat "$WORKSPACE_DIR/VERSION" 2>/dev/null || echo "0.5.0")
ISO_NAME="hyperos-${VERSION}-x86_64.iso"

# Check dependencies
check_dependencies() {
    log_step "Checking dependencies..."
    
    local deps=("pacman" "makepkg" "archiso" "mkarchiso" "sqfs" "xorriso")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &>/dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${missing[*]}"
        log_error "Install with: sudo pacman -S archiso squashfs-tools libisoburn"
        exit 1
    fi
    
    log_info "All dependencies found"
}

# Prepare build environment
prepare_build() {
    log_step "Preparing build environment..."
    
    # Clean previous builds
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"
    mkdir -p "$OUTPUT_DIR"
    
    # Copy profile
    cp -r "$ISO_DIR"/* "$BUILD_DIR/"
    
    log_info "Build environment prepared"
}

# Build HyperOS packages (if not already built)
build_packages() {
    log_step "Building HyperOS packages..."
    
    cd "$WORKSPACE_DIR"
    
    if [ ! -f "$WORKSPACE_DIR/build/packages-built.flag" ]; then
        ./build.sh packages || {
            log_warn "Package build failed, continuing with available packages"
        }
        touch "$WORKSPACE_DIR/build/packages-built.flag"
    else
        log_info "Packages already built"
    fi
    
    cd "$SCRIPT_DIR"
}

# Copy packages to ISO repository
setup_repository() {
    log_step "Setting up local repository in ISO..."
    
    REPO_DIR="$BUILD_DIR/repo/x86_64"
    mkdir -p "$REPO_DIR"
    
    # Copy built packages
    if [ -d "$WORKSPACE_DIR/build/packages" ]; then
        cp "$WORKSPACE_DIR/build/packages"/*.pkg.tar.zst "$REPO_DIR/" 2>/dev/null || true
        log_info "Copied $(ls -1 "$REPO_DIR"/*.pkg.tar.zst 2>/dev/null | wc -l) packages to repository"
    else
        log_warn "No built packages found, ISO will use online repositories only"
    fi
    
    # Create package database
    if [ "$(ls -A "$REPO_DIR" 2>/dev/null)" ]; then
        cd "$REPO_DIR"
        repo-add hyperos.db.tar.gz *.pkg.tar.zst 2>/dev/null || true
        cd "$SCRIPT_DIR"
        log_info "Repository database created"
    else
        log_warn "Repository is empty, skipping database creation"
    fi
}

# Customize AIROOTFS
customize_airootfs() {
    log_step "Customizing AIROOTFS..."
    
    AIROOTFS="$BUILD_DIR/airootfs"
    
    # Create necessary directories
    mkdir -p "$AIROOTFS/etc/systemd/system/getty@tty1.service.d"
    mkdir -p "$AIROOTFS/etc/skel/.config/hypr"
    mkdir -p "$AIROOTFS/etc/skel/.config/waybar"
    mkdir -p "$AIROOTFS/root/.automated_script.d"
    
    # Copy configurations
    if [ -d "$WORKSPACE_DIR/packages/hyperos-daemon/data" ]; then
        cp -r "$WORKSPACE_DIR/packages/hyperos-daemon/data"/* "$AIROOTFS/usr/share/" 2>/dev/null || true
    fi
    
    # Set permissions
    chmod +x "$AIROOTFS/root/.automated_script.sh" 2>/dev/null || true
    
    log_info "AIROOTFS customized"
}

# Build the ISO
build_iso() {
    log_step "Building ISO image..."
    
    cd "$BUILD_DIR"
    
    # Build with mkarchiso
    mkarchiso -v -w "/tmp/archiso-work" -o "$OUTPUT_DIR" "$BUILD_DIR" || {
        log_error "ISO build failed!"
        exit 1
    }
    
    cd "$WORKSPACE_DIR"
    
    # Rename ISO
    if [ -f "$OUTPUT_DIR/hyperos-x86_64.iso" ]; then
        mv "$OUTPUT_DIR/hyperos-x86_64.iso" "$OUTPUT_DIR/$ISO_NAME"
    fi
    
    log_info "ISO built successfully: $OUTPUT_DIR/$ISO_NAME"
}

# Generate checksums
generate_checksums() {
    log_step "Generating checksums..."
    
    cd "$OUTPUT_DIR"
    
    if [ -f "$ISO_NAME" ]; then
        sha256sum "$ISO_NAME" > "${ISO_NAME}.sha256"
        log_info "Checksum generated: ${ISO_NAME}.sha256"
    fi
    
    cd "$WORKSPACE_DIR"
}

# Show summary
show_summary() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   HyperOS ISO Build Complete!                         ║"
    echo "║                                                       ║"
    if [ -f "$OUTPUT_DIR/$ISO_NAME" ]; then
        ISO_SIZE=$(du -h "$OUTPUT_DIR/$ISO_NAME" | cut -f1)
        echo "║   ISO: $ISO_NAME"
        echo "║   Size: $ISO_SIZE"
        echo "║   Location: $OUTPUT_DIR/"
    else
        echo "║   ⚠️  ISO build failed or was skipped"
    fi
    echo "║                                                       ║"
    echo "║   Next steps:                                         ║"
    echo "║   1. Test in VM: ./scripts/test-iso.sh                ║"
    echo "║   2. Burn to USB: dd if=ISO of=/dev/sdX bs=4M         ║"
    echo "║   3. Boot and install!                                ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
}

# Main execution
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   HyperOS ISO Builder v$VERSION                        ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    check_dependencies
    prepare_build
    build_packages
    setup_repository
    customize_airootfs
    build_iso
    generate_checksums
    show_summary
}

# Run main function
main "$@"
