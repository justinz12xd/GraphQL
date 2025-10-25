from typing import List, Optional
from uuid import UUID
from app.modules.campania.domain.entitie import Campania
from app.modules.campania.infrastructure.campania_respository import CampaniaRepository

class CampaniaApplicationService:
    def __init__(self):
        self.repo = CampaniaRepository()

    async def obtener_campania(self, id_campania: UUID) -> Optional[Campania]:
        return await self.repo.obtener_campania_por_id(id_campania)

    async def listar_campanias(self, limit: int, offset: int) -> List[Campania]:
        return await self.repo.listar_campanias(limit, offset)