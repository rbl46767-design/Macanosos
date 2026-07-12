from __future__ import annotations

import logging

import discord

from managers.activity_manager import ActivityManager
from managers.payment_manager import PaymentManager
from views.activity_view import ActivityView
from views.payment_view import PaymentView


class PersistentViews:

    @staticmethod
    async def register(bot: discord.Client):

        bot.add_view(ActivityView())
        bot.add_view(PaymentView())

        activity_manager = ActivityManager()
        payment_manager = PaymentManager()

        activities = activity_manager.get_all()
        payments = payment_manager.get_all()

        logging.info(
            "Actividades restauradas: %s",
            len(activities)
        )

        logging.info(
            "Repartos restaurados: %s",
            len(payments)
        )