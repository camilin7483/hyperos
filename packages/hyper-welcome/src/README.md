# Hyper Welcome

First-boot welcome screen for HyperOS.

## Purpose

Hyper Welcome is the first application users see after booting HyperOS. It displays system information, provides quick access to key tools, and guides new users. It runs once on first boot and never appears again unless manually re-enabled.

## Features

- Welcome screen with HyperOS branding
- System information panel (CPU, RAM, GPU, Storage, Kernel, Desktop)
- Internet connectivity status indicator
- Quick action buttons (Hyper Center, Install Software, Documentation, GitHub, Settings, Exit)
- First-boot state management (runs once, then suppressed)
- Dark theme with HyperOS styling

## Architecture

The application follows Clean Architecture:

```
hyper_welcome/
├── app.py              # Application entry point
├── domain/
│   ├── models.py       # Data models (SystemInfo, ConnectivityStatus)
│   └── enums.py        # Enumerations (FirstBootState)
├── services/
│   ├── system_service.py    # System information collection
│   ├── network_service.py   # Internet connectivity check
│   └── firstboot_service.py # First-boot state persistence
├── ui/
│   ├── main_window.py  # Main application window
│   ├── welcome_page.py # Welcome content widget
│   └── styles.py       # Qt stylesheet (dark theme)
├── widgets/
│   ├── info_card.py    # System information card
│   ├── status_indicator.py # Connection status indicator
│   └── action_button.py    # Themed action button
├── resources/
│   ├── icons/
│   └── translations/
└── tests/
    ├── test_system_service.py
    └── test_firstboot_service.py
```

## Dependencies

- Python >= 3.11
- PySide6 >= 6.6

## Running

```bash
# Direct execution
python -m hyper_welcome

# Or after installation
hyper-welcome
```

## First-Boot Mechanism

The application checks `~/.config/hyperos/hyper-welcome.state` on startup:
- If the file contains `"state": "completed"` or `"state": "disabled"`, the app exits immediately
- Otherwise, it displays the welcome screen
- When the window is closed, the state file is written with `"state": "completed"`

To re-enable:
```bash
rm ~/.config/hyperos/hyper-welcome.state
```

## Integration

- Desktop entry: `/usr/share/applications/hyper-welcome.desktop`
- Systemd user service: `/usr/lib/systemd/user/hyperwelcome.service`
- Icon: `/usr/share/icons/hicolor/scalable/apps/hyper-welcome.svg`
