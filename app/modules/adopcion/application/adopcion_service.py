from typing import Optional
from uuid import UUID
from app.modules.adopcion.domain.entities import Adopcion
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository


class AdopcionService:
    """Servicio de aplicación para la lógica de negocio de Adopciones"""
    
    def __init__(self, repository: AdopcionRepository):
        self.repository = repository
    
    async def obtener_todas(self) -> list[Adopcion]:
        """Obtener todas las adopciones"""
        return await self.repository.listar_adopciones()
    
    async def obtener_adopcion_por_id(self, id_adopcion: UUID) -> Optional[Adopcion]:
        """Obtener una adopción por ID"""
        return await self.repository.obtener_adopcion_por_id(id_adopcion)
