#!/usr/bin/env bash
#
# package.sh — Build all HyperOS packages
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

PACKAGES_DIR="$PROJECT_ROOT/packages"

echo "[package] Building HyperOS packages..."

BUILD_FAILED=0

for pkg_dir in "$PACKAGES_DIR"/hyper-*/; do
    if [ -f "$pkg_dir/PKGBUILD" ]; then
        pkg_name="$(basename "$pkg_dir")"
        echo "[package] Building $pkg_name..."

        cd "$pkg_dir"

        if makepkg_output=$(makepkg -s 2>&1); then
            echo "[package] $pkg_name built successfully."
        else
            echo "[package] ERROR: $pkg_name build failed."
            echo "$makepkg_output" | tail -5
            BUILD_FAILED=1
        fi

        cd "$PROJECT_ROOT"
    fi
done

if [ $BUILD_FAILED -eq 0 ]; then
    echo "[package] All packages built successfully."
else
    echo "[package] Some packages failed to build."
    exit 1
fi
