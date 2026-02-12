from typing import TypedDict

class TelegramMessageDict(TypedDict):
    message: str
    message_url: str | None


class TelegramMessage:
    """Model for Telegram message"""
    def __init__(self, message: str, message_url: str | None = None):
        self._message = message
        self._message_url = message_url

    @property
    def message(self) -> str:
        return self._message

    @property
    def message_url(self) -> str | None:
        return self._message_url

    def to_dict(self) -> TelegramMessageDict:
        """Convert to dictionary"""
        return TelegramMessageDict(
            message=self.message,
            message_url=self.message_url
        )

    @classmethod
    def from_dict(cls, data: TelegramMessageDict) -> 'TelegramMessage':
        """Create from dictionary"""
        return cls(
            message=data['message'],
            message_url=data.get('message_url')
        )
    

if __name__ == "__main__":
    pass
