from __future__ import annotations

from datetime import datetime

from core.constants import LOGS_FILE
from storage.json_storage import JsonStorage


class LogManager:

    def __init__(self):

        self.storage = JsonStorage(LOGS_FILE)

    def add(
        self,
        event: str,
        user_id: int,
        activity_id: str,
        details: str = ""
    ) -> None:

        data = self.storage.load()

        data.setdefault(
            "logs",
            []
        )

        data["logs"].append(
            {
                "date": datetime.utcnow().isoformat(),
                "event": event,
                "user_id": user_id,
                "activity_id": activity_id,
                "details": details
            }
        )

        self.storage.save(data)

    def get_all(self):

        data = self.storage.load()

        return data.get(
            "logs",
            []
        )

    def activity_logs(
        self,
        activity_id: str
    ):

        return [

            log

            for log in self.get_all()

            if log["activity_id"] == activity_id

        ]