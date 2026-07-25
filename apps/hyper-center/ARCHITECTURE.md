# Hyper Center Architecture

## Overview

Hyper Center is a GTK4/libadwaita application that displays system information and provides access to HyperOS tools.

## Component Tree

```
HyperCenter
├── Dashboard
│   ├── SystemWidget (CPU, RAM, Disk)
│   ├── NetworkWidget
│   └── HealthWidget
├── Launcher
│   └── AppGrid
└── Settings
    └── ConfigPanel
```

## Data Flow

1. Dashboard queries `libhyper-system` for real-time metrics
2. Launcher discovers installed HyperOS applications via `core/ipc`
3. Settings reads/writes configuration via `libhyper-config`

## Communication

- Reads system metrics via `libhyper-system`
- Launches other apps via DBus activation
- Sends configuration changes via DBus signals
