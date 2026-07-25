# TODO

## Completed

- [x] Create repository structure
- [x] Write root documentation
- [x] Write directory README files
- [x] Create ArchISO profile
- [x] Create branding placeholders
- [x] Create configuration system
- [x] Create system layer
- [x] Create package placeholders
- [x] Create application architecture docs
- [x] Create core infrastructure
- [x] Create build scripts
- [x] Bootable ISO
- [x] Hyper Welcome application
- [x] Hyper Center
- [x] Hyper Store
- [x] Hyper Update
- [x] Hyper Settings
- [x] Hyper Backup
- [x] Driver Manager (Hyper Drivers)
- [x] Hyper Assistant
- [x] Hyper Installer
- [x] Plymouth theme
- [x] Full code audit and bug fixes
- [x] Build system fixes (mkinitcpio, syslinux, loader.conf)

## In Progress

- [ ] Validate ISO on real hardware (USB boot)
- [ ] Unit test coverage for all packages
- [ ] Threaded subprocess (QThread) for all GUI apps
- [ ] Real installer backend (archinstall integration)
- [ ] hyper-cli / hyper-gaming / hyper-kernel implementation

## Next Release (v0.6.0)

- [ ] Test ISO on real hardware (SDDM + Hyprland + apps)
- [ ] Fix initramfs microcode embedding (`/dev/stdin` missing in mkinitcpio)
- [ ] Complete unit test suite
- [ ] Performance: move all subprocess calls to QThread workers
- [ ] Hyper Assistant LLM integration (Ollama)
- [ ] Hyper Installer real disk partitioning
- [ ] CI: build packages in container before ISO
- [ ] Security audit pass
