from __future__ import annotations

from storage.base_storage import BaseStorage


class BaseRepository:

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def load(self) -> dict:
        return self.storage.load()

    def save(self, data: dict) -> None:
        self.storage.save(data)