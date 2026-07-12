from __future__ import annotations

from discord import app_commands
from discord.ext import commands

from modals.create_activity_modal import CreateActivityModal


class ActivityCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @app_commands.command(
        name="actividad",
        description="Crear una nueva actividad."
    )
    async def activity(
        self,
        interaction
    ):

        await interaction.response.send_modal(
            CreateActivityModal()
        )


async def setup(bot: commands.Bot):

    await bot.add_cog(
        ActivityCommand(bot)
    )