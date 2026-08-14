# HyperOS

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?logo=arch-linux&logoColor=white)](https://archlinux.org)
[![Hyprland](https://img.shields.io/badge/Hyprland-00AEEF?logo=hyprland&logoColor=white)](https://hyprland.org)
[![Build ISO](https://img.shields.io/github/actions/workflow/status/camilin7483/hyperos/build-iso.yml?label=Build%20ISO)](https://github.com/camilin7483/hyperos/actions/workflows/build-iso.yml)
[![Release](https://img.shields.io/badge/Release-v1.0.0-00AEEF?logo=github)](https://github.com/camilin7483/hyperos/releases)

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

### Descargar la última release (recomendado)

La ISO estable se genera automáticamente en CI y se publica en [Releases](https://github.com/camilin7483/hyperos/releases):

```bash
curl -LO https://github.com/camilin7483/hyperos/releases/download/v1.0.0/hyperos-2026.08.14-x86_64.iso
```

### Construir desde el repositorio

```bash
git clone https://github.com/camilin7483/hyperos.git
cd hyperos

# 1. Construir paquetes + repositorio local
./build.sh all

# 2. Añadir el repo local al pacman.conf del perfil (como hace CI):
#    [hyperos-local]
#    SigLevel = Never
#    Server = file:///abs/path/hyperos/build/repository/x86_64

# 3. Construir la ISO
sudo pacman -S archiso   # si no está instalado
./scripts/build-iso.sh

# La ISO estará en out/ como hyperos-<fecha>-x86_64.iso
```

La ISO también se genera automáticamente en [GitHub Actions](https://github.com/camilin7483/hyperos/actions/workflows/build-iso.yml) (artefacto `hyperos-iso`) y en cada release.

### Probar en QEMU

```bash
./scripts/test-iso.sh
```

### Instalar en Hardware Real

1. Grabar ISO en USB: `dd if=out/hyperos-<fecha>-x86_64.iso of=/dev/sdX bs=4M status=progress`
2. Bootear desde USB
3. Ejecutar "Hyper Installer" desde el menú
4. Seguir el asistente de instalación (particionado UEFI/GPT + pacstrap)

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `apps/` | Legacy GUI application entries |
| `archiso/` | ArchISO profile used by CI and `scripts/build-iso.sh` |
| `assets/` | Static resources |
| `branding/` | Visual identity |
| `configs/` | Centralized configuration |
| `core/` | Shared libraries and infrastructure |
| `docs/` | Technical documentation |
| `installer/` | Installer support files |
| `kernel/` | Kernel configuration |
| `packages/` | HyperOS system packages (built by CI) |
| `repositories/` | Package repository infrastructure |
| `scripts/` | Build and maintenance scripts |
| `security/` | Security profiles |
| `system/` | System-level configuration |
| `testing/` | Test environment |

## License

HyperOS is free software licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
