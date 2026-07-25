# Configuration System

Centralized configuration for HyperOS.

## Design

The configuration system uses a layered approach:

1. **Defaults** — Hardcoded sensible defaults in each component
2. **System configs** — Files in `configs/` that override defaults
3. **User configs** — User-specific overrides in `~/.config/hyperos/`

All configuration follows a `.conf` format with commented options and documentation.

## Directories

| Directory | Purpose |
|-----------|---------|
| `system/` | Base system configuration (locale, hostname, time) |
| `desktop/` | Desktop environment configuration |
| `hyprland/` | Hyprland-specific configuration |
| `security/` | Security policies (firewall, sudo, apparmor) |
| `performance/` | Performance tuning and profiles |
| `network/` | Network configuration |
| `systemd/` | Systemd service configuration |

## Adding Configuration

1. Create a `.conf` file in the appropriate directory
2. Document all options with comments
3. Provide sensible defaults
4. Use the `hyperos-config` tool (future) to apply changes
