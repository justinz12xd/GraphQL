import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.adopcion.interface.graphql_type import AdopcionType
from app.modules.adopcion.application.adopcion_service import AdopcionService
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository


@strawberry.type
class AdopcionQuery:
    """Queries GraphQL para Adopción"""
    
    @strawberry.field
    async def adopciones(self) -> List[AdopcionType]:
        """Obtener todas las adopciones"""
        adapter = AdopcionRepository()
        service = AdopcionService(adapter)
        adopciones = await service.obtener_todas()
        
        return [
            AdopcionType(
                id_adopcion=strawberry.ID(str(adopcion.id_adopcion)),
                fecha_adopcion=adopcion.fecha_adopcion,
                estado=adopcion.estado,
                id_publicacion=strawberry.ID(str(adopcion.id_publicacion)) if adopcion.id_publicacion else None,
                id_usuario=strawberry.ID(str(adopcion.id_usuario)) if adopcion.id_usuario else None
            )
            for adopcion in adopciones
        ]
    
    @strawberry.field
    async def adopcion(self, id_adopcion: strawberry.ID) -> Optional[AdopcionType]:
        """Obtener una adopción por ID"""
        adapter = AdopcionRepository()
        service = AdopcionService(adapter)
        adopcion = await service.obtener_adopcion_por_id(UUID(id_adopcion))
        
        if adopcion is None:
            return None
        
        return AdopcionType(
            id_adopcion=strawberry.ID(str(adopcion.id_adopcion)),
            fecha_adopcion=adopcion.fecha_adopcion,
            estado=adopcion.estado,
            id_publicacion=strawberry.ID(str(adopcion.id_publicacion)) if adopcion.id_publicacion else None,
            id_usuario=strawberry.ID(str(adopcion.id_usuario)) if adopcion.id_usuario else None
        )
