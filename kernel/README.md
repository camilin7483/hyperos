# Kernel

Kernel configuration and resources for HyperOS.

## Current Status

HyperOS uses the `linux-zen` kernel from the Arch Linux repositories. No custom kernel is maintained at this stage.

## Future: linux-hyperos

A custom kernel optimized for HyperOS (linux-hyperos) is planned for future releases. This directory prepares for that work.

## Structure

| Path | Purpose |
|------|---------|
| `configs/` | Kernel configuration files |
| `patches/` | Kernel patches for optimization |
| `scripts/` | Kernel build and management scripts |

## Adding a Custom Kernel

When the project is ready for a custom kernel:

1. Add kernel configuration to `configs/`
2. Add any required patches to `patches/`
3. Update the ISO profile to use `linux-hyperos` instead of `linux-zen`
4. Create the `hyper-kernel` package in `packages/hyper-kernel/`

This directory structure supports the transition without restructuring the repository.
