from __future__ import annotations

from core.constants import ACTIVITIES_FILE
from models.activity import Activity
from storage.json_storage import JsonStorage


class ActivityRepository:

    def __init__(self) -> None:
        self.storage = JsonStorage(ACTIVITIES_FILE)

    def get_all(self) -> list[Activity]:

        data = self.storage.load()

        activities: list[Activity] = []

        for activity_data in data.get("data", {}).values():
            activities.append(
                Activity.from_dict(activity_data)
            )

        return activities

    def get(self, activity_id: str) -> Activity | None:

        data = self.storage.load()

        activity_data = data.get("data", {}).get(activity_id)

        if activity_data is None:
            return None

        return Activity.from_dict(activity_data)

    def save(self, activity: Activity) -> None:

        data = self.storage.load()

        data.setdefault("data", {})

        data["data"][activity.id] = activity.to_dict()

        self.storage.save(data)

    def update(self, activity: Activity) -> None:

        self.save(activity)

    def delete(self, activity_id: str) -> None:

        data = self.storage.load()

        if activity_id in data.get("data", {}):
            del data["data"][activity_id]

        self.storage.save(data)