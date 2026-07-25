# Scripts

Build and maintenance scripts for HyperOS.

## Available Scripts

| Script | Purpose |
|--------|---------|
| `build.sh` | Orchestrate the full build process |
| `build-iso.sh` | Build the ArchISO image |
| `build-package.sh` | Build a single package |
| `clean.sh` | Remove build artifacts |
| `lint.sh` | Run validation checks |
| `test.sh` | Execute test suites |
| `release.sh` | Prepare a project release |
| `package.sh` | Build all HyperOS packages |
| `setup-dev.sh` | Configure development environment |
| `chroot.sh` | Enter the ISO chroot for debugging |

## Usage

```bash
./scripts/build-iso.sh    # Build the ISO
./scripts/lint.sh          # Validate code
./scripts/clean.sh         # Clean artifacts
```

All scripts support `--help` for usage information.
