from typing import Optional
from uuid import UUID
from app.modules.publicacion.domain.entities import Publicacion
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
