from typing import List, Optional
from uuid import UUID
from app.modules.campania.domain.entitie import Campania, NewCampania, UpdateCampania
from app.modules.campania.infrastructure.campania_respository import CampaniaRepository

class CampaniaApplicationService:
    def __init__(self):
        self.repo = CampaniaRepository()

    async def obtener_campania(self, id_campania: UUID) -> Optional[Campania]:
        return await self.repo.obtener_campania_por_id(id_campania)

    async def listar_campanias(self, limit: int, offset: int) -> List[Campania]:
        return await self.repo.listar_campanias(limit, offset)

    async def crear_campania(self, nueva_campania: NewCampania) -> Campania:
        return await self.repo.crear_campania(nueva_campania)

    async def actualizar_campania(self, id_campania: UUID, campania_actualizada: UpdateCampania) -> Optional[Campania]:
        return await self.repo.actualizar_campania(id_campania, campania_actualizada)

    async def eliminar_campania(self, id_campania: UUID) -> bool:
        return await self.repo.eliminar_campania(id_campania)