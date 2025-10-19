from typing import List, Optional
from uuid import UUID
from app.modules.causa_urgente.domain.entities import CausaUrgente, NewCausaUrgente, UpdateCausaUrgente
from app.modules.causa_urgente.infrastructure.causa_urgente_repository import CausaUrgenteRepository

class CausaUrgenteService:
    def __init__(self, repo: CausaUrgenteRepository):
        self.repo = repo

    async def obtener_causas_urgentes(self) -> List[CausaUrgente]:
        return await self.repo.obtener_causas_urgentes()

    async def obtener_causa_urgente_por_id(self, id_causa_urgente: UUID) -> Optional[CausaUrgente]:
        return await self.repo.obtener_causa_urgente_por_id(id_causa_urgente)

    async def crear_causa_urgente(self, nueva_causa_urgente: NewCausaUrgente) -> CausaUrgente:
        return await self.repo.crear_causa_urgente(nueva_causa_urgente)

    async def actualizar_causa_urgente(self, id_causa_urgente: UUID, causa_urgente_actualizada: UpdateCausaUrgente) -> Optional[CausaUrgente]:
        return await self.repo.actualizar_causa_urgente(id_causa_urgente, causa_urgente_actualizada)

    async def eliminar_causa_urgente(self, id_causa_urgente: UUID) -> bool:
        return await self.repo.eliminar_causa_urgente(id_causa_urgente)
        