from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from views.leader_view import LeaderView
from views.role_select import RoleSelectView


class ActivityView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

        self.manager = ActivityManager()

    def get_activity(
        self,
        interaction: discord.Interaction
    ):

        if not interaction.message.embeds:

            return None

        footer = interaction.message.embeds[0].footer.text

        if footer is None:

            return None

        activity_id = footer.replace(
            "Actividad ID: ",
            ""
        )

        return self.manager.get(
            activity_id
        )

    @discord.ui.button(
        label="➕ Unirse",
        style=discord.ButtonStyle.success,
        custom_id="activity_join"
    )
    async def join_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = self.get_activity(
            interaction
        )

        if activity is None:

            await interaction.response.send_message(
                "La actividad no existe.",
                ephemeral=True
            )

            return

        if activity.is_closed:

            await interaction.response.send_message(
                "La actividad ya fue cerrada.",
                ephemeral=True
            )

            return

        if len(activity.roles) == 0:

            await interaction.response.send_message(
                "El líder todavía no ha creado roles.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "Selecciona el rol que deseas ocupar.",
            view=RoleSelectView(
                activity.id
            ),
            ephemeral=True
        )

    @discord.ui.button(
        label="➖ Salir",
        style=discord.ButtonStyle.secondary,
        custom_id="activity_leave"
    )
    async def leave_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = self.get_activity(
            interaction
        )

        if activity is None:

            await interaction.response.send_message(
                "Actividad inexistente.",
                ephemeral=True
            )

            return

        removed = False

        for role in activity.roles:

            if interaction.user.id in role["players"]:

                role["players"].remove(
                    interaction.user.id
                )

                removed = True

        activity.participants = [

            player

            for player in activity.participants

            if player["user_id"] != interaction.user.id

        ]

        self.manager.update(
            activity
        )

        if removed:

            embed = interaction.message.embeds[0]

            text = ""

            for role in activity.roles:

                text += (
                    f"{role['emoji']} "
                    f"**{role['name']}** "
                    f"({len(role['players'])}/{role['limit']})\n"
                )

            if text == "":
                text = "No hay roles."

            embed.set_field_at(
                3,
                name="🎭 Roles",
                value=text,
                inline=False
            )

            await interaction.message.edit(
                embed=embed,
                view=self
            )

        await interaction.response.send_message(
            "Has salido de la actividad.",
            ephemeral=True
        )

    @discord.ui.button(
        label="👑 Panel",
        style=discord.ButtonStyle.primary,
        custom_id="activity_panel"
    )
    async def leader_panel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = self.get_activity(
            interaction
        )

        if activity is None:

            await interaction.response.send_message(
                "Actividad inexistente.",
                ephemeral=True
            )

            return

        if interaction.user.id != activity.leader_id:

            await interaction.response.send_message(
                "Solo el líder puede abrir este panel.",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="👑 Panel del Líder",
            description="Selecciona una opción.",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(
            embed=embed,
            view=LeaderView(
                activity.id
            ),
            ephemeral=True
        )