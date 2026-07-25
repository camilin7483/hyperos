#!/usr/bin/env bash
#
# clean.sh — Remove build artifacts
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "[clean] Removing build artifacts..."

# ISO build
rm -rf out/
rm -rf work/

# Package build artifacts (only build-generated dirs under package src/)
find packages -type d -name "pkg" -exec rm -rf {} + 2>/dev/null || true
find packages -type d -name "src" -path "*/src/src" -exec rm -rf {} + 2>/dev/null || true
find packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find packages -type f -name "*.pkg.tar.*" -delete 2>/dev/null || true
find packages -type f -name "*.log" -delete 2>/dev/null || true

# Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true

echo "[clean] Done."
