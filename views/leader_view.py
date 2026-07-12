from __future__ import annotations

import discord

from managers.activity_manager import ActivityManager
from modals.add_role_modal import AddRoleModal
from modals.payment_modal import PaymentModal


class LeaderView(discord.ui.View):

    def __init__(
        self,
        activity_id: str
    ):

        super().__init__(
            timeout=300
        )

        self.activity_id = activity_id
        self.manager = ActivityManager()

    # --------------------------------------------------
    # Utilidades
    # --------------------------------------------------

    def activity(self):

        return self.manager.get(
            self.activity_id
        )

    async def leader_only(
        self,
        interaction: discord.Interaction
    ):

        activity = self.activity()

        if activity is None:

            await interaction.response.send_message(
                "❌ La actividad ya no existe.",
                ephemeral=True
            )

            return None

        if interaction.user.id != activity.leader_id:

            await interaction.response.send_message(
                "❌ Solo el líder puede usar este panel.",
                ephemeral=True
            )

            return None

        return activity

    async def refresh_activity(
        self,
        interaction: discord.Interaction
    ):

        """
        En las siguientes partes este método actualizará
        automáticamente el embed y los botones.

        Por ahora solamente recarga la actividad.
        """

        activity = self.activity()

        if activity is None:
            return

        return activity

    # --------------------------------------------------
    # Botón Agregar Rol
    # --------------------------------------------------

    @discord.ui.button(
        label="🎭 Agregar rol",
        style=discord.ButtonStyle.success,
        row=0
    )
    async def add_role(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(
            interaction
        )

        if activity is None:
            return

        await interaction.response.send_modal(
            AddRoleModal(
                activity.id
            )
        )

    # --------------------------------------------------
    # Botón Repartir
    # --------------------------------------------------

    @discord.ui.button(
        label="💰 Repartir",
        style=discord.ButtonStyle.success,
        row=0
    )
    async def payment(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(
            interaction
        )

        if activity is None:
            return

        if len(activity.participants) == 0:

            await interaction.response.send_message(
                "No existen participantes.",
                ephemeral=True
            )

            return

        await interaction.response.send_modal(
            PaymentModal(
                activity.id
            )
        )
            # --------------------------------------------------
    # Botón Eliminar Rol
    # --------------------------------------------------

    @discord.ui.button(
        label="🗑 Eliminar rol",
        style=discord.ButtonStyle.danger,
        row=0
    )
    async def remove_role(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(interaction)

        if activity is None:
            return

        if len(activity.roles) == 0:

            await interaction.response.send_message(
                "❌ No existen roles.",
                ephemeral=True
            )

            return

        options = []

        for role in activity.roles:

            options.append(

                discord.SelectOption(
                    label=role["name"],
                    emoji=role["emoji"],
                    value=role["name"]
                )

            )

        parent = self

        class RemoveRoleSelect(discord.ui.Select):

            def __init__(self):

                super().__init__(
                    placeholder="Selecciona un rol...",
                    min_values=1,
                    max_values=1,
                    options=options
                )

            async def callback(
                self,
                interaction: discord.Interaction
            ):

                activity = parent.activity()

                if activity is None:

                    await interaction.response.send_message(
                        "La actividad ya no existe.",
                        ephemeral=True
                    )

                    return

                parent.manager.remove_role(
                    activity,
                    self.values[0]
                )

                await interaction.response.edit_message(
                    content="✅ Rol eliminado correctamente.",
                    view=None
                )

        class RemoveRoleView(discord.ui.View):

            def __init__(self):

                super().__init__(timeout=180)

                self.add_item(
                    RemoveRoleSelect()
                )

        await interaction.response.send_message(
            "Selecciona el rol que deseas eliminar.",
            view=RemoveRoleView(),
            ephemeral=True
        )

    # --------------------------------------------------
    # Botón Agregar Jugador
    # --------------------------------------------------

    @discord.ui.button(
        label="➕ Agregar jugador",
        style=discord.ButtonStyle.primary,
        row=1,
        disabled=True
    )
    async def add_player(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🚧 Función disponible próximamente.",
            ephemeral=True
        )

    # --------------------------------------------------
    # Botón Quitar Jugador
    # --------------------------------------------------

    @discord.ui.button(
        label="➖ Quitar jugador",
        style=discord.ButtonStyle.primary,
        row=1,
        disabled=True
    )
    async def remove_player(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🚧 Función disponible próximamente.",
            ephemeral=True
        )
            # --------------------------------------------------
    # Botón Cerrar Actividad
    # --------------------------------------------------

    @discord.ui.button(
        label="🔒 Cerrar actividad",
        style=discord.ButtonStyle.secondary,
        row=2
    )
    async def close_activity(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(
            interaction
        )

        if activity is None:
            return

        if activity.is_closed:

            await interaction.response.send_message(
                "⚠️ La actividad ya está cerrada.",
                ephemeral=True
            )

            return

        self.manager.close(activity)

        await self.refresh_activity(
            interaction
        )

        await interaction.response.send_message(
            "🔒 Actividad cerrada correctamente.",
            ephemeral=True
        )

    # --------------------------------------------------
    # Botón Reabrir Actividad
    # --------------------------------------------------

    @discord.ui.button(
        label="🔓 Reabrir",
        style=discord.ButtonStyle.success,
        row=2
    )
    async def reopen_activity(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(
            interaction
        )

        if activity is None:
            return

        if not activity.is_closed:

            await interaction.response.send_message(
                "⚠️ La actividad ya está abierta.",
                ephemeral=True
            )

            return

        self.manager.reopen(activity)

        await self.refresh_activity(
            interaction
        )

        await interaction.response.send_message(
            "🟢 Actividad reabierta correctamente.",
            ephemeral=True
        )

    # --------------------------------------------------
    # Botón Eliminar Actividad
    # --------------------------------------------------

    @discord.ui.button(
        label="🗑 Eliminar actividad",
        style=discord.ButtonStyle.danger,
        row=3
    )
    async def delete_activity(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = await self.leader_only(
            interaction
        )

        if activity is None:
            return

        message = interaction.message

        self.manager.delete(
            activity.id
        )

        try:

            if message is not None:

                await message.delete()

        except discord.HTTPException:
            pass

        await interaction.response.send_message(
            "🗑 Actividad eliminada correctamente.",
            ephemeral=True
        )
            # --------------------------------------------------
    # Botón Cerrar Panel
    # --------------------------------------------------

    @discord.ui.button(
        label="❌ Cerrar panel",
        style=discord.ButtonStyle.secondary,
        row=3
    )
    async def close_panel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        activity = self.activity()

        if activity is None:

            await interaction.response.edit_message(
                content="La actividad ya no existe.",
                embed=None,
                view=None
            )

            return

        await interaction.response.edit_message(
            content="✅ Panel cerrado.",
            embed=None,
            view=None
        )

    # --------------------------------------------------
    # Utilidades futuras
    # --------------------------------------------------

    async def update_public_message(self):

        """
        Este método actualizará el embed público.

        En la Parte 5 quedará terminado para que
        cualquier cambio (roles, participantes,
        cerrar, reabrir, etc.) refresque el mismo
        mensaje automáticamente.
        """

        activity = self.activity()

        if activity is None:
            return False

        return True

    async def delete_public_message(
        self,
        interaction: discord.Interaction
    ):

        """
        En la Parte 5 este método eliminará
        el mensaje público utilizando:

            activity.channel_id
            activity.message_id

        evitando depender de interaction.message.
        """

        return True

    async def refresh_all(
        self,
        interaction: discord.Interaction
    ):

        """
        Método central.

        Todas las acciones del líder llamarán
        únicamente a este método para refrescar
        la actividad.

        Así evitaremos tener código duplicado
        en todos los botones.
        """

        await self.update_public_message()