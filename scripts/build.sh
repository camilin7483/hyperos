#!/usr/bin/env bash
#
# build.sh — Orchestrate the full HyperOS build process
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "[build] Starting HyperOS build..."

./scripts/lint.sh
./scripts/build-iso.sh
./scripts/package.sh

echo "[build] Build complete."
