import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.publicacion.interface.graphql_type import PublicacionType
from app.modules.publicacion.application.publicacion_service import PublicacionService
from app.modules.publicacion.infrastructure.publicacion_repository import PublicacionRepository


@strawberry.type
class PublicacionQuery:
    """Queries GraphQL para Publicacion"""

    @strawberry.field
    async def publicaciones(self) -> List[PublicacionType]:
        """Obtener todas las publicaciones"""
        adapter = PublicacionRepository()
        service = PublicacionService(adapter)
        publicaciones = await service.obtener_todas()

        return [
            PublicacionType(
                id_publicacion=strawberry.ID(str(pub.id_publicacion)),
                titulo=pub.titulo,
                descripcion=pub.descripcion,
                fecha_publicacion=pub.fecha_publicacion,
                estado=pub.estado,
                id_usuario=strawberry.ID(str(pub.id_usuario)) if pub.id_usuario else None,
            )
            for pub in publicaciones
        ]

    @strawberry.field
    async def publicacion(self, id_publicacion: strawberry.ID) -> Optional[PublicacionType]:
        """Obtener una publicación por ID"""
        adapter = PublicacionRepository()
        service = PublicacionService(adapter)
        publicacion = await service.obtener_publicacion_por_id(UUID(id_publicacion))

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
