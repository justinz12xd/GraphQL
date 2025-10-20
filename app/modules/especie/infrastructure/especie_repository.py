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

    def save(self, especie: Especie) -> Especie:
        """Guardar una nueva especie o actualizar una existente.
        Si no tiene un ID asignado, genera uno auto-incremental."""
        if especie.id is None:
            especie.id = self._next
            self._next += 1
        self._data[especie.id] = especie  # Insertar o actualizar entidad
        return especie

    def delete(self, id_: int) -> bool:
        """Eliminar una especie por su ID.
        Devuelve True si la eliminación fue exitosa, False en caso contrario."""
        return self._data.pop(id_, None) is not None
