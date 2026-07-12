from __future__ import annotations

import asyncio

from config import config
from core.bot import BotClient
from core.logger import setup_logger
from core.startup import StartupManager


async def main() -> None:
    setup_logger()

    StartupManager.initialize()

    bot = BotClient()

    async with bot:
        await bot.start(config.bot_token)


if __name__ == "__main__":
    asyncio.run(main())