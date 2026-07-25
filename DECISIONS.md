# Architecture Decision Records

This document records key architectural decisions made during HyperOS development.

## ADR-001: Default Desktop Environment

**Status**: Accepted

**Context**: HyperOS needs a default desktop environment that aligns with its performance and minimalism goals.

**Decision**: Hyprland (Wayland) is the default desktop. The architecture remains desktop-agnostic, allowing future editions (KDE, XFCE, GNOME) to be added without restructuring.

**Consequences**:
- Active development focuses on Hyprland
- Configuration system supports desktop-specific profiles
- Future editions can be added as new profiles

## ADR-002: Kernel Strategy

**Status**: Accepted

**Context**: HyperOS needs a kernel that balances performance and stability.

**Decision**: Use linux-zen as the default kernel. No custom kernel development yet. The `kernel/` directory prepares for a future linux-hyperos.

**Consequences**:
- ISO uses linux-zen
- Kernel configuration placeholders exist for future work
- No maintenance burden of a custom kernel during early development

## ADR-003: Project Language

**Status**: Accepted

**Context**: The project must be accessible to an international audience.

**Decision**: English is used for all code, documentation, comments, commit messages, and identifiers.

**Consequences**:
- Consistent communication across the project
- Professional appearance
- International accessibility

## ADR-004: Shared Core Architecture

**Status**: Accepted

**Context**: Multiple HyperOS applications need common functionality.

**Decision**: A `core/` directory provides shared libraries, IPC, DBus interfaces, schemas, and API definitions. All applications depend on this core.

**Consequences**:
- No duplicated logic across applications
- Consistent behavior
- Clear dependency graph

## ADR-005: Visual Identity

**Status**: Accepted

**Context**: HyperOS needs a professional visual identity.

**Decision**: Minimal, clean design with black, dark gray, white, and electric blue (#00AEEF). Avoid RGB gaming aesthetics.

**Consequences**:
- Professional appearance
- Consistent branding across all components
- Easy to extend for community themes

## ADR-006: Build System

**Status**: Accepted

**Context**: HyperOS needs a reproducible build process.

**Decision**: Use ArchISO for ISO generation and standard PKGBUILD format for packages.

**Consequences**:
- Follows Arch Linux standards
- Familiar to Arch users and contributors
- easy integration with existing tooling

## ADR-007: Display Manager Configuration (ISO)

**Status**: Accepted · 2026-07-25

**Context**: The live ISO boots to SDDM for graphical login. Initial config used `DisplayServer=wayland` but the Wayland greeter crashed in the live environment (no Wayland compositor running for SDDM to connect to). Also lacked serial console access for debugging.

**Decision**:
1. SDDM `DisplayServer=x11` — more compatible with live ISO environment; Xorg starts on demand via SDDM
2. Syslinux `SERIAL 0 115200` — enables serial console for headless/QEMU debugging

**Consequences**:
- SDDM greeter works reliably in both live ISO and installed system
- Serial console available for kernel/bootloader debugging
- Hyprland session still launched as Wayland compositor after SDDM login
