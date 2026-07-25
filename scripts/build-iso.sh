#!/usr/bin/env bash
#
# build-iso.sh — Build the HyperOS ArchISO image
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

ISO_DIR="$PROJECT_ROOT/archiso"
OUT_DIR="$PROJECT_ROOT/out"

# Check for archiso
if ! command -v mkarchiso &>/dev/null; then
    echo "[build-iso] Error: mkarchiso not found. Install archiso:"
    echo "    sudo pacman -S archiso"
    exit 1
fi

# Verify profile
if [ ! -f "$ISO_DIR/profiledef.sh" ]; then
    echo "[build-iso] Error: ArchISO profile not found at $ISO_DIR"
    exit 1
fi

# Create output directory
mkdir -p "$OUT_DIR"

# Build ISO
echo "[build-iso] Building HyperOS ISO..."
mkarchiso -v -w "$OUT_DIR/work" -o "$OUT_DIR" "$ISO_DIR"

echo "[build-iso] ISO built successfully:"
ls -lh "$OUT_DIR"/*.iso 2>/dev/null || echo "    (no ISO found)"
