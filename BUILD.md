# Building HyperOS

This guide covers everything from setting up your build environment to producing a bootable ISO and installing HyperOS packages.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Build](#quick-build)
3. [Building the ISO](#building-the-iso)
4. [Building Packages](#building-packages)
5. [Development Workflow](#development-workflow)
6. [Testing in a Virtual Machine](#testing-in-a-virtual-machine)
7. [Advanced ISO Configuration](#advanced-iso-configuration)
8. [Troubleshooting](#troubleshooting)
9. [Continuous Integration](#continuous-integration)

---

## Prerequisites

### Required System Packages

HyperOS builds require an **Arch Linux** system (or an environment with `archiso`). Install the following:

```bash
sudo pacman -S --needed \
    archiso \
    base-devel \
    git \
    python \
    python-pyside6 \
    python-build \
    python-installer \
    python-wheel
```

### Recommended

```bash
# Shell script linting
sudo pacman -S shellcheck

# QEMU for VM testing
sudo pacman -S qemu-desktop qemu-img

# Python testing
pip install --user pytest
```

### Verify Installation

```bash
which mkarchiso          # Should point to /usr/bin/mkarchiso
python --version         # Should be Python 3.11+
```

---

## Quick Build

```bash
# Clone the repository
git clone https://github.com/camilin7483/hyperos.git
cd hyperos

# Build the ISO (this builds all packages and generates the ISO)
./scripts/build-iso.sh

# The output ISO will be placed in out/
ls -lh out/hyperos-*.iso
```

---

## Building the ISO

### Step 1: Prepare the Environment

```bash
./scripts/setup-dev.sh
```

This script:
- Checks for required packages
- Installs pre-commit hooks
- Verifies the build environment

### Step 2: Build Packages

Build all HyperOS packages before generating the ISO:

```bash
./scripts/package.sh
```

Or build individual packages:

```bash
./scripts/build-package.sh packages/hyper-center
./scripts/build-package.sh packages/hyper-welcome
```

### Step 3: Generate the ISO

```bash
./scripts/build-iso.sh
```

The build process:

1. **Validates** the ArchISO profile (`archiso/profiledef.sh`)
2. **Resolves** all package dependencies
3. **Downloads** packages into a clean chroot
4. **Applies** the `airootfs/` overlay (custom configs, scripts, assets)
5. **Configures** bootloaders (GRUB for BIOS, systemd-boot for UEFI, syslinux/isolinux for legacy)
6. **Generates** the squashfs filesystem (compressed with xz)
7. **Produces** the final bootable ISO image

### Step 4: Output

The ISO is written to:

```
out/hyperos-YYYY.MM.DD-x86_64.iso
```

---

## Building Packages

### Individual Package

Each HyperOS package is a standard Arch Linux PKGBUILD:

```bash
# Navigate to the package
cd packages/hyper-center

# Build the package
makepkg -s

# Build and install
makepkg -si
```

### Using the Build Script

```bash
# Build a specific package
./scripts/build-package.sh packages/hyper-center

# Build all packages
./scripts/package.sh
```

### Package Structure

```
packages/hyper-<name>/
├── PKGBUILD                    # Arch Linux package build file
├── README.md                   # Package documentation
├── src/
│   ├── pyproject.toml          # Python package metadata
│   └── hyper_<name>/           # Python source code
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py              # Application entry point
│       ├── domain/             # Domain layer (models, enums)
│       ├── services/           # Service layer (business logic)
│       ├── widgets/             # Widget layer (reusable UI)
│       ├── ui/                 # UI layer (windows, pages)
│       └── tests/              # Unit tests
├── data/
│   ├── hyper-<name>.desktop    # Desktop entry file
│   └── hyper<name>.service     # Systemd service (optional)
└── assets/
    └── icons/
        └── hyper-<name>.svg    # Application icon
```

### Adding a New Package

1. Create the package directory structure
2. Write the PKGBUILD following the template at `packages/PKGBUILD.common`
3. Implement the application using Clean Architecture
4. Add unit tests in `tests/`
5. Create the desktop entry in `data/`
6. Add the SVG icon in `assets/icons/`
7. Add the package to `archiso/packages.x86_64`

---

## Development Workflow

### Setup

```bash
# Set up development environment
./scripts/setup-dev.sh

# Activate the project (sets PYTHONPATH, etc.)
# No activation needed — use PYTHONPATH when testing
```

### Running Applications Directly

```bash
# Run Hyper Center from source
cd packages/hyper-center/src
PYTHONPATH=/path/to/core:$PYTHONPATH python -m hyper_center

# Run Hyper Welcome from source
cd packages/hyper-welcome/src
PYTHONPATH=/path/to/core:$PYTHONPATH python -m hyper_welcome
```

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run tests for a specific package
cd packages/hyper-center/src
python -m pytest hyper_center/tests/ -v

# Run all tests with coverage
python -m pytest --cov=hyper_center hyper_center/tests/
```

### Code Quality

```bash
# Run linting (ShellCheck, PKGBUILD syntax, required files)
./scripts/lint.sh

# Manual checks
python -m py_compile packages/hyper-center/src/hyper_center/app.py
bash -n packages/hyper-center/PKGBUILD
```

### Cleaning

```bash
# Remove build artifacts
./scripts/clean.sh
```

This removes:
- `out/` (ISO output directory)
- `work/` (ISO build working directory)
- `__pycache__/` and `*.pyc` (Python cache)
- `*.egg-info/` (Python package metadata)
- `dist/` and `build/` (Python build artifacts)
- `*.pkg.tar.*` (Arch Linux package files)

---

## Testing in a Virtual Machine

### Using QEMU

```bash
# Basic test
qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -cdrom out/hyperos-*.iso

# With UEFI
qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -bios /usr/share/edk2-ovmf/x64/OVMF.fd \
    -cdrom out/hyperos-*.iso

# With disk for installation testing
qemu-img create -f qcow2 hyperos-test.qcow2 32G
qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -cdrom out/hyperos-*.iso \
    -drive file=hyperos-test.qcow2,format=qcow2
```

### Using VirtualBox

1. Create a new VM with at least 4 GB RAM and 32 GB disk
   - Type: Linux
   - Version: Arch Linux (64-bit)
   - Enable EFI if supported
2. Attach the ISO as a optical drive
3. Boot and proceed with installation

### Validation Checklist

After booting the ISO, verify:

- [ ] Desktop (Hyprland) starts automatically
- [ ] Plymouth boot splash shows HyperOS branding
- [ ] SDDM login screen shows HyperOS theme
- [ ] Hyper Welcome appears on first boot
- [ ] Hyper Center launches and shows correct system info
- [ ] Hyper Settings opens all 11 sections
- [ ] Hyper Store can search packages
- [ ] Hyper Update can check for updates
- [ ] Terminal (kitty) opens
- [ ] NetworkManager connects to networks
- [ ] Audio (PipeWire) works
- [ ] The installer can partition and install

---

## Advanced ISO Configuration

### Customizing Packages

Edit `archiso/packages.x86_64` to add or remove packages from the live environment:

```
# Live add your package
my-custom-package
```

### Customizing the Live Environment

Edit files in `archiso/airootfs/`:
- `/etc/hostname` — Live system hostname
- `/etc/locale.conf` — Default locale
- `/etc/locale.gen` — Enabled locales
- `/usr/local/bin/hyperos-before` — Pre-boot script
- `/usr/local/bin/hyperos-welcome` — Welcome script

### Customizing Bootloaders

- **GRUB**: `archiso/grub/grub.cfg`
- **systemd-boot**: `archiso/efiboot/`
- **syslinux**: `archiso/bootloader/syslinux.cfg`
- **ISOLINUX**: `archiso/isolinux/isolinux.cfg`

### Customizing Branding

See `branding/README.md` for details on:
- Logo (SVG, required sizes)
- Plymouth theme
- GRUB theme
- SDDM theme
- Wallpapers (PNG, recommended resolution)

---

## Troubleshooting

### `mkarchiso: command not found`

```bash
sudo pacman -S archiso
```

### `python-pyside6: package not found`

PySide6 is available in the Arch Linux `extra` repository:

```bash
sudo pacman -S pyside6
```

### ISO build fails with disk space

ISO builds require significant temporary space (up to 10 GB). Ensure your `work/` directory has enough space. You can symlink it to a larger partition:

```bash
ln -s /path/to/large/disk/work work
```

### Package build fails: missing dependencies

Ensure `python-build`, `python-installer`, and `python-wheel` are installed:

```bash
sudo pacman -S python-build python-installer python-wheel
```

### `import hyperos_core` fails

Ensure the core library path is in `PYTHONPATH`:

```bash
export PYTHONPATH=/path/to/hyperos/core:$PYTHONPATH
```

### QEMU does not boot

- Ensure KVM is enabled (`-enable-kvm`)
- For UEFI, ensure `edk2-ovmf` is installed and the OMVF path is correct
- For BIOS, ensure the ISO was built with BIOS support (syslinux)

---

## Continuous Integration

HyperOS uses GitHub Actions for CI. The following workflows are available:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `lint.yml` | Push, PR | ShellCheck, PKGBUILD validation |
| `test.yml` | Push, PR | Python test suite |
| `build-iso.yml` | Tag | Build release ISO |
| `release.yml` | Tag | Create GitHub release |
| `sync-mirrors.yml` | Weekly | Sync package mirrors |

---

## Release Process

```bash
# Ensure clean state
git status

# Run full test suite
./scripts/test.sh

# Build the ISO
./scripts/build-iso.sh

# Run the release script
./scripts/release.sh

# Tag and push
git tag -a v0.4.0 -m "HyperOS v0.4.0 — Core Applications Complete"
git push origin v0.4.0
```

The release script will:
1. Verify clean git tree
2. Run all tests
3. Build the ISO
4. Generate checksums
5. Print release instructions
