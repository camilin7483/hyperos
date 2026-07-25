# HyperOS Architecture

This document describes the architecture, design principles, and internal structure of HyperOS.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Application Architecture (Clean Architecture)](#application-architecture-clean-architecture)
3. [Design Principles](#design-principles)
4. [Key Design Decisions](#key-design-decisions)
5. [Shared Core Library (hyperos-core)](#shared-core-library-hyperos-core)
6. [Package Layout](#package-layout)
7. [Data Flow](#data-flow)
8. [Communication Between Components](#communication-between-components)
9. [Configuration System](#configuration-system)
10. [Boot Process](#boot-process)
11. [Performance Architecture](#performance-architecture)
12. [Security Architecture](#security-architecture)

---

## System Architecture

HyperOS follows a 5-layer architecture with strict dependency direction: each layer depends only on the layers below it.

```
┌─────────────────────────────────────────────────────────────┐
│                   GUI Applications (PySide6 / Qt6)          │
│  Welcome  ·  Center  ·  Settings  ·  Store  ·  Update      │
│  Drivers  ·  Backup  ·  Assistant  ·  Installer            │
├─────────────────────────────────────────────────────────────┤
│               Core Library (hyperos-core)                   │
│  Domain   ·  Services   ·  Widgets   ·  UI Theme/Stylesheet │
├─────────────────────────────────────────────────────────────┤
│               Configuration System                          │
│  System   ·  Desktop (Hyprland)   ·  Security               │
│  Performance Profiles   ·  Network                          │
├─────────────────────────────────────────────────────────────┤
│               System Services                               │
│  systemd  ·  udev  ·  NetworkManager  ·  polkit             │
│  PipeWire  ·  SDDM  ·  dbus-broker  ·  pam                 │
├─────────────────────────────────────────────────────────────┤
│               Arch Linux Base System                        │
│  linux-zen  ·  glibc  ·  systemd  ·  pacman                 │
│  Wayland  ·  Vulkan  ·  mesa                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Technology |
|-------|---------------|------------|
| **GUI Applications** | User-facing system administration tools | PySide6 (Qt6), QML |
| **Core Library** | Shared domain models, services, UI components | Pure Python + PySide6 |
| **Configuration** | Centralized system configuration, profiles, defaults | TOML/YAML files, dconf |
| **System Services** | Background daemons, system management | systemd, udev, polkit |
| **Base System** | Operating system foundation | Arch Linux packages |

### Desktop-Agnostic Layer

While **Hyprland** is the default desktop environment, the architecture isolates desktop-specific configuration so other desktops (KDE Plasma, XFCE, GNOME) can be supported as editions without restructuring:

```
configs/
├── desktop/          # Desktop-agnostic defaults
├── hyprland/         # Hyprland-specific config
└── <desktop>/        # Future desktop editions
```

---

## Application Architecture (Clean Architecture)

Every HyperOS GUI application follows **Clean Architecture** with four strictly layered modules:

```
hyper_<app>/
├── domain/
│   ├── __init__.py
│   └── models.py            # Pure data classes (no PySide6, no I/O)
├── services/
│   ├── __init__.py
│   └── <name>_service.py     # Business logic, system calls
├── widgets/
│   ├── __init__.py
│   └── <widget>.py           # Reusable UI components
├── ui/
│   ├── __init__.py
│   ├── main_window.py        # Application window
│   └── <page>.py             # Page/section components
├── tests/
│   ├── __init__.py
│   └── test_<name>.py        # Unit and integration tests
├── app.py                    # QApplication bootstrap
├── __init__.py
└── __main__.py
```

### Layer Rules

| Layer | Dependencies | Can Import | Purpose |
|-------|-------------|------------|---------|
| **Domain** | None (pure Python) | `dataclasses`, `enum` | Data models, enums, type definitions |
| **Services** | `domain` | Subprocess, threading, logging | Business logic, system interaction |
| **Widgets** | `domain` | PySide6 (QtCore, QtGui) | Reusable UI components |
| **UI** | `domain`, `services`, `widgets` | PySide6 (QtWidgets) | Application windows, pages |

### Dependency Direction

```
UI → Widgets → Services → Domain
```

Dependencies flow **inward only**. Domain has zero dependencies. This ensures:
- **Testability** — Business logic (services) can be tested without UI
- **Swapability** — UI framework can be replaced without touching domain or services
- **Isolation** — Changes in outer layers don't affect inner layers

### Application Boilerplate Pattern

```python
# app.py
import sys
import logging
from PySide6.QtWidgets import QApplication
from hyperos_core.widgets.theme import apply_theme
from .ui.main_window import MainWindow

logger = logging.getLogger(__name__)

def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## Design Principles

### SOLID

- **Single Responsibility** — Each class has exactly one reason to change
- **Open/Closed** — Extend via inheritance, never modify existing working code
- **Liskov Substitution** — Derived classes must be substitutable for their base types
- **Interface Segregation** — Small, focused interfaces rather than large monoliths
- **Dependency Inversion** — Depend on abstractions (domain models), not on concretions (UI widgets)

### DRY (Don't Repeat Yourself)

Shared logic lives in `hyperos-core`. No two applications should duplicate:
- System information collection
- Pacman wrapper code
- Network status queries
- Theme/styling code
- Common widget patterns (cards, sidebars, metric displays)

### Performance

- UI thread never blocks — use `QThread` for system calls
- Data collection runs asynchronously with periodic refresh
- Heavy operations (package listing, hardware detection) run in background threads
- Application startup targets < 500ms

---

## Key Design Decisions

### Why PySide6 (Qt6)?

| Criteria | PySide6 | GTK4 | Tkinter | Electron |
|----------|---------|------|---------|----------|
| Native look on Wayland | ✅ | ✅ | ⚠️ | ❌ |
| Dark theme support | ✅ Native QSS | ✅ | ⚠️ | ✅ (CSS) |
| Python type hints | ✅ | ⚠️ | ❌ | ❌ |
| Memory footprint | Low | Low | Very low | High |
| Startup time | Fast | Fast | Fast | Slow |

### Why Hyprland?

- Dynamic tiling with Wayland-native performance
- GPU-accelerated rendering via wlroots
- Extremely configurable (no hardcoded behavior)
- Low idle RAM (~200 MB)
- Active, growing community

### Why linux-zen?

- Lower latency than stock linux
- Better desktop interactivity under load
- Includes BBR congestion control, MuQSS scheduler
- Same kernel ABI as stock (compatible with proprietary drivers)

### Why Not Systemd Services for Apps?

HyperOS applications are desktop GUI applications, not background daemons. systemd services are provided only where appropriate (Hyper Update for background checks, Hyper Backup for scheduled snapshots). All GUI apps are launched via `.desktop` entries through the application menu or autostart.

---

## Shared Core Library (hyperos-core)

```
core/hyperos_core/
├── __init__.py
├── domain/
│   ├── __init__.py
│   └── models.py              # SystemInfo, NetworkInfo, StorageInfo,
│                               # ServiceInfo, PackageInfo, UserInfo, PowerProfile
├── services/
│   ├── __init__.py
│   ├── system_service.py      # CPU, memory, kernel, uptime
│   ├── network_service.py     # Interfaces, connectivity, wireless
│   ├── pacman_service.py      # Package queries, installation
│   ├── service_manager.py     # systemd unit management
│   ├── hardware_service.py    # GPU, disks, peripherals
│   └── power_service.py      # Governor, profiles, battery
├── widgets/
│   ├── __init__.py
│   ├── card.py                 # InfoCard, MetricCard
│   ├── sidebar.py              # NavigationSidebar
│   ├── theme.py                # apply_theme(), QSS stylesheet
│   └── styles.py               # Color constants, style helpers
└── tests/
    └── test_services.py
```

### Service Patterns

Each service follows a consistent pattern:

```python
class XService:
    """Description of what this service provides."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_info(self) -> XInfo:
        """Returns domain model with collected data."""
        pass

    def refresh(self) -> None:
        """Forces data refresh."""
        pass
```

Services collect system data via:
- Reading `/proc/` and `/sys/` filesystem
- Parsing output of system commands (subprocess)
- Querying systemd via DBus (via `systemctl`)
- Reading configuration files

---

## Package Layout

Each application is a standard Arch Linux package with a consistent structure:

```
packages/hyper-<name>/
├── PKGBUILD                    # Arch Linux package build recipe
├── README.md                   # Package documentation
├── src/
│   ├── pyproject.toml          # Python packaging metadata
│   └── hyper_<name>/           # Python source code
├── data/
│   ├── hyper-<name>.desktop    # Freedesktop desktop entry
│   └── hyper-<name>.service    # systemd user service (optional)
├── assets/
│   └── icons/
│       └── hyper-<name>.svg    # Application icon (SVG, scalable)
└── tests/                      # Additional integration tests
    └── test_<name>.py
```

### Dependencies Between Packages

```
                hyper-installer
                      |
               hyper-backup
                  |
hyper-welcome → hyper-center ← hyper-settings
                  |       |
                  |   hyper-update
                  |       |
              hyper-store → hyper-drivers
                  |
           hyper-assistant
```

All applications depend on `hyperos-core` (the shared library). No application depends on another application.

---

## Data Flow

### User Request Flow

```
User Input (click/keyboard)
    ↓
UI Widget (Page/Section)
    ↓  calls service method
Service Layer
    ↓  reads/writes
System (proc, sysctl, commands, config files)
    ↓  returns data
Service Layer
    ↓  returns domain model
UI Widget
    ↓  updates display
User sees result
```

### Data Refresh Cycle

```
[Timer] → Service.refresh() → System Query → Domain Model → UI Update
   ↑                                                            |
   └────────────────────────────────────────────────────────────┘
```

Each application caches data and refreshes on a configurable interval (default 5 seconds for live data, on-demand for static data).

---

## Communication Between Components

### IPC and Coordination

| Method | Purpose | Used By |
|--------|---------|---------|
| **DBus** | System-wide notifications | System services, session management |
| **Filesystem** | Shared state (configs, caches) | All applications |
| **Command line** | Application invocation | Launcher, scripts, terminal |

### Direct Application Integration

Applications do not communicate with each other directly. Integration happens through:
- Shared files in `~/.config/hyperos/`
- System-wide settings in `/etc/hyperos/`
- The `hyperos-core` library

---

## Configuration System

### Configuration Hierarchy

```
lowest priority: /etc/hyperos/defaults.toml       (system defaults)
                 /etc/hyperos/<profile>.toml       (distribution profile)
                 ~/.config/hyperos/settings.toml   (user settings)
highest priority: CLI flags / environment vars     (runtime overrides)
```

### Configuration Files

| Path | Purpose |
|------|---------|
| `/etc/hyperos/hyperos.conf` | Main system configuration |
| `~/.config/hyperos/settings.toml` | User preferences |
| `/etc/hyperos/profiles.toml` | Performance profile definitions |
| `/etc/hyperos/blacklist` | Package blacklist for Hyper Store |

All configuration is versioned and backed up with the system.

---

## Boot Process

```
BIOS/UEFI → Bootloader (GRUB/systemd-boot)
    ↓
Linux Kernel (linux-zen)
    ↓
initramfs → Mount root filesystem
    ↓
systemd (PID 1)
    ↓
Plymouth Boot Splash ← hyperos-boot.service
    ↓
Network (NetworkManager) ← NetworkManager.service
    ↓
Display Manager (SDDM) ← sddm.service
    ↓
Desktop Environment (Hyprland) ← hyprland.desktop
    ↓
User Session ← hyperos-session.target
    ├── hyper-welcome (first boot only)
    ├── hyprland.conf (keybinds, rules, monitors)
    ├── waybar (status bar)
    └── dunst (notifications)
```

### Session Targets

```
hyperos-session.target
├── hyperos-welcome.service    # First-boot welcome (runs once)
├── hyperos-update.service     # Background update checker
└── hyperos-backup.service     # Scheduled backup timer
```

---

## Performance Architecture

### Profiles

HyperOS provides 4 performance profiles that adjust CPU, I/O, and memory behavior:

| Profile | CPU Governor | Swappiness | I/O Scheduler | Use Case |
|---------|-------------|-----------|---------------|----------|
| **Balanced** | schedutil | 60 | kyber | Daily use, good battery life |
| **Performance** | performance | 10 | none | Demanding tasks, compilation, rendering |
| **Power Saver** | powersave | 100 | kyber | Battery saving, laptops unplugged |
| **Gaming** | performance | 10 | none | Gaming, reduced latency |

Each profile is applied via `sysctl` and `cpupower` commands through the PowerService.

---

## Security Architecture

### Principle of Least Privilege

- GUI applications run as the **user** (not root)
- Privileged operations use **polkit** authentication
- System services run as dedicated **system users**
- No application has direct root access

### Security Boundaries

```
┌──────────────────────┐
│   User Applications  │  Unprivileged user space
├──────────────────────┤
│   Polkit / sudo      │  Authentication boundary
├──────────────────────┤
│   System Services    │  Privileged system space
├──────────────────────┤
│   Kernel             │  Hardware access
└──────────────────────┘
```

### Secure Defaults

- Firewall enabled by default (nftables)
- SSH disabled by default
- Bluetooth disabled by default
- Auditd configured for security events
- No setuid binaries except those from Arch Linux base
- /tmp mounted as tmpfs with noexec,nosuid
- Kernel hardening via sysctl

---

## Scalability and Future-Proofing

The architecture is designed to accommodate future features without restructuring:

| Feature | Architecture Impact |
|---------|-------------------|
| Online package repository | Add repository config to pacman.conf |
| OTA updates | Add update service with download manager |
| Cloud sync | Add cloud service to hyperos-core |
| AI assistant integration | Hyper Assistant plugin engine ready |
| Gaming mode | Performance profile + compositor tweaks |
| Flathub integration | Add flatpak as optional backend to Hyper Store |
| Custom kernel (linux-hyperos) | New package in packages/hyper-kernel |
| Mobile edition | New desktop config in configs/ |

No future feature requires restructuring the repository or modifying the architecture layers.

---

## Summary Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HYPEROS DISTRIBUTION                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    GUI APPLICATIONS                         │   │
│  │  ┌──────┐ ┌──────┐ ┌────────┐ ┌─────┐ ┌─────┐ ┌────────┐ │   │
│  │  │Welcome│ │Center│ │Settings│ │Store│ │Update│ │Drivers │ │   │
│  │  └──────┘ └──────┘ └────────┘ └─────┘ └─────┘ └────────┘ │   │
│  │  ┌────────┐ ┌──────┐ ┌──────────┐ ┌────┐ ┌────────┐     │   │
│  │  │Backup  │ │Asst. │ │Installer │ │CLI │ │Gaming  │     │   │
│  │  └────────┘ └──────┘ └──────────┘ └────┘ └────────┘     │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │                    CORE LIBRARY                             │   │
│  │  Domain │ Services │ Widgets │ Theme │ Styles              │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │              CONFIGURATION & SYSTEM                         │   │
│  │  systemd · udev · polkit · sysctl · NetworkManager         │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │              ARCH LINUX BASE                                │   │
│  │  linux-zen · glibc · systemd · pacman · Wayland            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```
