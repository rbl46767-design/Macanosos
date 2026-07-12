from __future__ import annotations

import json
import logging

from core.constants import (
    ACTIVITIES_FILE,
    PAYMENTS_FILE,
    STATS_FILE,
    LOGS_FILE,
    HISTORY_FILE,
)


class StartupManager:

    @staticmethod
    def initialize() -> None:

        files = [
            ACTIVITIES_FILE,
            PAYMENTS_FILE,
            STATS_FILE,
            LOGS_FILE,
            HISTORY_FILE,
        ]

        for file in files:

            if not file.exists():

                file.write_text(
                    "{}",
                    encoding="utf-8"
                )

                logging.info(
                    "Archivo creado: %s",
                    file.name
                )

                continue

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    json.load(f)

            except Exception:

                file.write_text(
                    "{}",
                    encoding="utf-8"
                )

                logging.warning(
                    "Archivo reparado: %s",
                    file.name
                )

        logging.info(
            "Proyecto inicializado correctamente."
        )