from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import discord

from config import config
from core.exceptions import ActivityError
from managers.activity_manager import ActivityManager
from utils.embed_builder import ActivityEmbedBuilder
from views.activity_view import ActivityView


class CreateActivityModal(discord.ui.Modal, title="Crear actividad"):
    activity_name = discord.ui.TextInput(
        label="Nombre",
        placeholder="Ej. Ava Roads T8",
        required=True,
        max_length=100,
    )

    activity_description = discord.ui.TextInput(
        label="Descripción",
        style=discord.TextStyle.paragraph,
        placeholder="Describe la actividad...",
        required=False,
        max_length=500,
    )

    activity_date = discord.ui.TextInput(
        label="Fecha (DD/MM/AAAA)",
        placeholder="Ej. 25/12/2026",
        required=True,
        min_length=10,
        max_length=10,
    )

    activity_time = discord.ui.TextInput(
        label="Hora (formato 24 h)",
        placeholder="Ej. 20:30",
        required=True,
        min_length=5,
        max_length=5,
    )

    def __init__(self) -> None:
        super().__init__()
        self.manager = ActivityManager()

    def _scheduled_at(self) -> datetime:
        date_text = self.activity_date.value.strip()
        time_text = self.activity_time.value.strip()

        scheduled_at = datetime.strptime(
            f"{date_text} {time_text}",
            "%d/%m/%Y %H:%M",
        )

        return scheduled_at.replace(
            tzinfo=ZoneInfo(config.activity_timezone)
        )

    async def on_submit(
        self,
        interaction: discord.Interaction,
    ) -> None:
        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message(
                "Las actividades solo pueden crearse dentro de un servidor.",
                ephemeral=True,
            )
            return

        try:
            scheduled_at = self._scheduled_at()
        except ValueError:
            await interaction.response.send_message(
                "Usa una fecha válida DD/MM/AAAA y una hora válida HH:MM.",
                ephemeral=True,
            )
            return

        try:
            activity = self.manager.create(
                guild_id=interaction.guild.id,
                channel_id=interaction.channel.id,
                leader_id=interaction.user.id,
                title=self.activity_name.value,
                description=self.activity_description.value,
                scheduled_at=scheduled_at,
            )
        except ActivityError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        message = await interaction.channel.send(
            embed=ActivityEmbedBuilder.build(activity),
            view=ActivityView(),
        )

        activity.message_id = message.id
        self.manager.update(activity)

        await interaction.response.send_message(
            "✅ Actividad creada correctamente.",
            ephemeral=True,
        )
