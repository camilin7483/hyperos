# HyperOS Memory

## Project State — v0.4 (Core Applications Complete)

HyperOS now has a complete set of GUI applications built on PySide6 (Qt6) with Clean Architecture. The shared `hyperos-core` library provides common services and widgets across all apps.

## Implemented Applications

### hyperos-core (shared library)
- Domain models: SystemInfo, NetworkInfo, StorageInfo, ServiceInfo, PackageInfo, UserInfo, PowerProfile
- Services: SystemService, NetworkService, PacmanService, ServiceManager, HardwareService, PowerService
- Widgets: Card, MetricCard, Sidebar, SidebarButton
- UI: Full dark theme QSS stylesheet, color constants
- Utils: Logging setup, permission helpers

### Hyper Welcome (packages/hyper-welcome/)
- First-boot welcome screen with system info display and action buttons
- Uses background QThread for non-blocking system info collection
- First-boot state management via JSON state file with 0600 permissions
- 22 unit tests passing

### Hyper Center (packages/hyper-center/)
- Central control panel with sidebar navigation
- Dashboard, System, Packages, Services, Network, Storage, Profiles sections
- Background data collection thread
- 4 tests passing

### Hyper Settings (packages/hyper-settings/)
- 11 settings pages: Appearance, Display, Audio, Network, Power, Keyboard, Mouse, Users, Language, Privacy, Accessibility

### Hyper Update (packages/hyper-update/)
- Pacman-based system updater with check/update/sync
- Output display for command results

### Hyper Store (packages/hyper-store/)
- Package browser with search, install, and remove via pacman
- Installed/search results tree view

### Hyper Drivers (packages/hyper-drivers/)
- Hardware detection: GPU vendor (NVIDIA/AMD/Intel), kernel modules, firmware, Bluetooth, printers

### Hyper Backup (packages/hyper-backup/)
- Btrfs snapshot management via snapper integration

### Hyper Assistant (packages/hyper-assistant/)
- Chat-based assistant with plugin engine
- JSON plugin system in ~/.config/hyperos/assistant-plugins/
- Built-in responses for time, help, greetings

### Hyper Installer (packages/hyper-installer/)
- 6-step graphical installer: Welcome → Disk → User → Locale → Install → Complete
- Disk detection via lsblk, filesystem selection (Btrfs/ext4), encryption option

## Architecture
- Desktop: Hyprland (Wayland) as default
- Kernel: linux-zen
- GUI Framework: PySide6 (Qt6)
- Language: English for all code
- License: GNU GPL v3
- Brand: Electric Blue #00AEEF
- Core library under core/ prevents code duplication

## Next Steps
1. Build bootable ISO
2. Validate live environment
3. Validate installation process
4. Push to GitHub
5. Bug fixing and polish for v1.0
