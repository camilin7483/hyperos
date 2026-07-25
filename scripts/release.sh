#!/usr/bin/env bash
#
# release.sh — Prepare a HyperOS release
#
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh v0.2.0
#
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 v0.2.0"
    exit 1
fi

VERSION="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "[release] Preparing release $VERSION..."

# Verify clean working tree
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "[release] Error: Working tree is not clean."
    exit 1
fi

# Run tests
echo "[release] Running tests..."
./scripts/test.sh

# Build ISO
echo "[release] Building ISO..."
./scripts/build-iso.sh

# TODO: Update CHANGELOG.md
# TODO: Update version references
# TODO: Create git tag

echo "[release] Release $VERSION prepared."
echo "[release] Next steps:"
echo "    1. Update CHANGELOG.md"
echo "    2. Create git tag: git tag -a $VERSION -m 'HyperOS $VERSION'"
echo "    3. Push: git push && git push --tags"
