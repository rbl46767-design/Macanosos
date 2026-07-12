from __future__ import annotations

from datetime import datetime

from core.constants import DATA_DIR
from storage.json_storage import JsonStorage


class HistoryManager:

    def __init__(self):

        self.storage = JsonStorage(
            DATA_DIR / "history.json"
        )

    def save_activity(
        self,
        activity
    ):

        data = self.storage.load()

        data.setdefault(
            "activities",
            []
        )

        data["activities"].append(
            {
                "id": activity.id,
                "title": activity.title,
                "leader": activity.leader_id,
                "participants": activity.participants,
                "roles": activity.roles,
                "closed": activity.is_closed,
                "created_at": activity.created_at,
                "saved_at": datetime.utcnow().isoformat()
            }
        )

        self.storage.save(data)

    def save_payment(
        self,
        payment
    ):

        data = self.storage.load()

        data.setdefault(
            "payments",
            []
        )

        data["payments"].append(
            payment.to_dict()
        )

        self.storage.save(data)

    def activities(self):

        return self.storage.load().get(
            "activities",
            []
        )

    def payments(self):

        return self.storage.load().get(
            "payments",
            []
        )