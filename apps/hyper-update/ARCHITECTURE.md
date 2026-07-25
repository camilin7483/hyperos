# Hyper Update Architecture

## Overview

Hyper Update wraps pacman and provides a graphical update management interface.

## Component Tree

```
HyperUpdate
├── UpdateChecker
│   ├── CheckUpdates
│   └── UpdateList
├── UpdateInstaller
│   ├── InstallQueue
│   └── ProgressMonitor
└── Notifier
    ├── TrayIcon
    └── NotificationService
```

## Data Flow

1. UpdateChecker queries `libhyper-package` for available updates
2. UpdateInstaller manages the installation process
3. Notifier shows tray icon and desktop notifications
