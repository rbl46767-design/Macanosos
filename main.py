import discord
from discord.ext import commands
from discord import app_commands

import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

activities = {}


class ActivityView(discord.ui.View):
    def __init__(self, activity_id):
        super().__init__(timeout=None)
        self.activity_id = activity_id

    async def update_message(self, interaction):
        activity = activities[self.activity_id]

        embed = discord.Embed(
            title=f"📌 {activity['name']}",
            color=discord.Color.gold()
        )

        for role_name, data in activity["roles"].items():
            users = "\n".join(
                f"<@{u}>" for u in data["users"]
            ) or "Vacío"

            embed.add_field(
                name=f"{role_name} ({len(data['users'])}/{data['limit']})",
                value=users,
                inline=False
            )

        await interaction.message.edit(
            embed=embed,
            view=self
        )

    @discord.ui.button(label="Salir", style=discord.ButtonStyle.danger)
    async def leave_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        activity = activities[self.activity_id]

        for role_data in activity["roles"].values():
            if interaction.user.id in role_data["users"]:
                role_data["users"].remove(interaction.user.id)

        await self.update_message(interaction)

        await interaction.response.send_message(
            "Has salido de la actividad.",
            ephemeral=True
        )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Conectado como {bot.user}")


@bot.tree.command(name="actividad_crear")
@app_commands.describe(
    nombre="Nombre de la actividad",
    roles="Ej: Tank=1,Healer=2,DPS=5"
)
async def actividad_crear(
    interaction: discord.Interaction,
    nombre: str,
    roles: str
):

    activity_id = len(activities) + 1

    parsed_roles = {}

    for item in roles.split(","):
        role_name, limit = item.split("=")

        parsed_roles[role_name.strip()] = {
            "limit": int(limit),
            "users": []
        }

    activities[activity_id] = {
        "name": nombre,
        "creator": interaction.user.id,
        "roles": parsed_roles
    }

    embed = discord.Embed(
        title=f"📌 {nombre}",
        color=discord.Color.green()
    )

    view = ActivityView(activity_id)

    for role_name in parsed_roles:
        embed.add_field(
            name=f"{role_name} (0/{parsed_roles[role_name]['limit']})",
            value="Vacío",
            inline=False
        )

        async def role_callback(
            inter,
            role_name=role_name,
            activity_id=activity_id
        ):
            activity = activities[activity_id]

            # quitar usuario de cualquier otro rol
            for role_data in activity["roles"].values():
                if inter.user.id in role_data["users"]:
                    role_data["users"].remove(inter.user.id)

            role_data = activity["roles"][role_name]

            if len(role_data["users"]) >= role_data["limit"]:
                await inter.response.send_message(
                    "Ese rol está lleno.",
                    ephemeral=True
                )
                return

            role_data["users"].append(inter.user.id)

            await view.update_message(inter)

            await inter.response.send_message(
                f"Te uniste como {role_name}.",
                ephemeral=True
            )

        btn = discord.ui.Button(
            label=role_name,
            style=discord.ButtonStyle.primary
        )

        btn.callback = role_callback
        view.add_item(btn)

    await interaction.response.send_message(
        embed=embed,
        view=view
    )


@bot.tree.command(name="actividad_agregar")
@app_commands.describe(
    actividad_id="ID de la actividad",
    usuario="Usuario",
    rol="Rol"
)
async def actividad_agregar(
    interaction: discord.Interaction,
    actividad_id: int,
    usuario: discord.Member,
    rol: str
):

    if actividad_id not in activities:
        await interaction.response.send_message(
            "Actividad no encontrada.",
            ephemeral=True
        )
        return

    activity = activities[actividad_id]

    if activity["creator"] != interaction.user.id:
        await interaction.response.send_message(
            "Solo el creador puede agregar personas.",
            ephemeral=True
        )
        return

    if rol not in activity["roles"]:
        await interaction.response.send_message(
            "Rol inválido.",
            ephemeral=True
        )
        return

    role_data = activity["roles"][rol]

    if len(role_data["users"]) >= role_data["limit"]:
        await interaction.response.send_message(
            "Rol lleno.",
            ephemeral=True
        )
        return

    role_data["users"].append(usuario.id)

    await interaction.response.send_message(
        f"{usuario.mention} agregado a {rol}"
    )


@bot.tree.command(name="actividad_quitar")
@app_commands.describe(
    actividad_id="ID",
    usuario="Usuario"
)
async def actividad_quitar(
    interaction: discord.Interaction,
    actividad_id: int,
    usuario: discord.Member
):

    if actividad_id not in activities:
        await interaction.response.send_message(
            "Actividad no encontrada.",
            ephemeral=True
        )
        return

    activity = activities[actividad_id]
if activity.get("cerrada", False):
    await inter.response.send_message(
        "❌ Esta actividad está cerrada.",
        ephemeral=True
    )
    return
    if activity["creator"] != interaction.user.id:
        await interaction.response.send_message(
            "Solo el creador puede quitar personas.",
            ephemeral=True
        )
        return

    for role_data in activity["roles"].values():
        if usuario.id in role_data["users"]:
            role_data["users"].remove(usuario.id)

    await interaction.response.send_message(
        f"{usuario.mention} removido."
    )
@bot.tree.command(name="actividad_cerrar")
@app_commands.describe(
    actividad_id="ID de la actividad"
)
async def actividad_cerrar(
    interaction: discord.Interaction,
    actividad_id: int
):
    if actividad_id not in activities:
        await interaction.response.send_message(
            "Actividad no encontrada.",
            ephemeral=True
        )
        return

    activity = activities[actividad_id]

    if activity["creator"] != interaction.user.id:
        await interaction.response.send_message(
            "Solo el creador puede cerrar la actividad.",
            ephemeral=True
        )
        return

    activity["cerrada"] = True

    await interaction.response.send_message(
        f"✅ Actividad {actividad_id} cerrada."
    )


@bot.tree.command(name="actividad_eliminar")
@app_commands.describe(
    actividad_id="ID de la actividad"
)
async def actividad_eliminar(
    interaction: discord.Interaction,
    actividad_id: int
):
    if actividad_id not in activities:
        await interaction.response.send_message(
            "Actividad no encontrada.",
            ephemeral=True
        )
        return

    activity = activities[actividad_id]

    if activity["creator"] != interaction.user.id:
        await interaction.response.send_message(
            "Solo el creador puede eliminar la actividad.",
            ephemeral=True
        )
        return

    del activities[actividad_id]

    await interaction.response.send_message(
        "🗑️ Actividad eliminada."
    )


@bot.tree.command(name="actividad_repartir")
@app_commands.describe(
    actividad_id="ID de la actividad",
    monto="Cantidad de plata a repartir"
)
async def actividad_repartir(
    interaction: discord.Interaction,
    actividad_id: int,
    monto: int
):
    if actividad_id not in activities:
        await interaction.response.send_message(
            "Actividad no encontrada.",
            ephemeral=True
        )
        return

    activity = activities[actividad_id]

    participantes = set()

    for role_data in activity["roles"].values():
        participantes.update(role_data["users"])

    if len(participantes) == 0:
        await interaction.response.send_message(
            "No hay participantes.",
            ephemeral=True
        )
        return

    reparto = monto / len(participantes)

    await interaction.response.send_message(
        f"💰 Reparto total: {monto:,}\n"
        f"👥 Participantes: {len(participantes)}\n"
        f"💵 Cada uno recibe: {reparto:,.2f}"
    )

bot.run(TOKEN)
