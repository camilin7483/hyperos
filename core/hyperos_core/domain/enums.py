from enum import Enum, auto


class PowerProfileType(Enum):
    BALANCED = auto()
    PERFORMANCE = auto()
    POWER_SAVE = auto()
    GAMING = auto()
    CUSTOM = auto()


class ServiceState(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    FAILED = auto()
    ACTIVATING = auto()
    DEACTIVATING = auto()
    NOT_FOUND = auto()


class PackageState(Enum):
    INSTALLED = auto()
    NOT_INSTALLED = auto()
    OUTDATED = auto()
    UPDATE_AVAILABLE = auto()


class SessionType(Enum):
    WAYLAND = auto()
    X11 = auto()
    TTY = auto()
    UNKNOWN = auto()
