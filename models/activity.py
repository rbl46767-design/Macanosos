from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class Activity:
    id: str = field(default_factory=lambda: str(uuid4()))

    guild_id: int = 0
    channel_id: int = 0
    message_id: int = 0
    leader_id: int = 0

    title: str = ""
    description: str = ""
    scheduled_at: str | None = None

    is_closed: bool = False
    roles: list[dict[str, Any]] = field(default_factory=list)
    participants: list[dict[str, Any]] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    closed_at: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_id": self.message_id,
            "leader_id": self.leader_id,
            "title": self.title,
            "description": self.description,
            "scheduled_at": self.scheduled_at,
            "is_closed": self.is_closed,
            "roles": self.roles,
            "participants": self.participants,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Activity":
        return cls(
            id=data.get("id", str(uuid4())),
            guild_id=data.get("guild_id", 0),
            channel_id=data.get("channel_id", 0),
            message_id=data.get("message_id", 0),
            leader_id=data.get("leader_id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            scheduled_at=data.get("scheduled_at"),
            is_closed=data.get("is_closed", False),
            roles=data.get("roles", []),
            participants=data.get("participants", []),
            created_at=data.get(
                "created_at",
                datetime.utcnow().isoformat(),
            ),
            closed_at=data.get("closed_at"),
        )
