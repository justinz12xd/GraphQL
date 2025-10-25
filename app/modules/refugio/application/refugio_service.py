from typing import Optional
from uuid import UUID
from app.modules.refugio.domain.entities import Refugio
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
