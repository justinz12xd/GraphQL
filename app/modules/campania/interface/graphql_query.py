import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.campania.interface.graphql_type import CampaniaType
from app.modules.campania.application.campania_service import CampaniaApplicationService
from app.modules.campania.infrastructure.campania_respository import CampaniaRepository

@strawberry.type
class CampaniaQuery:
    """Queries relacionadas con campañas"""

    @strawberry.field
    async def obtener_campania_id(self, id_campania: strawberry.ID) -> Optional[CampaniaType]:
        """Obtener una campaña por su ID"""
        service = CampaniaApplicationService()
        campania = await service.obtener_campania(UUID(id_campania))

        if campania is None:
            return None
            
        return CampaniaType(
            id_campania=campania.id_campania,
            id_tipo_campania=campania.id_tipo_campania,
            titulo=campania.titulo,
            descripcion=campania.descripcion,
            fecha_inicio=campania.fecha_inicio,
            fecha_fin=campania.fecha_fin,
            lugar=campania.lugar,
            organizador=campania.organizador,
            estado=campania.estado
        )

    @strawberry.field
    async def listar_campanias(self, limit: int = 50, offset: int = 0) -> List[CampaniaType]:
        """Listar todas las campañas con paginación"""
        service = CampaniaApplicationService()
        campanias = await service.listar_campanias(limit=limit, offset=offset)

        return [
            CampaniaType(
                id_campania=campania.id_campania,
                id_tipo_campania=campania.id_tipo_campania,
                titulo=campania.titulo,
                descripcion=campania.descripcion,
                fecha_inicio=campania.fecha_inicio,
                fecha_fin=campania.fecha_fin,
                lugar=campania.lugar,
                organizador=campania.organizador,
                estado=campania.estado
            )
            for campania in campanias
        ]
    
