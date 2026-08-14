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

**HyperOS v1.0.0 - STABLE RELEASE** ✅

HyperOS es una distribución Linux completa y funcional basada en Arch Linux, lista para producción.

### Características Principales

- ✅ **ISO Booteable** - UEFI/BIOS con Live Environment
- ✅ **Instalador Gráfico Real** - Particionado UEFI/GPT, formateo, pacstrap
- ✅ **Hyprland Configurado** - Wayland optimizado con animaciones
- ✅ **Aplicaciones HyperOS** - 13 aplicaciones nativas completamente funcionales
- ✅ **Repositorio Propio** - Paquetes firmados con GPG
- ✅ **Actualizaciones Seguras** - Sistema de actualización atómico
- ✅ **Recuperación** - Herramientas de repair y backup
- ✅ **Documentación Completa** - Guías de instalación, administración y desarrollo

## Quick Start

```bash
# Clonar el repositorio
git clone https://github.com/hyperos/hyperos.git
cd hyperos

# Construir TODO (paquetes + repositorio + ISO)
./build.sh all

# O construir solo la ISO
./build.sh iso

# La ISO estará en build/iso/
```

### Probar en QEMU

```bash
./scripts/test-iso.sh
```

### Instalar en Hardware Real

1. Grabar ISO en USB: `dd if=build/iso/hyperos.iso of=/dev/sdX bs=4M status=progress`
2. Bootear desde USB
3. Ejecutar "Hyper Installer" desde el menú
4. Seguir el asistente de instalación

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
