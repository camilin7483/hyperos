#!/bin/bash
# shellcheck disable=SC2126,SC2162
# HyperOS Diagnostic Tool - Real hardware validation
# Usage: hyper-diagnose [--full|--desktop|--network|--audio|--gpu|--portal]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS_COUNT++))
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL_COUNT++))
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN_COUNT++))
}

log_info() {
    echo -e "  → $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        log_pass "$1 is installed"
        return 0
    else
        log_fail "$1 is NOT installed"
        return 1
    fi
}

# System Information
echo "=========================================="
echo "  HYPEROS DIAGNOSTIC TOOL v0.6.0"
echo "=========================================="
echo ""

MODE="${1:---quick}"

case "$MODE" in
    --full)
        echo "=== SYSTEM INFORMATION ==="
        if [ -f /etc/hyperos-release ]; then
            log_info "HyperOS Version: $(cat /etc/hyperos-release)"
        else
            log_warn "HyperOS release file not found"
        fi
        
        log_info "Kernel: $(uname -r)"
        log_info "Hostname: $(hostname)"
        log_info "Uptime: $(uptime -p 2>/dev/null || uptime)"
        echo ""

        echo "=== HARDWARE DETECTION ==="
        # CPU
        if [ -f /proc/cpuinfo ]; then
            CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)
            CPU_CORES=$(grep -c "^processor" /proc/cpuinfo)
            log_pass "CPU: $CPU_MODEL ($CPU_CORES cores)"
        else
            log_fail "Cannot detect CPU"
        fi

        # RAM
        if [ -f /proc/meminfo ]; then
            TOTAL_RAM=$(grep "MemTotal" /proc/meminfo | awk '{printf "%.2f GB", $2/1024/1024}')
            AVAIL_RAM=$(grep "MemAvailable" /proc/meminfo | awk '{printf "%.2f GB", $2/1024/1024}')
            log_pass "RAM: $TOTAL_RAM total, $AVAIL_RAM available"
        else
            log_fail "Cannot detect RAM"
        fi

        # GPU
        echo ""
        echo "=== GPU DETECTION ==="
        if command -v lspci &> /dev/null; then
            GPU_INFO=$(lspci -k | grep -A 2 -i vga)
            if [ -n "$GPU_INFO" ]; then
                log_pass "GPU detected:"
                echo "$GPU_INFO" | while read line; do
                    log_info "  $line"
                done
            else
                log_warn "No VGA controller found"
            fi
        else
            log_warn "lspci not available"
        fi

        # Check graphics drivers
        if lsmod | grep -q "nvidia"; then
            log_pass "NVIDIA proprietary driver loaded"
        elif lsmod | grep -q "nouveau"; then
            log_info "Nouveau (open NVIDIA) driver loaded"
        elif lsmod | grep -q "amdgpu"; then
            log_pass "AMDGPU driver loaded"
        elif lsmod | grep -q "i915"; then
            log_pass "Intel i915 driver loaded"
        else
            log_warn "No known GPU driver detected"
        fi
        echo ""

        echo "=== DESKTOP ENVIRONMENT ==="
        # Wayland session
        if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
            log_pass "Running on Wayland"
        else
            log_warn "Not running on Wayland (current: ${XDG_SESSION_TYPE:-unknown})"
        fi

        # Hyprland
        if command -v hyprctl &> /dev/null; then
            if hyprctl version &> /dev/null; then
                log_pass "Hyprland compositor running"
                HYPRLAND_VER=$(hyprctl version | grep "Version:" | head -1)
                log_info "  $HYPRLAND_VER"
            else
                log_warn "Hyprland command available but not running"
            fi
        else
            log_fail "Hyprland not installed"
        fi

        # XDG Variables
        echo ""
        log_info "XDG Variables:"
        log_info "  XDG_CURRENT_DESKTOP=${XDG_CURRENT_DESKTOP:-NOT SET}"
        log_info "  XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-NOT SET}"
        log_info "  XDG_SESSION_DESKTOP=${XDG_SESSION_DESKTOP:-NOT SET}"
        
        if [ "$XDG_CURRENT_DESKTOP" = "Hyprland" ]; then
            log_pass "XDG_CURRENT_DESKTOP correctly set"
        else
            log_warn "XDG_CURRENT_DESKTOP may be incorrect for Hyprland"
        fi
        echo ""

        echo "=== XDG PORTALS ==="
        # Portal processes
        if pgrep -x "xdg-desktop-portal" > /dev/null; then
            log_pass "xdg-desktop-portal is running"
        else
            log_fail "xdg-desktop-portal is NOT running"
        fi

        if pgrep -x "xdg-desktop-portal-gtk" > /dev/null; then
            log_pass "xdg-desktop-portal-gtk is running"
        else
            log_warn "xdg-desktop-portal-gtk is NOT running (file pickers may fail)"
        fi

        if pgrep -x "xdg-desktop-portal-hyprland" > /dev/null; then
            log_pass "xdg-desktop-portal-hyprland is running"
        else
            log_warn "xdg-desktop-portal-hyprland is NOT running (screenshots may fail)"
        fi

        # D-Bus check
        if command -v busctl &> /dev/null; then
            PORTAL_COUNT=$(busctl --user list | grep -c "org.freedesktop.portal" || echo "0")
            if [ "$PORTAL_COUNT" -gt 0 ]; then
                log_pass "$PORTAL_COUNT portal services available on D-Bus"
            else
                log_fail "No portal services found on D-Bus"
            fi
        else
            log_warn "busctl not available, skipping D-Bus check"
        fi
        echo ""

        echo "=== NETWORK ==="
        if command -v nmcli &> /dev/null; then
            if nmcli -t -f ACTIVE dev | grep -q "connected"; then
                log_pass "NetworkManager has active connections"
                nmcli -t -f DEVICE,TYPE,STATE dev | grep "connected" | while read line; do
                    log_info "  $line"
                done
            else
                log_warn "No active network connections"
            fi
            
            if nmcli -t -f ALL dev wifi list | head -1 | grep -q "."; then
                log_pass "WiFi scanning functional"
            else
                log_warn "WiFi scanning may not be functional"
            fi
        else
            log_fail "NetworkManager CLI (nmcli) not installed"
        fi

        if command -v ping &> /dev/null; then
            if ping -c 1 -W 2 8.8.8.8 &> /dev/null; then
                log_pass "Internet connectivity OK"
            else
                log_warn "No internet connectivity"
            fi
        fi
        echo ""

        echo "=== AUDIO ==="
        if command -v pactl &> /dev/null; then
            if pactl info | grep -q "PipeWire"; then
                log_pass "PipeWire audio server running"
            elif pactl info | grep -q "PulseAudio"; then
                log_info "PulseAudio server running"
            else
                log_warn "Unknown audio server"
            fi
            
            SINK_COUNT=$(pactl list short sinks | wc -l)
            SOURCE_COUNT=$(pactl list short sources | wc -l)
            log_info "  $SINK_COUNT output devices, $SOURCE_COUNT input devices"
        elif command -v pw-cli &> /dev/null; then
            log_pass "PipeWire installed (pw-cli available)"
        else
            log_fail "No audio control tools found"
        fi
        echo ""

        echo "=== BLUETOOTH ==="
        if systemctl is-active --quiet bluetooth; then
            log_pass "Bluetooth service is active"
            if command -v bluetoothctl &> /dev/null; then
                log_info "bluetoothctl available"
            fi
        else
            log_warn "Bluetooth service is not active"
        fi
        echo ""

        echo "=== SYSTEM SERVICES ==="
        FAILED_UNITS=$(systemctl --failed --no-legend | wc -l)
        if [ "$FAILED_UNITS" -eq 0 ]; then
            log_pass "No failed systemd units"
        else
            log_warn "$FAILED_UNITS failed systemd units:"
            systemctl --failed --no-legend | while read unit; do
                log_info "  $unit"
            done
        fi
        echo ""

        echo "=== BOOT PERFORMANCE ==="
        if command -v systemd-analyze &> /dev/null; then
            BOOT_TIME=$(systemd-analyze 2>&1 | grep "Startup finished in" | head -1)
            if [ -n "$BOOT_TIME" ]; then
                log_info "$BOOT_TIME"
            fi
            
            log_info "Top 5 slowest services:"
            systemd-analyze blame 2>/dev/null | head -5 | while read line; do
                log_info "  $line"
            done
        fi
        echo ""

        echo "=== STORAGE ==="
        if command -v df &> /dev/null; then
            log_info "Disk usage:"
            df -h / /home /boot 2>/dev/null | tail -n +2 | while read line; do
                log_info "  $line"
            done
        fi
        echo ""

        ;;
    
    --desktop)
        echo "=== DESKTOP VALIDATION ==="
        # Focused desktop checks
        if [ "$XDG_SESSION_TYPE" = "wayland" ] && command -v hyprctl &> /dev/null && hyprctl version &> /dev/null; then
            log_pass "Hyprland Wayland session active"
        else
            log_fail "Hyprland Wayland session NOT active"
        fi
        
        # Test screenshot capability
        if command -v grim &> /dev/null; then
            log_pass "grim (screenshot tool) available"
        else
            log_warn "grim not installed"
        fi
        
        if command -v slurp &> /dev/null; then
            log_pass "slurp (region selector) available"
        else
            log_warn "slurp not installed"
        fi
        ;;
    
    --network)
        echo "=== NETWORK VALIDATION ==="
        check_command "nmcli"
        check_command "ping"
        
        if nmcli -t -f ACTIVE dev | grep -q "connected"; then
            log_pass "Active network connection detected"
        else
            log_fail "No active network connection"
        fi
        
        if ping -c 1 -W 2 8.8.8.8 &> /dev/null; then
            log_pass "External connectivity (8.8.8.8) OK"
        else
            log_fail "Cannot reach 8.8.8.8"
        fi
        ;;
    
    --audio)
        echo "=== AUDIO VALIDATION ==="
        if command -v pactl &> /dev/null || command -v pw-cli &> /dev/null; then
            log_pass "Audio control tools available"
            
            if pactl info 2>/dev/null | grep -q "Server Name"; then
                log_pass "Audio server responding"
            else
                log_warn "Audio server not responding"
            fi
        else
            log_fail "No audio control tools found"
        fi
        ;;
    
    --gpu)
        echo "=== GPU VALIDATION ==="
        if command -v lspci &> /dev/null; then
            GPU_COUNT=$(lspci | grep -i vga | wc -l)
            if [ "$GPU_COUNT" -gt 0 ]; then
                log_pass "$GPU_COUNT GPU(s) detected"
                lspci | grep -i vga | while read line; do
                    log_info "  $line"
                done
            else
                log_warn "No GPU detected via lspci"
            fi
        fi
        
        if lsmod | grep -qE "(nvidia|nouveau|amdgpu|i915|radeon)"; then
            log_pass "GPU driver module loaded"
        else
            log_warn "No known GPU driver module loaded"
        fi
        ;;
    
    *)
        echo "Usage: $0 [--full|--desktop|--network|--audio|--gpu]"
        echo ""
        echo "Options:"
        echo "  --full     Complete system diagnostic (recommended)"
        echo "  --desktop  Desktop environment validation only"
        echo "  --network  Network connectivity validation only"
        echo "  --audio    Audio subsystem validation only"
        echo "  --gpu      GPU detection validation only"
        exit 1
        ;;
esac

echo "=========================================="
echo "  SUMMARY"
echo "=========================================="
echo -e "  ${GREEN}Passed:${NC}   $PASS_COUNT"
echo -e "  ${RED}Failed:${NC}   $FAIL_COUNT"
echo -e "  ${YELLOW}Warnings:${NC} $WARN_COUNT"
echo ""

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo -e "${GREEN}All critical checks passed!${NC}"
    exit 0
elif [ "$FAIL_COUNT" -le 2 ]; then
    echo -e "${YELLOW}Some non-critical checks failed. System should be functional.${NC}"
    exit 0
else
    echo -e "${RED}Multiple critical checks failed. Review issues above.${NC}"
    exit 1
fi
