"""Enum definitions for the StayUpToDo Laundry backend."""
from enum import Enum

class MachineStatus(str, Enum):
    """Enum for machine status"""
    AVAILABLE = "available"
    PAID_FOR = "paidFor"
    IN_USE = "inUse"
    PENDING_UNLOAD = "pendingUnload"
    OUT_OF_ORDER = "outOfOrder"


class MachineType(str, Enum):
    """Enum for machine type"""
    WASHER = "washer"
    DRYER = "dryer"


if __name__ == "__main__":
    pass
