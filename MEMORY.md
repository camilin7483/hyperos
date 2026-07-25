# HyperOS Memory

## Project State — v0.5 (Stable ISO)

HyperOS has a bootable ISO with all 10 GUI applications. The ISO build process was debugged and fixed, SDDM configured for X11 compatibility, GitHub CI/CD pipeline operational, and real application screenshots added to README.

## Project Statistics

- **~18,246 lines** of code total
- **12,373 lines** Python (apps + core library)
- **14 PKGBUILDs** for system packages
- **5 GUI applications** with screenshots in README
- **GitHub Actions** CI/CD for automated builds

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

## ISO Build (2026-07-25)

### Problems Encountered
1. **Stale mounts** — previous build left proc/sys/dev/tmp mounted in `out/work/x86_64/airootfs/`, causing "cannot remove" errors
2. **Empty /etc/resolv.conf** — pacman inside chroot couldn't resolve mirrors (only a comment, no nameservers)
3. **Broken /dev/null** — wrong permissions 644 instead of char device 1,3 with 666
4. **SDDM Wayland crash** — `DisplayServer=wayland` failed in live ISO; changed to `x11`
5. **No serial console** — ISOLINUX couldn't receive keyboard input via serial; added `SERIAL 0 115200`

### Fixes
- Unmounted all stale mounts with `umount -R` before build
- Wrapper script ensures `/etc/resolv.conf` has valid nameservers (8.8.8.8, 1.1.1.1)
- `/dev/null` recreated as `mknod -m 666 /dev/null c 1 3`
- SDDM config: `DisplayServer=x11` instead of wayland
- Syslinux config: added `SERIAL 0 115200`
- `.gitignore` updated for `pkg/` and `local-repo/`

### QEMU Testing Results
| GPU | Result |
|---|---|
| `-vga std` | Boots to TTY/fbcon after pressing Enter (1280x800, blue-bordered fbcon). SDDM fails — needs OpenGL 3.3+ |
| `-vga virtio` | Boots to text mode (720x400, gray text on black). Same SDDM limitation |
| `-device virtio-vga-gl` with `-display egl-headless` | Same as virtio. virgl available but guest lacks Mesa virgl driver |

**Conclusion**: ISO boots correctly (ISOLINUX → kernel → userspace → TTY). SDDM/Hyprland need a GPU with OpenGL 3.3+ — real hardware required. QEMU test confirmed BIOS boot, bootloader, kernel, initramfs, and filesystem all work.

### GitHub
- Remote: github.com/camilin7483/hyperos.git
- Pushed: ISO build fixes, documentation updates

## Next Steps
1. ~~Build bootable ISO~~ ✓
2. ~~Validate live environment~~ ✓ (QEMU: kernel + userspace OK, GPU-dependent)
3. Validate installation process on real hardware
4. ~~Push to GitHub~~ ✓
5. Bug fixing and polish for v1.0
