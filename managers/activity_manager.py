from __future__ import annotations

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
        description: str
    ) -> Activity:

        activity = Activity(
            guild_id=guild_id,
            channel_id=channel_id,
            leader_id=leader_id,
            title=title,
            description=description
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
        role: dict
    ):

        activity.roles.append(role)

        self.update(activity)

    def remove_role(
        self,
        activity: Activity,
        role_name: str
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
        role_name: str
    ):

        for role in activity.roles:

            if role["name"] == role_name:

                return role

        return None

    def user_role(
        self,
        activity: Activity,
        user_id: int
    ):

        for role in activity.roles:

            if user_id in role["players"]:

                return role

        return None

    def remove_user(
        self,
        activity: Activity,
        user_id: int
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
        activity: Activity
    ) -> int:

        return len(activity.participants)