import strawberry
from typing import Optional, List
from uuid import UUID
from app.modules.voluntario.interface.graphql_type import VoluntarioType
from app.modules.voluntario.application.voluntario_service import VoluntarioService
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository

@strawberry.type
class VoluntarioQuery:
    """Queries GraphQL para Voluntario"""

    @strawberry.field
    async def voluntarios(self) -> List[VoluntarioType]:
        """Obtener todos los voluntarios"""
        service = VoluntarioService()
        voluntarios = await service.listar_voluntarios()
        return [VoluntarioType(
            id_voluntario=voluntario.id_voluntario,
            rol=voluntario.rol,
            estado=voluntario.estado,
            id_usuario=voluntario.id_usuario,
            id_campania=voluntario.id_campania) for voluntario in voluntarios]
    
    @strawberry.field
    async def voluntario_por_id(self, id_voluntario: strawberry.ID) -> Optional[VoluntarioType]:
        """Obtener un voluntario por ID"""
        service = VoluntarioService()
        voluntario = await service.obtener_voluntario_por_id(UUID(id_voluntario))
        if voluntario is None:
            return None
        return VoluntarioType(
            id_voluntario=voluntario.id_voluntario,
            rol=voluntario.rol,
            estado=voluntario.estado,
            id_usuario=voluntario.id_usuario,
            id_campania=voluntario.id_campania)
    
