from typing import Optional
from uuid import UUID
from app.modules.seguimiento.domain.entities import Seguimiento
from app.modules.seguimiento.infrastructure.seguimiento_repository import SeguimientoRepository


class SeguimientoService:
    """Servicio de aplicación para la lógica de negocio de Seguimiento"""

    def __init__(self, repository: SeguimientoRepository):
        self.repository = repository

    async def obtener_todos(self) -> list[Seguimiento]:
        """Obtener todos los seguimientos"""
        return await self.repository.listar_seguimientos()

    async def obtener_seguimiento_por_id(self, id_seguimiento: UUID) -> Optional[Seguimiento]:
        """Obtener un seguimiento por ID"""
        return await self.repository.obtener_seguimiento_por_id(id_seguimiento)
