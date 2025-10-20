from typing import Optional
from uuid import UUID
from app.modules.refugio.domain.entities import Refugio, NewRefugio, UpdateRefugio
from app.modules.refugio.infrastructure.refugio_repository import RefugioRepository


class RefugioService:
    """Servicio de aplicación para la lógica de negocio de Refugios"""

    def __init__(self, repository: RefugioRepository):
        self.repository = repository

    async def obtener_todos(self) -> list[Refugio]:
        """Obtener todos los refugios"""
        return await self.repository.listar_refugios()

    async def obtener_refugio_por_id(self, id_refugio: UUID) -> Optional[Refugio]:
        """Obtener un refugio por ID"""
        return await self.repository.obtener_refugio_por_id(id_refugio)

    async def crear_refugio(self, nuevo_refugio: NewRefugio) -> Refugio:
        """Crear un nuevo refugio. Aquí validar reglas de negocio si es necesario."""
        return await self.repository.crear_refugio(nuevo_refugio)

    async def actualizar_refugio(self, refugio_actualizado: UpdateRefugio) -> Optional[Refugio]:
        """Actualizar un refugio existente"""
        return await self.repository.actualizar_refugio(refugio_actualizado)

    async def eliminar_refugio(self, id_refugio: UUID) -> bool:
        """Eliminar un refugio"""
        return await self.repository.eliminar_refugio(id_refugio)
