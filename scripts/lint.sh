#!/usr/bin/env bash
#
# lint.sh — Run validation checks on the HyperOS codebase
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

HAS_ERRORS=0

echo "[lint] Running lint checks..."

# ShellCheck for shell scripts
if command -v shellcheck &>/dev/null; then
    echo "[lint] Running shellcheck..."
    while IFS= read -r -d '' script; do
        shellcheck -x "$script" || HAS_ERRORS=1
    done < <(find . -name "*.sh" -type f -print0)
else
    echo "[lint] Warning: shellcheck not found. Skipping shell script validation."
fi

# Check for required files
echo "[lint] Checking required files..."
REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "ARCHITECTURE.md"
    "CONTRIBUTING.md"
    "ROADMAP.md"
    "BUILD.md"
    "archiso/profiledef.sh"
    "archiso/packages.x86_64"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PROJECT_ROOT/$file" ]; then
        echo "[lint] Missing required file: $file"
        HAS_ERRORS=1
    fi
done

# Check PKGBUILD files (basic syntax)
echo "[lint] Checking PKGBUILD files..."
while IFS= read -r -d '' pkgbuild; do
    if [ -f "$pkgbuild" ]; then
        bash -n "$pkgbuild" 2>/dev/null || {
            echo "[lint] Syntax error in: $pkgbuild"
            HAS_ERRORS=1
        }
    fi
done < <(find packages -name "PKGBUILD" -type f -print0 2>/dev/null || true)

if [ $HAS_ERRORS -eq 0 ]; then
    echo "[lint] All checks passed."
else
    echo "[lint] Some checks failed."
    exit 1
fi
