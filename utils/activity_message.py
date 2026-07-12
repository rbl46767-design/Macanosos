from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from utils.embed_builder import ActivityEmbedBuilder


class ActivityMessage:

    @staticmethod
    async def refresh(
        guild: discord.Guild,
        activity_id: str
    ) -> None:

        manager = ActivityManager()

        activity = manager.get(activity_id)

        if activity is None:

            return

        channel = guild.get_channel(
            activity.channel_id
        )

        if channel is None:

            return

        try:

            message = await channel.fetch_message(
                activity.message_id
            )

            await message.edit(

                embed=ActivityEmbedBuilder.build(
                    activity
                )

            )

        except discord.HTTPException:

            return