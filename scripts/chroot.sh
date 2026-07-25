#!/usr/bin/env bash
#
# chroot.sh — Enter the ArchISO build chroot for debugging
#
# Usage: ./scripts/chroot.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

CHROOT_DIR="$PROJECT_ROOT/out/work/x86_64/airootfs"

if [ ! -d "$CHROOT_DIR" ]; then
    echo "[chroot] Error: Chroot directory not found."
    echo "[chroot] Build the ISO first: ./scripts/build-iso.sh"
    echo "[chroot] Expected: $CHROOT_DIR"
    exit 1
fi

echo "[chroot] Entering chroot at $CHROOT_DIR"
echo "[chroot] Type 'exit' to leave."

sudo arch-chroot "$CHROOT_DIR"
