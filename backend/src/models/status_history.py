"""Model for status history entry"""
from datetime import datetime
from typing import TypedDict

from src.types.enums import MachineStatus

class StatusHistoryEntryDict(TypedDict):
    status: str
    timestamp: str
    user: str


class StatusHistoryEntry:
    """Model for status history entry"""
    def __init__(self, status: MachineStatus, timestamp: datetime, user: str):
        self._status = status
        self._timestamp = timestamp
        self._user = user
    
    @property
    def status(self) -> MachineStatus:
        return self._status

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def user(self) -> str:
        return self._user

    def to_dict(self) -> StatusHistoryEntryDict:
        """Convert to dictionary"""
        return StatusHistoryEntryDict(
            status=self.status.value,
            timestamp=self.timestamp.isoformat(),
            user=self.user
        )

    @classmethod
    def from_dict(cls, data: StatusHistoryEntryDict) -> 'StatusHistoryEntry':
        """Create from dictionary"""
        return cls(
            status=MachineStatus(data['status']),
            timestamp=datetime.fromisoformat(data['timestamp']),
            user=data['user']
        )
    

if __name__ == "__main__":
    pass
