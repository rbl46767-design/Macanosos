from __future__ import annotations

from datetime import datetime, timezone

import discord

from models.activity import Activity


class ActivityEmbedBuilder:
    @staticmethod
    def build(activity: Activity) -> discord.Embed:
        embed = discord.Embed(
            title=f"⚔️ {activity.title}",
            description=activity.description or "*Sin descripción.*",
            color=discord.Color.blurple(),
        )

        status = "🟢 Abierta"

        if activity.is_closed:
            status = "🔴 Cerrada"

        embed.add_field(
            name="👑 Líder",
            value=f"<@{activity.leader_id}>",
            inline=False,
        )

        embed.add_field(
            name="📊 Estado",
            value=status,
            inline=True,
        )

        embed.add_field(
            name="👥 Participantes",
            value=str(len(activity.participants)),
            inline=True,
        )

        embed.add_field(
            name="🎭 Roles",
            value=ActivityEmbedBuilder._roles_text(activity),
            inline=False,
        )

        embed.add_field(
            name="🗓️ Fecha y hora",
            value=ActivityEmbedBuilder._schedule_text(activity),
            inline=False,
        )

        embed.set_footer(
            text=f"Actividad ID: {activity.id}",
        )

        return embed

    @staticmethod
    def _roles_text(activity: Activity) -> str:
        if not activity.roles:
            return "*Todavía no existen roles.*"

        roles_text = ""

        for role in activity.roles:
            players = role.get("players", [])

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

        return roles_text

    @staticmethod
    def _schedule_text(activity: Activity) -> str:
        if not activity.scheduled_at:
            return "*Sin programar.*"

        try:
            scheduled_at = datetime.fromisoformat(activity.scheduled_at)
        except ValueError:
            return "*Fecha guardada inválida.*"

        if scheduled_at.tzinfo is None:
            scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)

        timestamp = int(scheduled_at.timestamp())

        return f"<t:{timestamp}:F>\n<t:{timestamp}:R>"
