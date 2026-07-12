from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from models.role_slot import RoleSlot
from utils.embed_builder import ActivityEmbedBuilder


class AddRoleModal(discord.ui.Modal, title="Agregar rol"):

    role_name = discord.ui.TextInput(
        label="Nombre",
        placeholder="Ej. Tank",
        max_length=30
    )

    emoji = discord.ui.TextInput(
        label="Emoji",
        placeholder="🛡️",
        max_length=10
    )

    slots = discord.ui.TextInput(
        label="Cantidad",
        placeholder="2",
        max_length=2
    )

    def __init__(self, activity_id: str):

        super().__init__()

        self.activity_id = activity_id

        self.manager = ActivityManager()

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        activity = self.manager.get(
            self.activity_id
        )

        if activity is None:

            await interaction.response.send_message(
                "Actividad inexistente.",
                ephemeral=True
            )

            return

        try:

            limit = int(str(self.slots))

        except ValueError:

            await interaction.response.send_message(
                "Cantidad inválida.",
                ephemeral=True
            )

            return

        activity.roles.append(

            RoleSlot(

                name=str(self.role_name),

                emoji=str(self.emoji),

                limit=limit

            ).to_dict()

        )

        self.manager.update(activity)

        channel = interaction.guild.get_channel(
            activity.channel_id
        )

        if channel:

            try:

                message = await channel.fetch_message(
                    activity.message_id
                )

                await message.edit(
                    embed=ActivityEmbedBuilder.build(activity)
                )

            except Exception:
                pass

        await interaction.response.send_message(
            "✅ Rol agregado correctamente.",
            ephemeral=True
        )