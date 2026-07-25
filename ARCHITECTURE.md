# HyperOS Architecture

## Overview

HyperOS follows a layered architecture with clear separation of concerns. Each layer depends only on the layers below it, and components within each layer communicate through well-defined interfaces.

## Layer Diagram

```
+--------------------------------------------------+
|                  GUI Applications                  |
|  Center | Store | Settings | Drivers | Welcome   |
+--------------------------------------------------+
|                   Core Libraries                   |
|  IPC  |  DBus  |  Schemas  |  Shared  |  API     |
+--------------------------------------------------+
|              Configuration System                  |
|  System  |  Desktop  |  Security  |  Performance  |
+--------------------------------------------------+
|               System Services                      |
|  systemd  |  udev  |  polkit  |  pam  |  sysctl   |
+--------------------------------------------------+
|                 Arch Linux Base                    |
|  linux-zen  |  pacman  |  glibc  |  systemd       |
+--------------------------------------------------+
```

## Design Principles

### Clean Architecture

- **Independence** — Each layer is independent of external frameworks
- **Testability** — Business logic can be tested without UI or infrastructure
- **Separation of Concerns** — Each component has a single responsibility

### Modular Design

- Applications communicate through shared interfaces
- No direct coupling between applications
- New features can be added as independent modules

### Configuration

- All system configuration is centralized under `configs/`
- Applications read from a unified configuration API
- Sensible defaults are provided for every setting

## Key Design Decisions

### Desktop Agnosticism

While Hyprland is the default desktop, the architecture supports adding KDE Plasma, XFCE, or GNOME editions without restructuring. Desktop-specific configurations are isolated in `configs/desktop/` and `configs/hyprland/`.

### Shared Core

All HyperOS applications use `core/libraries/` for common functionality. This prevents code duplication and ensures consistent behavior across the system.

### Future Expansion

The architecture anticipates:

- Hyper Store (package management GUI)
- Graphical installer
- Driver manager
- Kernel manager (linux-hyperos)
- AI assistant integration
- Backup and restore points
- Gaming mode
- Performance profiles

No future feature requires restructuring the repository.

## Communication

Applications communicate through:

- **DBus** — System-wide messaging
- **IPC** — Inter-process communication
- **Shared Schemas** — Data contracts between components
- **Core API** — Unified application interface
