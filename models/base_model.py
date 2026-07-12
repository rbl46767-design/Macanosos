from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Clase base para todos los modelos del proyecto.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convierte el modelo en un diccionario serializable.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """
        Reconstruye un modelo desde un diccionario.
        """
        raise NotImplementedError