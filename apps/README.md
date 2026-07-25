# Applications

Graphical user interface applications for HyperOS.

## Philosophy

Every administrative task should be available through a graphical interface. The terminal should remain optional.

## Applications

| Application | Purpose | Target Version |
|-------------|---------|----------------|
| Hyper Center | Central control panel | v0.4 |
| Hyper Store | Application store | v0.5 |
| Hyper Settings | System settings | v0.4 |
| Hyper Drivers | Driver manager | v0.8 |
| Hyper Welcome | Post-install welcome (implemented) | v0.3 ✅ |
| Hyper Backup | Backup and restore | Future |
| Hyper Update | System updater | v0.6 |
| Hyper Assistant | AI assistant | Future |

## Architecture

Each application is independent and communicates through the core libraries in `core/`. See `ARCHITECTURE.md` for each application for details.
