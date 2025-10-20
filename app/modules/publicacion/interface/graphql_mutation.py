import strawberry
from typing import Optional
from uuid import UUID
from app.modules.publicacion.interface.graphql_type import PublicacionType, CreatePublicacionInput, UpdatePublicacionInput
from app.modules.publicacion.application.publicacion_service import PublicacionService
from app.modules.publicacion.infrastructure.publicacion_repository import PublicacionRepository
from app.modules.publicacion.domain.entities import NewPublicacion, UpdatePublicacion


@strawberry.type
class PublicacionMutation:
    """Mutations GraphQL para Publicacion"""

    @strawberry.mutation
    async def crear_publicacion(self, input: CreatePublicacionInput) -> PublicacionType:
        """Crear una nueva publicación"""
        adapter = PublicacionRepository()
        service = PublicacionService(adapter)

        nueva_publicacion = NewPublicacion(
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_publicacion=input.fecha_publicacion,
            estado=input.estado,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None,
        )

        publicacion = await service.crear_publicacion(nueva_publicacion)

        return PublicacionType(
            id_publicacion=strawberry.ID(str(publicacion.id_publicacion)),
            titulo=publicacion.titulo,
            descripcion=publicacion.descripcion,
            fecha_publicacion=publicacion.fecha_publicacion,
            estado=publicacion.estado,
            id_usuario=strawberry.ID(str(publicacion.id_usuario)) if publicacion.id_usuario else None,
        )

    @strawberry.mutation
    async def actualizar_publicacion(self, input: UpdatePublicacionInput) -> Optional[PublicacionType]:
        """Actualizar una publicación existente"""
        adapter = PublicacionRepository()
        service = PublicacionService(adapter)

        publicacion_actualizada = UpdatePublicacion(
            id_publicacion=UUID(input.id_publicacion),
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_publicacion=input.fecha_publicacion,
            estado=input.estado,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None,
        )

        publicacion = await service.actualizar_publicacion(publicacion_actualizada)

        if publicacion is None:
            return None

        return PublicacionType(
            id_publicacion=strawberry.ID(str(publicacion.id_publicacion)),
            titulo=publicacion.titulo,
            descripcion=publicacion.descripcion,
            fecha_publicacion=publicacion.fecha_publicacion,
            estado=publicacion.estado,
            id_usuario=strawberry.ID(str(publicacion.id_usuario)) if publicacion.id_usuario else None,
        )

    @strawberry.mutation
    async def eliminar_publicacion(self, id_publicacion: strawberry.ID) -> bool:
        """Eliminar una publicación"""
        adapter = PublicacionRepository()
        service = PublicacionService(adapter)

        return await service.eliminar_publicacion(UUID(id_publicacion))
