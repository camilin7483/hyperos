# HyperOS ISO Documentation

## Overview

HyperOS uses `archiso` to build a bootable ISO image containing a complete Live environment with the ability to install HyperOS to disk.

## Directory Structure

```
iso/
├── profiledef.sh              # Main archiso profile definition
├── pacman.conf                # Custom pacman configuration with HyperOS repo
├── build-iso.sh              # Build script for ISO creation
├── airootfs/                 # Root filesystem customization
│   ├── root/
│   │   └── .automated_script.sh  # First-boot automation
│   ├── etc/
│   │   ├── sddm.conf         # Display manager configuration
│   │   └── skel/             # User template directory
│   │       └── .config/
│   │           ├── hypr/     # Hyprland configuration
│   │           ├── waybar/   # Waybar configuration
│   │           └── autostart/ # Autostart applications
│   └── usr/
│       └── share/
│           └── wayland-sessions/ # Wayland session definitions
└── repo/
    └── x86_64/               # Local package repository
```

## Building the ISO

### Prerequisites

```bash
sudo pacman -S archiso squashfs-tools libisoburn qemu-base
```

### Build Process

1. **Build all packages first:**
   ```bash
   ./build.sh packages
   ```

2. **Build the ISO:**
   ```bash
   ./iso/build-iso.sh
   ```

3. **Output location:**
   ```
   build/hyperos-0.5.0-x86_64.iso
   build/hyperos-0.5.0-x86_64.iso.sha256
   ```

### What the Build Script Does

1. Checks dependencies (archiso, mkarchiso, sqfs, xorriso)
2. Cleans previous builds
3. Builds HyperOS packages if needed
4. Copies packages to local repository in ISO
5. Creates package database (hyperos.db)
6. Customizes AIROOTFS with configurations
7. Runs mkarchiso to build the ISO
8. Generates SHA256 checksum

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
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/x64/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=/tmp/ovmf-vars.fd \
  -cdrom build/hyperos-0.5.0-x86_64.iso \
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

Edit `iso/profiledef.sh` and add packages to the `packages_x86_64` array:

```bash
packages_x86_64=(
    # ... existing packages
    your-package
)
```

### Changing Desktop Configuration

Modify files in `iso/airootfs/etc/skel/.config/`:
- `hypr/hyprland.conf` - Compositor settings
- `waybar/config.jsonc` - Bar layout
- `waybar/style.css` - Bar theme

### Modifying First-Boot Script

Edit `iso/airootfs/root/.automated_script.sh` to change:
- Network setup
- Service enabling
- Welcome message
- Auto-started applications

## Troubleshooting

### ISO Build Fails

**Missing dependencies:**
```bash
sudo pacman -S archiso squashfs-tools libisobturn
```

**Package build errors:**
```bash
./build.sh packages 2>&1 | tee build.log
# Review build.log for specific errors
```

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

Before releasing an ISO:

- [ ] All packages build successfully
- [ ] ISO builds without errors
- [ ] ISO boots in QEMU
- [ ] Live environment loads completely
- [ ] Network connectivity works
- [ ] Audio works
- [ ] Hyprland starts automatically
- [ ] All HyperOS apps launch
- [ ] Installer can be launched
- [ ] SHA256 checksum generated
- [ ] Release notes updated
- [ ] Version number updated

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
