from __future__ import annotations

import logging

from core.constants import LOG_FILE


def setup_logger() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )

    logging.info(
        "Proyecto inicializado correctamente."
    )