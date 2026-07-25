# Hyper Settings Architecture

## Overview

Hyper Settings is a GTK4/libadwaita application organized as a navigation panel with category pages.

## Component Tree

```
HyperSettings
├── NavigationPanel
│   ├── AppearancePage
│   ├── HardwarePage
│   ├── SystemPage
│   ├── NetworkPage
│   └── PowerPage
└── SettingsManager
    └── ConfigBackend
```

## Data Flow

1. Each page reads/writes configuration via `libhyper-config`
2. Changes are applied immediately and persisted
3. DBus signals notify other components of changes

## Communication

- Reads/writes via `libhyper-config`
- Applies system changes via `libhyper-system`
- Notifies via DBus on configuration changes
