from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RoleSlot:

    name: str

    emoji: str

    limit: int

    players: list[int] = field(default_factory=list)

    @property
    def current(self) -> int:
        return len(self.players)

    @property
    def available(self) -> int:
        return self.limit - len(self.players)

    def is_full(self) -> bool:
        return self.current >= self.limit

    def contains(self, user_id: int) -> bool:
        return user_id in self.players

    def add_player(self, user_id: int) -> bool:

        if self.contains(user_id):
            return False

        if self.is_full():
            return False

        self.players.append(user_id)

        return True

    def remove_player(self, user_id: int) -> bool:

        if user_id not in self.players:
            return False

        self.players.remove(user_id)

        return True

    def to_dict(self) -> dict:

        return {
            "name": self.name,
            "emoji": self.emoji,
            "limit": self.limit,
            "players": self.players
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RoleSlot":

        return cls(
            name=data["name"],
            emoji=data["emoji"],
            limit=data["limit"],
            players=data.get("players", [])
        )