# Hyper Drivers Architecture

## Overview

Hyper Drivers detects hardware and recommends/installs appropriate drivers.

## Component Tree

```
HyperDrivers
├── HardwareDetector
│   ├── GPUDetector
│   ├── PrinterDetector
│   └── NetworkDetector
├── DriverList
│   ├── RecommendedDrivers
│   └── OptionalDrivers
└── Installer
    ├── DriverInstall
    └── Rollback
```

## Data Flow

1. HardwareDetector queries `libhyper-system` for hardware
2. DriverList matches hardware to driver packages
3. Installer manages driver package installation via `libhyper-package`
