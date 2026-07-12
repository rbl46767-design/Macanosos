from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Participant:

    user_id: int

    display_name: str

    role_name: str

    joined_at: str = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:

        return {
            "user_id": self.user_id,
            "display_name": self.display_name,
            "role_name": self.role_name,
            "joined_at": self.joined_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Participant":

        return cls(
            user_id=data["user_id"],
            display_name=data["display_name"],
            role_name=data["role_name"],
            joined_at=data["joined_at"]
        )