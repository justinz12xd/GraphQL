from typing import List, Optional
from app.modules.especie.domain.entities import Especie


class EspecieService:
    """Capa de servicio para el módulo Especie."""

    def __init__(self, repo):
        self.repo = repo

    def list_especies(self) -> List[Especie]:
        """Obtener y devolver todas las especies mediante el repositorio."""
        return self.repo.list_all()

    def get_especie(self, especie_id: int) -> Optional[Especie]:
        """Obtener una especie específica según su ID."""
        return self.repo.get_by_id(especie_id)

    def create_especie(self, name: str) -> Especie:
        """Crear y persistir una nueva especie con el nombre dado."""
        entidad = Especie(id=None, nombre=name)
        return self.repo.save(entidad)
