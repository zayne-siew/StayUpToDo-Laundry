"""Model for the laundry machine system"""
from datetime import datetime
from typing import TypedDict

from src.models.status_history import StatusHistoryEntry, StatusHistoryEntryDict
from src.models.telegram_message import TelegramMessage, TelegramMessageDict
from src.types.enums import MachineStatus, MachineType

class MachineDict(TypedDict):
    id: str
    block_number: int
    status: str
    status_history: list[StatusHistoryEntryDict]
    estimated_finish_time: str | None  # ISO 8601 UTC timestamp
    telegram_message: TelegramMessageDict | None


class Machine:
    """Model for laundry machine"""
    _VALID_BLOCKS = {55, 57, 59}
    MAX_RUN_TIME_SECONDS = 50 * 60  # 50 minutes in seconds
    
    def __init__(
        self,
        id: str,
        block_number: int,
        status: MachineStatus = MachineStatus.AVAILABLE,
        status_history: list[StatusHistoryEntry] | None = None,
        estimated_finish_time: str | None = None,
        telegram_message: TelegramMessage | None = None
    ):
        if block_number not in self._VALID_BLOCKS:
            raise ValueError(f"Block number must be one of {self._VALID_BLOCKS}, got {block_number}")
        
        self._id = id
        self._block_number = block_number
        self._status = status
        self._status_history = status_history or []
        self._estimated_finish_time = estimated_finish_time
        self._telegram_message = telegram_message

    @property
    def status(self) -> MachineStatus:
        return self._status

    @property
    def status_history(self) -> list[StatusHistoryEntry]:
        return self._status_history

    @property
    def estimated_finish_time(self) -> str | None:
        """Get estimated finish time in ISO 8601 UTC format"""
        return self._estimated_finish_time
    
    @estimated_finish_time.setter
    def estimated_finish_time(self, value: str | None) -> None:
        """Set estimated finish time. Must be ISO 8601 UTC timestamp or None"""
        if value is not None:
            # Validate that it's a valid ISO 8601 timestamp
            try:
                datetime.fromisoformat(value.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid ISO 8601 timestamp: {value}")
        self._estimated_finish_time = value

    @property
    def telegram_message(self) -> TelegramMessage | None:
        return self._telegram_message
    
    @telegram_message.setter
    def telegram_message(self, message: TelegramMessage | None) -> None:
        self._telegram_message = message
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def block_number(self) -> int:
        """Get block number"""
        return self._block_number

    @property
    def type(self) -> MachineType:
        """Get machine type from ID (e.g., '57W4' -> WASHER)"""
        # ID format: <block><type><number> (e.g., 57W4)
        for char in self._id:
            if char in ('W', 'D'):
                return MachineType.WASHER if char == 'W' else MachineType.DRYER
        raise ValueError(f"Invalid machine ID format: {self._id}")

    @property
    def number(self) -> int:
        """Get machine number from ID (e.g., '57W4' -> 4)"""
        # Extract the number part after W or D
        for i, char in enumerate(self._id):
            if char in ('W', 'D'):
                return int(self._id[i+1:])
        raise ValueError(f"Invalid machine ID format: {self._id}")

    def update_status(self, new_status: MachineStatus, user: str):
        """Update machine status and add to history"""
        self._status = new_status
        self._status_history.append(
            StatusHistoryEntry(
                status=new_status,
                timestamp=datetime.now(),
                user=user
            )
        )

    def to_dict(self) -> MachineDict:
        """Convert to dictionary"""
        return MachineDict(
            id=self._id,
            block_number=self._block_number,
            status=self._status.value,
            status_history=[entry.to_dict() for entry in self._status_history],
            estimated_finish_time=self._estimated_finish_time,
            telegram_message=self._telegram_message.to_dict() if self._telegram_message else None
        )

    @classmethod
    def from_dict(cls, data: MachineDict) -> 'Machine':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            block_number=data['block_number'],
            status=MachineStatus(data['status']),
            status_history=[
                StatusHistoryEntry.from_dict(entry)
                for entry in data.get('status_history', [])
            ],
            estimated_finish_time=data.get('estimated_finish_time'),
            telegram_message=(
                None if data['telegram_message'] is None
                else TelegramMessage.from_dict(data['telegram_message'])
            ),
        )


if __name__ == "__main__":
    pass
