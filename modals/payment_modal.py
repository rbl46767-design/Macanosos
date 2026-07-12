from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from managers.payment_manager import PaymentManager
from views.payment_view import PaymentView


class PaymentModal(discord.ui.Modal, title="Repartir plata"):

    total = discord.ui.TextInput(
        label="Cantidad total",
        placeholder="Ej. 12000000"
    )

    channel_id = discord.ui.TextInput(
        label="ID del canal",
        placeholder="Pega aquí el ID del canal"
    )

    def __init__(self, activity_id: str):

        super().__init__()

        self.activity_id = activity_id

        self.activity_manager = ActivityManager()

        self.payment_manager = PaymentManager()

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        activity = self.activity_manager.get(
            self.activity_id
        )

        if activity is None:

            await interaction.response.send_message(
                "Actividad inexistente.",
                ephemeral=True
            )

            return

        if len(activity.participants) == 0:

            await interaction.response.send_message(
                "No hay participantes.",
                ephemeral=True
            )

            return

        try:

            total = int(str(self.total))
            channel_id = int(str(self.channel_id))

        except ValueError:

            await interaction.response.send_message(
                "Datos inválidos.",
                ephemeral=True
            )

            return

        channel = interaction.guild.get_channel(channel_id)

        if channel is None:

            await interaction.response.send_message(
                "No se encontró el canal.",
                ephemeral=True
            )

            return

        payment = self.payment_manager.create(
            activity_id=activity.id,
            guild_id=interaction.guild.id,
            channel_id=channel.id,
            total=total,
            members=len(activity.participants),
            created_by=interaction.user.id
        )

        description = ""

        mentions = []

        for participant in activity.participants:

            mentions.append(
                f"<@{participant['user_id']}>"
            )

            description += (
                f"<@{participant['user_id']}> — 🟡 Pendiente\n"
            )

        embed = discord.Embed(
            title="💰 Reparto",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Total",
            value=f"{payment.total:,}",
            inline=True
        )

        embed.add_field(
            name="Cada jugador",
            value=f"{payment.each:,}",
            inline=True
        )

        embed.add_field(
            name="Estado",
            value=description,
            inline=False
        )

        embed.set_footer(
            text=payment.id
        )

        message = await channel.send(
            " ".join(mentions),
            embed=embed,
            view=PaymentView()
        )

        payment.message_id = message.id

        self.payment_manager.update(payment)

        await interaction.response.send_message(
            "✅ Reparto creado correctamente.",
            ephemeral=True
        )