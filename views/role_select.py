from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from utils.embed_builder import ActivityEmbedBuilder


class RoleSelect(discord.ui.Select):

    def __init__(self, activity_id: str):

        self.activity_id = activity_id
        self.manager = ActivityManager()

        activity = self.manager.get(activity_id)

        options = []

        if activity:

            for role in activity.roles:

                options.append(

                    discord.SelectOption(

                        label=role["name"],

                        emoji=role["emoji"],

                        description=f'{len(role["players"])}/{role["limit"]}',

                        value=role["name"]

                    )

                )

        super().__init__(

            placeholder="Selecciona un rol...",

            options=options,

            min_values=1,

            max_values=1

        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        activity = self.manager.get(self.activity_id)

        if activity is None:

            await interaction.response.send_message(
                "Actividad inexistente.",
                ephemeral=True
            )

            return

        selected = self.values[0]

        for role in activity.roles:

            if interaction.user.id in role["players"]:

                role["players"].remove(
                    interaction.user.id
                )

        destination = None

        for role in activity.roles:

            if role["name"] == selected:

                destination = role

                break

        if destination is None:

            await interaction.response.send_message(
                "Rol inválido.",
                ephemeral=True
            )

            return

        if len(destination["players"]) >= destination["limit"]:

            await interaction.response.send_message(
                "Ese rol ya está lleno.",
                ephemeral=True
            )

            return

        destination["players"].append(
            interaction.user.id
        )

        exists = False

        for player in activity.participants:

            if player["user_id"] == interaction.user.id:

                player["role_name"] = selected

                player["display_name"] = interaction.user.display_name

                exists = True

                break

        if not exists:

            activity.participants.append(
                {
                    "user_id": interaction.user.id,
                    "display_name": interaction.user.display_name,
                    "role_name": selected
                }
            )

        self.manager.update(activity)

        try:

            channel = interaction.guild.get_channel(
                activity.channel_id
            )

            message = await channel.fetch_message(
                activity.message_id
            )

            await message.edit(

                embed=ActivityEmbedBuilder.build(activity)

            )

        except Exception:

            pass

        await interaction.response.send_message(

            f"✅ Ahora perteneces al rol **{selected}**.",

            ephemeral=True

        )


class RoleSelectView(discord.ui.View):

    def __init__(self, activity_id: str):

        super().__init__(timeout=180)

        self.add_item(
            RoleSelect(activity_id)
        )