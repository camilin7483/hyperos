# Hyper Store Architecture

## Overview

Hyper Store is a GTK4/libadwaita application that wraps pacman for package management operations.

## Component Tree

```
HyperStore
├── Browser
│   ├── CategoryList
│   ├── PackageGrid
│   └── SearchBar
├── PackageDetail
│   ├── InfoPanel
│   ├── ScreenshotGallery
│   └── ActionButtons
└── Updates
    └── UpdateList
```

## Data Flow

1. Browser queries `libhyper-package` for package listings
2. PackageDetail fetches metadata and screenshots
3. Install/remove operations are delegated to `libhyper-package`
4. Updates check against repository metadata

## Communication

- Package operations via `libhyper-package` (pacman wrapper)
- Repository configuration via `libhyper-config`
- Installation progress via DBus signals
