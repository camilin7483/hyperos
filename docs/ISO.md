# HyperOS ISO Documentation

## Overview

HyperOS uses `archiso` to build a bootable ISO image containing a complete Live environment with the ability to install HyperOS to disk.

## Directory Structure

Perfil usado por CI y por `scripts/build-iso.sh`:

```
archiso/
├── profiledef.sh              # Main archiso profile definition
├── pacman.conf                # Custom pacman configuration (CI inyecta [hyperos-local])
├── packages.x86_64            # Lista de paquetes del Live environment
├── airootfs/                  # Root filesystem customization
│   ├── root/
│   │   └── .automated_script.sh  # First-boot automation
│   └── etc/
│       ├── sddm.conf.d/       # Display manager configuration
│       └── skel/              # User template directory
│           └── .config/
│               ├── hypr/      # Hyprland configuration
│               ├── waybar/    # Waybar configuration
│               └── autostart/ # Autostart applications
```

`iso/` es el perfil heredado (v0.5), con su propio `iso/build-iso.sh`; el perfil oficial es `archiso/`.

## Building the ISO

### Prerequisites

```bash
sudo pacman -S archiso
```

### Build Process (local)

1. **Build all packages and create the local repository:**
   ```bash
   ./build.sh all
   # Crea build/repository/x86_64/*.pkg.tar.zst
   ```

2. **Añadir el repo local al pacman.conf del perfil** (mkarchiso usa el pacman.conf del perfil, no el del host):
   ```
   # archiso/pacman.conf
   [hyperos-local]
   SigLevel = Never
   Server = file:///abs/path/hyperos/build/repository/x86_64
   ```

3. **Build the ISO:**
   ```bash
   ./scripts/build-iso.sh
   ```

4. **Output location:**
   ```
   out/hyperos-<fecha>-x86_64.iso      # ej: out/hyperos-2026.08.14-x86_64.iso
   ```

### Build en CI (GitHub Actions)

El flujo oficial es el workflow [build-iso.yml](../.github/workflows/build-iso.yml), que corre en cada push a `main`:

1. Instala deps (`base-devel`, `python-build/installer/wheel/setuptools`, `pyside6`, `archiso`)
2. Crea el usuario `builduser` (makepkg no puede correr como root)
3. `makepkg` de `core/` → `pacman -U` del paquete en el contenedor
4. `scripts/package.sh` como builduser → 14 paquetes `packages/hyper-*`
5. `repo-add` en `local-repo/x86_64` + inyección de `[hyperos-local]` en `archiso/pacman.conf`
6. `mkdir -p out/work` + `mkarchiso`
7. Sube el artefacto `hyperos-iso` (~1.9 GB)

Al taggear (`v*`), [release.yml](../.github/workflows/release.yml) publica la ISO y los 14 `.pkg.tar.zst` en GitHub Releases. La ISO de la última release: https://github.com/camilin7483/hyperos/releases

### What the Build Script Does

1. Checks dependencies (archiso, mkarchiso)
2. Creates `out/work` and `out`
3. Runs mkarchiso against the `archiso/` profile
4. Produces `out/hyperos-<fecha>-x86_64.iso`

## Testing the ISO

### Quick Test in QEMU

```bash
./scripts/test-iso.sh
```

This script:
- Creates a temporary 20GB disk image
- Configures UEFI boot
- Launches QEMU with the ISO
- Provides a test checklist
- Cleans up after exit

### Manual QEMU Testing

```bash
qemu-system-x86_64 \
  -enable-kvm \
  -m 4G \
  -smp 2 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/x64/OVMF_CODE.4m.fd \
  -drive if=pflash,format=raw,file=/tmp/ovmf-vars.4m.fd \
  -cdrom out/hyperos-2026.08.14-x86_64.iso \
  -boot d \
  -usb -device usb-tablet -device usb-kbd \
  -vga virtio \
  -display gtk
```

## Live Environment Features

### Pre-configured Components

- **Hyprland**: Wayland compositor with custom keybindings
- **Waybar**: Status bar with Catppuccin theme
- **SDDM**: Display manager for login
- **NetworkManager**: Network connectivity (WiFi/Ethernet)
- **PipeWire**: Audio server
- **Bluetooth**: BlueZ stack with blueman GUI
- **XDG Portals**: Screen sharing and file dialogs

### Default Applications

| Category | Application |
|----------|-------------|
| Terminal | kitty |
| File Manager | dolphin |
| App Launcher | wofi |
| Browser | firefox (install from repo) |
| Settings | hyper-settings |
| System Center | hyper-center |
| Store | hyper-store |
| Installer | hyper-installer |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| SUPER+Return | Open terminal |
| SUPER+D | App launcher |
| SUPER+C | Hyper Center |
| SUPER+I | Hyper Settings |
| SUPER+E | File manager |
| SUPER+L | Lock screen |
| SUPER+F | Fullscreen toggle |
| SUPER+SHIFT+Q | Logout |
| SUPER+1-0 | Switch workspace |
| Print | Screenshot (area) |
| SUPER+Print | Screenshot (full) |

## Installation from Live Environment

1. Boot the ISO
2. Connect to network (automatic or via nm-applet)
3. Launch installer:
   ```bash
   hyper-installer
   ```
4. Follow the installation wizard
5. Reboot and remove ISO

## Customization

### Adding Packages

Edit `archiso/packages.x86_64` and add the package name (los paquetes `hyper-*` requieren que el repo local `[hyperos-local]` esté configurado en `archiso/pacman.conf`, como hace CI):

```bash
packages=(
    # ... existing packages
    your-package
)
```

### Changing Desktop Configuration

Modify files in `archiso/airootfs/etc/skel/.config/`:
- `hypr/hyprland.conf` - Compositor settings
- `waybar/config.jsonc` - Bar layout
- `waybar/style.css` - Bar theme

### Modifying First-Boot Script

Edit `archiso/airootfs/root/.automated_script.sh` to change:
- Network setup
- Service enabling
- Welcome message
- Auto-started applications

## Troubleshooting

### ISO Build Fails

**Missing dependencies:**
```bash
sudo pacman -S archiso
```

**Package build errors:**
```bash
./build.sh packages 2>&1 | tee build.log
# Review build.log for specific errors
```

**`target not found: hyper-*` durante el pacstrap:**
- Falta el repo local en `archiso/pacman.conf`: añade `[hyperos-local]` con `Server = file:///.../build/repository/x86_64` (ver "Build Process").
- En CI esto lo inyecta el workflow automáticamente.

**`realpath: out/work: No such file or directory`:**
- `mkdir -p out/work` antes de `mkarchiso` (ya lo hace `scripts/build-iso.sh` y los workflows).

### VM Boot Issues

**No display:**
- Try `-vga std` instead of `-vga virtio`
- Add `-display sdl` for alternative display

**UEFI boot fails:**
- Ensure OVMF is installed: `sudo pacman -S ovmf`
- Check UEFI variables are copied correctly

### Live Environment Issues

**No network:**
```bash
# Check NetworkManager status
systemctl status NetworkManager

# Restart network
nmcli networking off && nmcli networking on
```

**No audio:**
```bash
# Check PipeWire status
systemctl --user status pipewire pipewire-pulse wireplumber

# Restart audio services
systemctl --user restart pipewire pipewire-pulse wireplumber
```

**Hyprland doesn't start:**
```bash
# Check logs
journalctl --user -u hyprland

# Try manual start
Hyprland
```

## ISO Specifications

| Property | Value |
|----------|-------|
| Base | Arch Linux |
| Kernel | linux (latest stable) |
| Init System | systemd |
| Display Server | Wayland |
| Compositor | Hyprland |
| Login Manager | SDDM |
| Package Manager | pacman |
| Filesystem | SquashFS (compressed) |
| Boot Modes | UEFI, BIOS (legacy) |
| Architecture | x86_64 |

## Release Checklist

El pipeline CI valida automáticamente (workflows `lint.yml`, `test.yml`, `build-iso.yml`, `release.yml`):

- [x] All packages build successfully (CI)
- [x] ISO builds without errors (CI)
- [ ] ISO boots in QEMU
- [ ] Live environment loads completely
- [ ] Network connectivity works
- [ ] Audio works
- [ ] Hyprland starts automatically
- [ ] All HyperOS apps launch
- [ ] Installer can be launched
- [x] Release published with ISO + packages (CI, tag `v*`)

## Security Considerations

- The local repository in the ISO uses `SigLevel = Optional TrustAll` for simplicity
- For production releases, implement proper package signing
- Review `.automated_script.sh` for security implications
- Ensure no sensitive data is included in the ISO

## Performance Tips

- Use KVM acceleration (`-enable-kvm`) for best VM performance
- Allocate at least 4GB RAM for smooth experience
- Use SSD or fast storage for installation target
- Enable hardware video decoding when available

## Related Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Packaging Guide](docs/PACKAGING.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Recovery Guide](docs/RECOVERY.md)
