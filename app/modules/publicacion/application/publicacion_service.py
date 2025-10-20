from typing import Optional
from uuid import UUID
from app.modules.publicacion.domain.entities import Publicacion, NewPublicacion, UpdatePublicacion
from app.modules.publicacion.infrastructure.publicacion_repository import PublicacionRepository


class PublicacionService:
    """Servicio de aplicación para la lógica de negocio de Publicaciones"""

    def __init__(self, repository: PublicacionRepository):
        self.repository = repository

    async def obtener_todas(self) -> list[Publicacion]:
        """Obtener todas las publicaciones"""
        return await self.repository.listar_publicaciones()

    async def obtener_publicacion_por_id(self, id_publicacion: UUID) -> Optional[Publicacion]:
        """Obtener una publicación por ID"""
        return await self.repository.obtener_publicacion_por_id(id_publicacion)

    async def crear_publicacion(self, nueva_publicacion: NewPublicacion) -> Publicacion:
        """Crear una nueva publicación

        Aquí es el lugar para validar reglas de negocio antes de delegar
        al repositorio (por ejemplo, longitud del título, contenido
        mínimo, permisos, etc.).
        """
        return await self.repository.crear_publicacion(nueva_publicacion)

    async def actualizar_publicacion(self, publicacion_actualizada: UpdatePublicacion) -> Optional[Publicacion]:
        """Actualizar una publicación existente"""
        return await self.repository.actualizar_publicacion(publicacion_actualizada)

    async def eliminar_publicacion(self, id_publicacion: UUID) -> bool:
        """Eliminar una publicación"""
        return await self.repository.eliminar_publicacion(id_publicacion)
