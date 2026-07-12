from __future__ import annotations

import discord

from models.activity import Activity


class ActivityEmbedBuilder:

    @staticmethod
    def build(activity: Activity) -> discord.Embed:

        embed = discord.Embed(
            title=f"⚔️ {activity.title}",
            description=activity.description or "*Sin descripción.*",
            color=discord.Color.blurple()
        )

        status = "🟢 Abierta"

        if activity.is_closed:
            status = "🔴 Cerrada"

        embed.add_field(
            name="👑 Líder",
            value=f"<@{activity.leader_id}>",
            inline=False
        )

        embed.add_field(
            name="📊 Estado",
            value=status,
            inline=True
        )

        embed.add_field(
            name="👥 Participantes",
            value=str(len(activity.participants)),
            inline=True
        )

        roles_text = ""

        if activity.roles:

            for role in activity.roles:

                players = role.get("players", [])

                mentions = ""

                if players:

                    mentions = "\n".join(
                        f"<@{player}>"
                        for player in players
                    )

                else:

                    mentions = "*Vacío*"

                roles_text += (
                    f"{role['emoji']} **{role['name']}** "
                    f"`{len(players)}/{role['limit']}`\n"
                    f"{mentions}\n\n"
                )

        else:

            roles_text = "*Todavía no existen roles.*"

        embed.add_field(
            name="🎭 Roles",
            value=roles_text,
            inline=False
        )

        embed.set_footer(
            text=f"Actividad ID: {activity.id}"
        )

        return embed