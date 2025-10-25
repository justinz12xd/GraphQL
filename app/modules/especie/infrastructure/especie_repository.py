from typing import List, Optional
from app.modules.especie.domain.entities import Especie


class EspecieRepository:
    """Repositorio en memoria para gestionar entidades Especie en la aplicación."""

    def __init__(self):
        """Inicializar el almacenamiento en memoria para entidades Especie."""
        self._data = {}  # Diccionario interno: id -> Especie
        self._next = 1   # Contador auto-incremental de IDs

    def list_all(self) -> List[Especie]:
        """Devolver una lista de todas las especies almacenadas."""
        return list(self._data.values())

    def get_by_id(self, id_: int) -> Optional[Especie]:
        """Obtener una especie por su ID; devuelve None si no existe."""
        return self._data.get(id_)
