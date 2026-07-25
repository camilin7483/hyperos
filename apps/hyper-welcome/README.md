# Hyper Welcome

Post-installation welcome screen for HyperOS.

## Status

**Implemented (v0.3).** Real PySide6 application.

## Responsibility

Hyper Welcome is the first application launched after a fresh installation. It shows system information, provides quick access to resources, and introduces the HyperOS experience. It runs once on first boot and never appears again.

## Features

- Welcome screen with HyperOS branding
- System information panel (CPU, RAM, GPU, Storage, Kernel, Desktop)
- Internet connectivity status
- Quick action buttons
- First-boot state management
- systemd user service integration

## Implementation

Located in `packages/hyper-welcome/src/hyper_welcome/`.

See the [package README](../../packages/hyper-welcome/README.md) for details.
