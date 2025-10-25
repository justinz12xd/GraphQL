from typing import List, Optional
from uuid import UUID
from app.modules.causa_urgente.domain.entities import CausaUrgente
from app.modules.causa_urgente.infrastructure.causa_urgente_repository import CausaUrgenteRepository

class CausaUrgenteService:
    def __init__(self, repo: CausaUrgenteRepository):
        self.repo = repo

    async def obtener_causas_urgentes(self) -> List[CausaUrgente]:
        return await self.repo.obtener_causas_urgentes()

    async def obtener_causa_urgente_por_id(self, id_causa_urgente: UUID) -> Optional[CausaUrgente]:
        return await self.repo.obtener_causa_urgente_por_id(id_causa_urgente)
        