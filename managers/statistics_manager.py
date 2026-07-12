from __future__ import annotations

from core.constants import STATS_FILE
from storage.json_storage import JsonStorage


class StatisticsManager:

    def __init__(self):

        self.storage = JsonStorage(
            STATS_FILE
        )

    def add_activity(
        self,
        user_id: int
    ):

        data = self.storage.load()

        data.setdefault(
            str(user_id),
            {
                "activities": 0,
                "gold": 0,
                "roles": {}
            }
        )

        data[str(user_id)]["activities"] += 1

        self.storage.save(data)

    def add_gold(
        self,
        user_id: int,
        amount: int
    ):

        data = self.storage.load()

        data.setdefault(
            str(user_id),
            {
                "activities": 0,
                "gold": 0,
                "roles": {}
            }
        )

        data[str(user_id)]["gold"] += amount

        self.storage.save(data)

    def add_role(
        self,
        user_id: int,
        role: str
    ):

        data = self.storage.load()

        data.setdefault(
            str(user_id),
            {
                "activities": 0,
                "gold": 0,
                "roles": {}
            }
        )

        roles = data[str(user_id)]["roles"]

        roles.setdefault(
            role,
            0
        )

        roles[role] += 1

        self.storage.save(data)

    def get(
        self,
        user_id: int
    ):

        return self.storage.load().get(
            str(user_id),
            {
                "activities": 0,
                "gold": 0,
                "roles": {}
            }
        )