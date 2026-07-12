from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

ACTIVITIES_FILE = DATA_DIR / "activities.json"
PAYMENTS_FILE = DATA_DIR / "payments.json"
STATS_FILE = DATA_DIR / "stats.json"
LOGS_FILE = DATA_DIR / "logs.json"
HISTORY_FILE = DATA_DIR / "history.json"

LOG_FILE = LOGS_DIR / "bot.log"