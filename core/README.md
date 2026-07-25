# Core

Shared infrastructure and libraries for HyperOS applications.

## Design

The core directory provides common functionality that all HyperOS applications depend on. This prevents code duplication and ensures consistent behavior.

## Structure

| Directory | Purpose |
|-----------|---------|
| `libraries/` | Shared utility libraries |
| `shared/` | Common data and constants |
| `ipc/` | Inter-process communication interfaces |
| `dbus/` | DBus service definitions |
| `schemas/` | Data schemas and validation |
| `api/` | Core API definitions |

## Principles

- Every application depends on core, not on other applications
- Core has no dependencies on applications
- All communication goes through defined interfaces
- No duplicated logic across the project
