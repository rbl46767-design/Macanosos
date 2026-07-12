from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from views.activity_view import ActivityView


class CreateActivityModal(discord.ui.Modal, title="Crear actividad"):

    activity_name = discord.ui.TextInput(
        label="Nombre",
        placeholder="Ej. Ava Roads T8",
        required=True,
        max_length=100
    )

    activity_description = discord.ui.TextInput(
        label="Descripción",
        style=discord.TextStyle.paragraph,
        placeholder="Describe la actividad...",
        required=False,
        max_length=500
    )

    def __init__(self) -> None:
        super().__init__()
        self.manager = ActivityManager()

    async def on_submit(
        self,
        interaction: discord.Interaction
    ) -> None:

        activity = self.manager.create(
            guild_id=interaction.guild.id,
            channel_id=interaction.channel.id,
            leader_id=interaction.user.id,
            title=str(self.activity_name),
            description=str(self.activity_description)
        )

        embed = discord.Embed(
            title=f"⚔️ {activity.title}",
            description=activity.description or "*Sin descripción*",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="👑 Líder",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="📊 Estado",
            value="🟢 Abierta",
            inline=True
        )

        embed.add_field(
            name="👥 Participantes",
            value="0",
            inline=True
        )

        embed.add_field(
            name="🎭 Roles",
            value="Aún no hay roles.",
            inline=False
        )

        embed.set_footer(
            text=f"Actividad ID: {activity.id}"
        )

        message = await interaction.channel.send(
            embed=embed,
            view=ActivityView()
        )

        activity.message_id = message.id

        self.manager.update(activity)

        await interaction.response.send_message(
            "✅ Actividad creada correctamente.",
            ephemeral=True
        )