import strawberry
from typing import Optional
from uuid import UUID
from app.modules.adopcion.interface.graphql_type import AdopcionType, CreateAdopcionInput, UpdateAdopcionInput
from app.modules.adopcion.application.adopcion_service import AdopcionService
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository
from app.modules.adopcion.domain.entities import NewAdopcion, UpdateAdopcion


@strawberry.type
class AdopcionMutation:
    """Mutations GraphQL para Adopción"""
    
    @strawberry.mutation
    async def crear_adopcion(self, input: CreateAdopcionInput) -> AdopcionType:
        """Crear una nueva adopción"""
        adapter = AdopcionRepository()
        service = AdopcionService(adapter)
        
        nueva_adopcion = NewAdopcion(
            fecha_adopcion=input.fecha_adopcion,
            estado=input.estado,
            id_publicacion=UUID(input.id_publicacion) if input.id_publicacion else None,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None
        )
        
        adopcion = await service.crear_adopcion(nueva_adopcion)
        
        return AdopcionType(
            id_adopcion=strawberry.ID(str(adopcion.id_adopcion)),
            fecha_adopcion=adopcion.fecha_adopcion,
            estado=adopcion.estado,
            id_publicacion=strawberry.ID(str(adopcion.id_publicacion)) if adopcion.id_publicacion else None,
            id_usuario=strawberry.ID(str(adopcion.id_usuario)) if adopcion.id_usuario else None
        )
    
    @strawberry.mutation
    async def actualizar_adopcion(self, input: UpdateAdopcionInput) -> Optional[AdopcionType]:
        """Actualizar una adopción existente"""
        adapter = AdopcionRepository()
        service = AdopcionService(adapter)
        
        adopcion_actualizada = UpdateAdopcion(
            id_adopcion=UUID(input.id_adopcion),
            fecha_adopcion=input.fecha_adopcion,
            estado=input.estado,
            id_publicacion=UUID(input.id_publicacion) if input.id_publicacion else None,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None
        )
        
        adopcion = await service.actualizar_adopcion(adopcion_actualizada)
        
        if adopcion is None:
            return None
        
        return AdopcionType(
            id_adopcion=strawberry.ID(str(adopcion.id_adopcion)),
            fecha_adopcion=adopcion.fecha_adopcion,
            estado=adopcion.estado,
            id_publicacion=strawberry.ID(str(adopcion.id_publicacion)) if adopcion.id_publicacion else None,
            id_usuario=strawberry.ID(str(adopcion.id_usuario)) if adopcion.id_usuario else None
        )
    
    @strawberry.mutation
    async def eliminar_adopcion(self, id_adopcion: strawberry.ID) -> bool:
        """Eliminar una adopción"""
        adapter = AdopcionRepository()
        service = AdopcionService(adapter)
        
        return await service.eliminar_adopcion(UUID(id_adopcion))
