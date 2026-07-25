# System

System-level configuration for HyperOS.

## Contents

| Path | Purpose |
|------|---------|
| `systemd/` | Systemd service units and timers |
| `pam.d/` | PAM authentication configuration |
| `sysctl.d/` | Kernel parameters |
| `modprobe.d/` | Kernel module configuration |
| `udev/` | Device rules |
| `environment` | System-wide environment variables |

## Purpose

This directory contains system configuration that ships with HyperOS. These files are installed to their respective locations in `/etc/` during system installation.
