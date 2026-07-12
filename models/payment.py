from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass(slots=True)
class Payment:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    activity_id: str = ""

    guild_id: int = 0

    channel_id: int = 0

    message_id: int = 0

    total: int = 0

    each: int = 0

    created_by: int = 0

    paid: list[int] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self):

        return {
            "id": self.id,
            "activity_id": self.activity_id,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "total": self.total,
            "each": self.each,
            "created_by": self.created_by,
            "paid": self.paid,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            id=data["id"],
            activity_id=data["activity_id"],
            guild_id=data["guild_id"],
            channel_id=data["channel_id"],
            message_id=data.get("message_id", 0),
            total=data["total"],
            each=data["each"],
            created_by=data["created_by"],
            paid=data.get("paid", []),
            created_at=data["created_at"]
        )