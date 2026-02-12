"""API resources for Flask-RESTful"""
from .machine import (
    MachineListResource,
    MachineResource,
    MachineStatusResource,
    MachineTimeResource,
    MachineTelegramResource,
    MachineHistoryResource,
    MachineInitializeResource
)

__all__ = [
    'MachineListResource',
    'MachineResource',
    'MachineStatusResource',
    'MachineTimeResource',
    'MachineTelegramResource',
    'MachineHistoryResource',
    'MachineInitializeResource'
]


if __name__ == "__main__":
    pass
