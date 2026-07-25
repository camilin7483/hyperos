# HyperOS Roadmap

## Current Status — v0.5

HyperOS has a bootable ISO with all 10 GUI applications. The ISO boots successfully (ISOLINUX → kernel → userspace) and is ready for testing on real hardware. GitHub CI/CD pipeline configured.

## Milestones

### v0.1 — Foundation
- [x] Repository structure
- [x] Documentation
- [x] ArchISO base

### v0.2 — Bootable ISO
- [x] Bootable ISO generation
- [x] Branding placeholders
- [x] Basic system configuration
- [x] Plymouth boot splash

### v0.3 — Hyper Welcome
- [x] Post-installation welcome screen
- [x] System detection
- [x] First-run setup
- [x] PySide6 GUI application
- [x] First-boot state management
- [x] systemd integration
- [x] Tests

### v0.4 — Core Applications
- [x] hyperos-core shared library
- [x] Hyper Center (control panel)
- [x] Hyper Settings (system settings)
- [x] Hyper Update (system updater)
- [x] Hyper Store (software center)
- [x] Hyper Drivers (driver manager)
- [x] Hyper Backup (snapshot manager)
- [x] Hyper Assistant (offline assistant)
- [x] Hyper Installer (graphical installer)

### v0.5 — Stable ISO (2026-07-25)
- [x] Bootable ISO build
- [x] Live environment validation (QEMU: kernel + userspace OK)
- [x] SDDM configuration (DisplayServer=x11, auto-login hyperos → Hyprland)
- [x] Serial console debugging (SERIAL 0 115200 in syslinux)
- [x] ISO build fixes (stale mounts, /etc/resolv.conf, /dev/null)
- [x] Local package repository (local-repo/)
- [x] GitHub CI/CD pipeline
- [x] Bug fixing and polish

### v0.6 — Testing & CI

- [ ] Test ISO on real hardware (USB boot, SDDM + Hyprland + all apps)
- [ ] Fix initramfs microcode embedding (`/dev/stdin` missing in mkinitcpio)
- [ ] Add screenshots to README (Hyper Welcome, Hyper Center, Hyper Settings, Hyper Store)
- [ ] CI: build packages in container before ISO (remove dependency on local-repo/)
- [ ] Unit test coverage for all packages
- [ ] Performance: move all subprocess calls to QThread workers
- [ ] Hyper Assistant LLM integration (Ollama)
- [ ] Hyper Installer real disk partitioning (archinstall integration)
- [ ] Security audit pass
- [ ] hyper-cli / hyper-gaming / hyper-kernel implementation

### v1.0 — Stable Release

- [ ] All core features complete
- [ ] Stable ISO tested on multiple hardware configurations
- [ ] Package repository (public, signed)
- [ ] Installation guide and user documentation
- [ ] Community contributions

## Future Possibilities

- Hyper Kernel (custom linux-hyperos)
- AI integration in Hyper Assistant
- KDE Plasma edition
- XFCE edition
- GNOME edition
- ARM architecture support
- Flatpak/AppImage support
- Secure Boot support
- Full disk encryption installer
- OTA updates (offline and online)
