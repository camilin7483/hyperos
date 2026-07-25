# Changelog

## v0.5.0 — ISO Build & VM Testing (2026-07-25)

### Added
- QEMU testing scripts with VNC screenshot capture (Python RFB protocol)
- GPU compatibility testing: std VGA, virtio, virtio-gl
- Build wrapper script (`/tmp/build-iso-wrapper.sh`) with automated /etc/resolv.conf fix

### Fixed
- **SDDM**: Changed `DisplayServer` from wayland to x11 — Wayland greeter crashed in live ISO
- **Syslinux**: Added `SERIAL 0 115200` for serial console debugging
- **Pacman chroot**: Fixed empty `/etc/resolv.conf` during ISO build (nameservers missing → mirror resolution failure)
- **Stale mounts**: Clean umount of previous build artifacts (`out/work/`)
- **Broken /dev/null**: Recreated as char device 1,3 with 666 permissions

### Known Issues
- Initramfs: `/dev/stdin` not found during mkinitcpio microcode hook — early_cpio empty
  - UEFI boots with external intel-ucode.img / amd-ucode.img
  - BIOS (syslinux) boot won't have microcode updates
- SDDM/Hyprland require GPU with OpenGL 3.3+ — cannot fully test in QEMU (only TTY/fbcon)

## v0.4.0 — Core Applications (2026-07-25)

### Added
- **hyperos-core**: Shared Python library with domain models, services (System, Network, Pacman, Service Manager, Hardware, Power), reusable widgets (Card, MetricCard, Sidebar), UI theme/styles, and utilities
- **Hyper Center**: Central control panel with dashboard, system info, package manager, service manager, network monitoring, storage info, and performance profiles
- **Hyper Settings**: Full settings application with 11 sections: Appearance, Display, Audio, Network, Power, Keyboard, Mouse, Users, Language, Privacy, Accessibility
- **Hyper Update**: System updater with check/update/sync capabilities and pacman integration
- **Hyper Store**: Package browser with search, install, and remove functionality via pacman
- **Hyper Drivers**: Hardware detection and driver information (GPU vendor detection, kernel modules, firmware, Bluetooth, printers)
- **Hyper Backup**: Btrfs snapshot management via snapper integration
- **Hyper Assistant**: Offline assistant with plugin architecture and built-in responses
- **Hyper Installer**: 6-step graphical installer with disk selection, filesystem choice, user creation, locale settings, and install progress

### Changed
- Updated archiso/packages.x86_64 with all HyperOS packages and python-pyside6 dependency
- All apps follow Clean Architecture with PySide6 (Qt6)
- All apps include desktop entries, SVG icons, and PKGBUILDs

## v0.3.0 — Hyper Welcome (2026-07-25)

### Added
- Hyper Welcome: First-boot welcome screen with system info, connectivity check, and action buttons
- Runtime validation and bug fixing (CursorShape fix, threading improvements)
- Unit tests (22 tests passing)

## v0.0.1 — Initial Foundation (2026-07-25)

### Added
- Repository structure, documentation, ArchISO profile, branding, configuration system
- Build scripts, package skeletons, CI/CD infrastructure
