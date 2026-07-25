# Overlay

Filesystem overlays for HyperOS.

## Purpose

This directory contains files that are overlaid onto the Arch Linux base system during ISO generation or installation. These files customize the default behavior, appearance, and configuration of the system.

## Usage

Files in this directory mirror the root filesystem structure. For example:

```
overlay/
├── etc/
│   ├── profile
│   └── bash.bashrc
└── usr/
    └── share/
        └── backgrounds/
            └── hyperos-wallpaper.png
```

## Relationship with archiso

The `archiso/airootfs/` directory contains the live environment overlay. This `overlay/` directory is for the installed system.
