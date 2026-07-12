from __future__ import annotations

from datetime import datetime, timezone

from core.exceptions import ActivityError
from models.activity import Activity
from repositories.activity_repository import ActivityRepository


class ActivityManager:
    def __init__(self):
        self.repository = ActivityRepository()

    def create(
        self,
        guild_id: int,
        channel_id: int,
        leader_id: int,
        title: str,
        description: str,
        scheduled_at: datetime,
    ) -> Activity:
        clean_title = title.strip()
        clean_description = description.strip()

        if not clean_title:
            raise ActivityError("El nombre de la actividad es obligatorio.")

        if len(clean_title) > 100:
            raise ActivityError("El nombre no puede superar 100 caracteres.")

        if len(clean_description) > 500:
            raise ActivityError(
                "La descripción no puede superar 500 caracteres."
            )

        if guild_id <= 0 or channel_id <= 0 or leader_id <= 0:
            raise ActivityError(
                "La actividad debe crearse dentro de un servidor."
            )

        if (
            scheduled_at.tzinfo is None
            or scheduled_at.utcoffset() is None
        ):
            raise ActivityError(
                "La fecha y hora deben incluir una zona horaria válida."
            )

        activity = Activity(
            guild_id=guild_id,
            channel_id=channel_id,
            leader_id=leader_id,
            title=clean_title,
            description=clean_description,
            scheduled_at=scheduled_at.astimezone(timezone.utc).isoformat(),
        )

        self.repository.save(activity)

        return activity

    def get(self, activity_id: str):
        return self.repository.get(activity_id)

    def get_all(self):
        return self.repository.get_all()

    def update(self, activity: Activity):
        self.repository.update(activity)

    def delete(self, activity_id: str):
        self.repository.delete(activity_id)

    def close(self, activity: Activity):
        activity.is_closed = True
        self.update(activity)

    def reopen(self, activity: Activity):
        activity.is_closed = False
        self.update(activity)

    def add_role(
        self,
        activity: Activity,
        role: dict,
    ):
        activity.roles.append(role)
        self.update(activity)

    def remove_role(
        self,
        activity: Activity,
        role_name: str,
    ) -> bool:
        before = len(activity.roles)

        activity.roles = [
            role
            for role in activity.roles
            if role["name"] != role_name
        ]

        self.update(activity)

        return before != len(activity.roles)

    def get_role(
        self,
        activity: Activity,
        role_name: str,
    ):
        for role in activity.roles:
            if role["name"] == role_name:
                return role

        return None

    def user_role(
        self,
        activity: Activity,
        user_id: int,
    ):
        for role in activity.roles:
            if user_id in role["players"]:
                return role

        return None

    def remove_user(
        self,
        activity: Activity,
        user_id: int,
    ):
        for role in activity.roles:
            if user_id in role["players"]:
                role["players"].remove(user_id)

        activity.participants = [
            participant
            for participant in activity.participants
            if participant["user_id"] != user_id
        ]

        self.update(activity)

    def participant_count(
        self,
        activity: Activity,
    ) -> int:
        return len(activity.participants)
