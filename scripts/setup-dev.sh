#!/usr/bin/env bash
#
# setup-dev.sh — Configure the HyperOS development environment
#
set -euo pipefail

echo "[setup-dev] Setting up HyperOS development environment..."

# Required packages
REQUIRED_PACKAGES=(
    "archiso"
    "base-devel"
    "git"
    "shellcheck"
)

echo "[setup-dev] Checking required packages..."
MISSING=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! pacman -Qi "$pkg" &>/dev/null; then
        MISSING+=("$pkg")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "[setup-dev] Missing packages: ${MISSING[*]}"
    echo "[setup-dev] Install with: sudo pacman -S ${MISSING[*]}"
fi

# Set up git hooks
echo "[setup-dev] Setting up git hooks..."
GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"

if [ -d "$GIT_ROOT/.git" ]; then
    HOOKS_DIR="$GIT_ROOT/.git/hooks"

    cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/usr/bin/env bash
echo "[pre-commit] Running linter..."
./scripts/lint.sh
EOF
    chmod +x "$HOOKS_DIR/pre-commit"

    echo "[setup-dev] Pre-commit hook installed."
fi

echo "[setup-dev] Development environment ready."
