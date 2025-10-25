from typing import Optional
from uuid import UUID
from app.modules.supervisor.domain.entities import Supervisor
from app.modules.supervisor.infrastructure.supervisor_repository import SupervisorRepository

class SupervisorService:
    def __init__(self):
        self.repository = SupervisorRepository()

    async def listar_supervisores(self) -> list[Supervisor]:
        return await self.repository.listar_supervisores()

    async def obtener_supervisor_por_id(self, id_supervisor: UUID) -> Optional[Supervisor]:
        return await self.repository.obtener_supervisor_por_id(id_supervisor)