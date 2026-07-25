# ArchISO Profile

ArchISO profile for generating the HyperOS live ISO.

## Structure

```
archiso/
├── profiledef.sh       # Profile definition (name, version, publisher)
├── packages.x86_64     # Packages included in the ISO
├── pacman.conf         # Pacman configuration for the build
├── mkinitcpio.conf     # Initramfs configuration
├── efiboot/            # EFI boot entries
├── syslinux/           # Syslinux/ISOLINUX configuration
├── grub/               # GRUB theme and config
├── airootfs/           # Root filesystem overlay
└── splash.png          # Boot splash image
```

## Building

```bash
# From the repository root
./scripts/build-iso.sh
```

## Requirements

- `archiso` package installed
- Root privileges are not required (mkarchiso handles this)

## Overlay Configuration

Key files in `airootfs/`:

| File | Purpose |
|---|---|
| `etc/sddm.conf` | SDDM auto-login as `hyperos` user, Session=hyprland, DisplayServer=x11 |
| `etc/passwd`, `etc/shadow` | Pre-created `hyperos` user (UID 1000) with hashed password |
| `etc/systemd/system/graphical.target.wants/sddm.service` | Enables SDDM at boot |
| `usr/local/bin/hyperos-before` | First-boot setup script |
| `usr/local/bin/hyperos-welcome` | Welcome screen launcher |

## Syslinux Configuration

- `syslinux/syslinux.cfg`: ISOLINUX boot config with `SERIAL 0 115200` for serial console
- Boot labels: `hyperos` (default, with quiet splash), `hyperos-nofb` (nomodeset), memtest, hdt, reboot, poweroff
- Kernel cmdline: `archisobasedir=arch archisolabel=HYPEROS_202607 quiet splash`

## UEFI Boot

- `efiboot/loader/loader.conf`: systemd-boot with 5s timeout, HyperOS as default entry
- External microcode images: intel-ucode.img, amd-ucode.img

## Building from Scratch

```bash
# Clean rebuild
./scripts/clean.sh && ./scripts/build.sh
```

## QEMU Testing

The ISO boots correctly in QEMU (ISOLINUX → kernel → userspace) but the graphical desktop (SDDM/Hyprland) requires a GPU with OpenGL 3.3+. In QEMU without virgl, only the TTY/framebuffer console is available.

```bash
# Basic boot test (VNC port 5900)
qemu-system-x86_64 -enable-kvm -m 4096 \
  -cdrom out/hyperos-*.iso \
  -vnc :0 -usb -device usb-tablet

# With virtio GPU and GL acceleration
qemu-system-x86_64 -enable-kvm -m 4096 \
  -cdrom out/hyperos-*.iso \
  -device virtio-vga-gl -display egl-headless \
  -vnc :0 -usb -device usb-tablet
```

## Customization

- Add packages to `packages.x86_64`
- Modify `profiledef.sh` to change ISO metadata
- Add files to `airootfs/` to include them in the live environment
