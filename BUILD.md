# Building HyperOS

## Prerequisites

### Required Packages

```bash
sudo pacman -S archiso base-devel git
```

### Optional

```bash
# For linting
sudo pacman -S shellcheck

# For testing in a VM
sudo pacman -S qemu-desktop
```

## Build the ISO

```bash
# Clone the repository
git clone https://github.com/hyperos/hyperos.git
cd hyperos

# Build the ISO
./scripts/build-iso.sh

# The output ISO will be placed in out/
```

## Build a Package

```bash
# Build a specific HyperOS package
./scripts/build-package.sh packages/hyper-center

# Or manually
cd packages/hyper-center
makepkg -si
```

## Development Workflow

```bash
# Set up development environment
./scripts/setup-dev.sh

# Run linting
./scripts/lint.sh

# Run tests
./scripts/test.sh

# Clean build artifacts
./scripts/clean.sh
```

## Test the ISO in QEMU

```bash
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom out/hyperos-*.iso
```

## Directory Overview

| Path | Description |
|------|-------------|
| `archiso/` | ArchISO profile for ISO generation |
| `packages/` | Individual HyperOS packages |
| `scripts/` | Build and maintenance scripts |
| `configs/` | System configuration profiles |

## ISO Build Details

The ISO build process:

1. Validates the ArchISO profile
2. Installs required packages in a clean chroot
3. Applies system overlays from `archiso/airootfs/`
4. Configures bootloaders (GRUB, syslinux, systemd-boot)
5. Generates the bootable ISO image

## Troubleshooting

### mkarchiso not found

Ensure `archiso` is installed:
```bash
sudo pacman -S archiso
```

### Build fails with network issues

Check your internet connection and DNS configuration. The build process downloads packages from Arch Linux mirrors.

### Out of disk space

ISO builds require significant temporary space. Use a filesystem with at least 10GB free.
