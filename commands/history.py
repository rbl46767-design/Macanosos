from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from managers.history_manager import HistoryManager


class HistoryCommand(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

        self.manager = HistoryManager()

    @app_commands.command(
        name="historial",
        description="Muestra las últimas actividades."
    )
    async def history(
        self,
        interaction: discord.Interaction
    ):

        activities = self.manager.activities()

        embed = discord.Embed(

            title="📜 Historial",

            color=discord.Color.blurple()

        )

        if not activities:

            embed.description = "No existe historial."

        else:

            text = ""

            for activity in activities[-10:]:

                text += (
                    f"⚔ **{activity['title']}**\n"
                    f"👑 <@{activity['leader']}>\n"
                    f"👥 {len(activity['participants'])} jugadores\n\n"
                )

            embed.description = text

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        HistoryCommand(bot)
    )