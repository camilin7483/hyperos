#!/usr/bin/env bash
#
# build-package.sh — Build a single HyperOS package
#
# Usage: ./scripts/build-package.sh packages/hyper-center
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <package-directory>"
    echo "Example: $0 packages/hyper-center"
    exit 1
fi

PACKAGE_DIR="$PROJECT_ROOT/$1"

if [ ! -f "$PACKAGE_DIR/PKGBUILD" ]; then
    echo "[build-package] Error: No PKGBUILD found in $PACKAGE_DIR"
    exit 1
fi

cd "$PACKAGE_DIR"

echo "[build-package] Building $1..."
makepkg -si

echo "[build-package] Package built successfully."
