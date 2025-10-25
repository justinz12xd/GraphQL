import strawberry
from typing import List, Optional
from app.modules.especie.interface.graphql_type import EspecieType
from app.modules.especie.application.especie_service import EspecieService
from app.modules.especie.infrastructure.especie_repository import EspecieRepository


@strawberry.type
class EspecieQuery:
    """GraphQL queries para Especie module."""
    
    @strawberry.field
    def especies(self) -> List[EspecieType]:
        """Obtener todas las especies"""
        repo = EspecieRepository()
        service = EspecieService(repo)
        especies = service.list_especies()
        return [EspecieType(id=esp.id, nombre=esp.nombre) for esp in especies]
    
    @strawberry.field
    def especie(self, id: int) -> Optional[EspecieType]:
        """Obtener una especie por ID"""
        repo = EspecieRepository()
        service = EspecieService(repo)
        especie = service.get_especie(id)
        if especie is None:
            return None
        return EspecieType(id=especie.id, nombre=especie.nombre)
