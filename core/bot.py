from __future__ import annotations

import logging

import discord
from discord.ext import commands

from config import config
from storage.persistent_views import PersistentViews


class BotClient(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()

        intents.guilds = True
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix=config.bot_prefix,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):

        logging.info("Registrando vistas persistentes...")

        await PersistentViews.register(self)

        logging.info("Cargando comandos...")

        await self.load_extension(
            "commands.activity"
        )
        
        await self.load_extension(
        "commands.stats"
         )
        
        await self.load_extension(
        "commands.history"
         )
        await self.load_extension(
        "commands.ping"
          )
        logging.info("Sincronizando comandos...")

        await self.tree.sync()

        logging.info("Inicialización completada.")


    async def on_ready(self):

        logging.info("Bot conectado.")

        print("=" * 60)
        print("Macanosos V2")
        print(f"Usuario : {self.user}")
        print(f"ID      : {self.user.id}")
        print("=" * 60)