# Packages

HyperOS system packages. Each directory contains a standalone Arch Linux package with its own PKGBUILD.

## Structure

Each package follows this layout:

```
hyper-<name>/
├── README.md       # Package description and usage
├── PKGBUILD        # Arch Linux package build file
├── src/            # Source code
└── assets/         # Package-specific resources
```

## Packages

| Package | Purpose |
|---------|---------|
| hyper-center | Central control panel |
| hyper-store | Application store |
| hyper-settings | System settings |
| hyper-installer | Installation configuration |
| hyper-update | System updater |
| hyper-drivers | Driver management |
| hyper-cli | Command-line tools |
| hyper-tools | System utilities |
| hyper-welcome | Welcome screen (implemented — PySide6) |
| hyper-backup | Backup manager |
| hyper-assistant | AI assistant |
| hyper-gaming | Gaming mode tools |
| hyper-kernel | Kernel management |

## Building

```bash
# Build all packages
./scripts/package.sh

# Build a specific package
cd packages/hyper-center
makepkg -si
```
