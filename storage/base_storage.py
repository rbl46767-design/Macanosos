from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseStorage(ABC):
    """
    Interfaz para cualquier sistema de almacenamiento.
    """

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @abstractmethod
    def load(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: dict) -> None:
        raise NotImplementedError