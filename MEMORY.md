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

## 2026-08-14 — v1.0.0 publicado con CI funcionando (WORK IN PROGRESS)
- Merge v1.0.0 (--allow-unrelated-histories) desde tarea qwen-code → main; PRs #1-#5 cerrados.
- CI reparado en main (commits d437dfc → bd8304d → 8d31d4f → dbcc79c):
  - Build ISO: --privileged, pipeline completo (makepkg core + package.sh como builduser,
    local-repo + repo-add, sección [hyperos-local] en archiso/pacman.conf — el del perfil,
    no del host —, mkdir -p out/work antes de mkarchiso).
  - PKGBUILDs: python-pyside6 → pyside6 (nombre real), core prepare() idempotente,
    hyper-kernel/gaming/cli instalan src/main.py directo, hyper-tools sha256sums=().
  - packages.x86_64: rofi-lbonn-wayland → rofi (solo AUR), fsck eliminado (util-linux).
  - Lint + Test + Build ISO: SUCCESS en 8d31d4f (ISO ~1.9 GB, artefacto hyperos-iso).
- Release: falló 403 (GITHUB_TOKEN read-only) → permissions: contents: write en
  release.yml (dbcc79c); tag v1.0.0 movido a dbcc79c, re-disparado. ✅ PUBLICADA:
  https://github.com/camilin7483/hyperos/releases/tag/v1.0.0 (ISO 1912 MB + 14 .pkg.tar.zst).
- PENDIENTE: rotar PAT expuesto (ghp_Mr67...f3u0), limpiar /tmp/opencode/hyperos-test.
