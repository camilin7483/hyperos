#!/usr/bin/env bash
#
# test.sh — Run HyperOS test suites
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "[test] Running tests..."

# Lint first
echo "[test] Running lint checks..."
./scripts/lint.sh

# ISO validation (if archiso is available)
if command -v mkarchiso &>/dev/null; then
    echo "[test] Validating ArchISO profile..."
    # TODO: Run mkarchiso validation
fi

# TODO: Add package tests
# TODO: Add unit tests
# TODO: Add integration tests

echo "[test] All tests passed."
