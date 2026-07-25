# Hyper Welcome Architecture

## Overview

Hyper Welcome is a PySide6 (Qt6) application following Clean Architecture.

## Layer Diagram

```
+-----------+
|    UI     |  PySide6 widgets, main window, stylesheet
+-----------+
|  Widgets  |  Reusable UI components (InfoCard, StatusIndicator, ActionButton)
+-----------+
| Services  |  SystemService, NetworkService, FirstBootService
+-----------+
|  Domain   |  Models (SystemInfo), Enums (FirstBootState)
+-----------+
```

## Component Tree

```
MainWindow
└── WelcomePage
    ├── Header (title, subtitle, version, status indicator)
    ├── System Grid (6 InfoCards: CPU, RAM, GPU, Storage, Kernel, Desktop)
    └── Actions (6 buttons + Exit)
```

## Data Flow

1. `MainWindow.showEvent()` triggers `WelcomePage.populate()`
2. `SystemService.collect()` reads `/proc/cpuinfo`, `/proc/meminfo`, `lspci`, etc.
3. `NetworkService.check_connectivity()` tests TCP connections to known hosts
4. `FirstBootService` manages state in `~/.config/hyperos/hyper-welcome.state`
5. On close, `FirstBootService.mark_completed()` writes state and suppresses future launches

## Key Dependencies

- **PySide6** (Qt6) — GUI framework (not GTK4)
- **Python 3.11+** — Runtime
- **systemd** — User service for automatic launch

## Communication

The application does not use DBus or IPC in this version. It reads system state directly from `/proc` and system commands.
