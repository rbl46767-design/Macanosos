from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from managers.statistics_manager import StatisticsManager


class StatisticsCommand(commands.Cog):

    def __init__(
        self,
        bot: commands.Bot
    ):

        self.bot = bot

        self.manager = StatisticsManager()

    @app_commands.command(
        name="estadisticas",
        description="Ver estadísticas de un jugador."
    )
    async def statistics(

        self,

        interaction: discord.Interaction,

        usuario: discord.Member | None = None

    ):

        member = usuario or interaction.user

        stats = self.manager.get(
            member.id
        )

        embed = discord.Embed(

            title=f"📊 Estadísticas de {member.display_name}",

            color=discord.Color.blurple()

        )

        embed.add_field(

            name="⚔ Actividades",

            value=str(stats["activities"]),

            inline=True

        )

        embed.add_field(

            name="💰 Oro recibido",

            value=f'{stats["gold"]:,}',

            inline=True

        )

        roles = stats["roles"]

        if roles:

            text = "\n".join(

                f"• {name}: {count}"

                for name, count in roles.items()

            )

        else:

            text = "Sin datos."

        embed.add_field(

            name="🎭 Roles",

            value=text,

            inline=False

        )

        await interaction.response.send_message(

            embed=embed

        )


async def setup(bot):

    await bot.add_cog(

        StatisticsCommand(bot)

    )