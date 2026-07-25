# HyperOS

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?logo=arch-linux&logoColor=white)](https://archlinux.org)
[![Hyprland](https://img.shields.io/badge/Hyprland-00AEEF?logo=hyprland&logoColor=white)](https://hyprland.org)

**HyperOS** is an Arch Linux-based distribution focused on performance, minimalism, and a GUI-first user experience. Built on Hyprland (Wayland), it aims to provide a fast, elegant, and professional operating system where the terminal is optional for everyday tasks.

## Philosophy

- **Performance First** — Optimized defaults without sacrificing stability
- **GUI First** — Graphical tools for every administrative task
- **Terminal Optional** — The terminal is available, never required
- **Modular Design** — Independent components, loosely coupled
- **Clean Architecture** — Maintainable, scalable, future-proof

## Status

HyperOS is in early development. See [ROADMAP.md](ROADMAP.md) for planned milestones.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hyperos/hyperos.git
cd hyperos

# Install build dependencies
sudo pacman -S archiso

# Build the ISO
./scripts/build-iso.sh

# The output ISO will be in out/
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `apps/` | GUI application placeholders |
| `archiso/` | ISO build system |
| `assets/` | Static resources |
| `branding/` | Visual identity |
| `configs/` | Centralized configuration |
| `core/` | Shared libraries and infrastructure |
| `docs/` | Technical documentation |
| `installer/` | Graphical installer (future) |
| `kernel/` | Kernel configuration |
| `packages/` | HyperOS system packages |
| `repositories/` | Package repository infrastructure |
| `scripts/` | Build and maintenance scripts |
| `security/` | Security profiles |
| `system/` | System-level configuration |
| `testing/` | Test environment |

## License

HyperOS is free software licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
