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
├── bootloader/         # Bootloader configuration
├── grub/               # GRUB theme and config
├── isolinux/           # ISOLINUX configuration
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

## Customization

- Add packages to `packages.x86_64`
- Modify `profiledef.sh` to change ISO metadata
- Add files to `airootfs/` to include them in the live environment
