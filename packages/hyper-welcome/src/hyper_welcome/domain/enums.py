"""Enumerations for Hyper Welcome domain."""

from enum import Enum, auto


class FirstBootState(Enum):
    """State of the first-boot flow."""

    PENDING = auto()
    COMPLETED = auto()
    SKIPPED = auto()
    DISABLED = auto()
