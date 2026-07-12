from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True, frozen=True)
class Config:
    bot_token: str
    bot_prefix: str
    version: str
    debug: bool


def _to_bool(value: str | None) -> bool:
    if value is None:
        return False

    return value.lower() in (
        "1",
        "true",
        "yes",
        "on"
    )


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:
        raise RuntimeError(
            "No se encontró BOT_TOKEN dentro del archivo .env"
        )

    return Config(
        bot_token=token,
        bot_prefix=os.getenv("BOT_PREFIX", "!"),
        version="2.0.0",
        debug=_to_bool(os.getenv("DEBUG"))
    )


config = load_config()