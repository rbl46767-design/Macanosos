from __future__ import annotations

import discord

from managers.payment_manager import PaymentManager


class PaymentView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.manager = PaymentManager()

    @discord.ui.button(
        label="✔ Cobrado",
        emoji="💰",
        style=discord.ButtonStyle.success,
        custom_id="payment_paid"
    )
    async def paid(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not interaction.message.embeds:

            await interaction.response.send_message(
                "No se encontró el reparto.",
                ephemeral=True
            )

            return

        payment_id = interaction.message.embeds[
            0
        ].footer.text

        payment = self.manager.get(
            payment_id
        )

        if payment is None:

            await interaction.response.send_message(
                "El reparto ya no existe.",
                ephemeral=True
            )

            return

        if interaction.user.id in payment.paid:

            await interaction.response.send_message(
                "Ya marcaste tu pago.",
                ephemeral=True
            )

            return

        payment.paid.append(
            interaction.user.id
        )

        self.manager.update(
            payment
        )

        embed = interaction.message.embeds[0]

        field = embed.fields[2]

        lines = field.value.split("\n")

        updated = []

        for line in lines:

            if f"<@{interaction.user.id}>" in line:

                line = line.replace(
                    "🟡 Pendiente",
                    "🟢 Pagado"
                )

            updated.append(line)

        embed.set_field_at(
            2,
            name="Estado",
            value="\n".join(updated),
            inline=False
        )

        await interaction.message.edit(
            embed=embed,
            view=self
        )

        await interaction.response.send_message(
            "Pago registrado correctamente.",
            ephemeral=True
        )