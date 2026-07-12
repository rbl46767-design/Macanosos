from __future__ import annotations

import json

from storage.base_storage import BaseStorage


class JsonStorage(BaseStorage):

    def load(self) -> dict:

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save(self, data: dict) -> None:

        with self.file_path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )