from typing import Optional
from uuid import UUID
from app.modules.supervisor.domain.entities import Supervisor, NewSupervisor, UpdateSupervisor
from app.modules.supervisor.infrastructure.supervisor_repository import SupervisorRepository

class SupervisorService:
    def __init__(self):
        self.repository = SupervisorRepository()

    async def listar_supervisores(self) -> list[Supervisor]:
        return await self.repository.listar_supervisores()

    async def obtener_supervisor_por_id(self, id_supervisor: UUID) -> Optional[Supervisor]:
        return await self.repository.obtener_supervisor_por_id(id_supervisor)

    async def crear_supervisor(self, nuevo_supervisor: NewSupervisor) -> Supervisor:
        return await self.repository.crear_supervisor(nuevo_supervisor)

    async def actualizar_supervisor(self, supervisor_actualizado: UpdateSupervisor, id_supervisor: UUID) -> Optional[Supervisor]:
        return await self.repository.actualizar_supervisor(supervisor_actualizado, id_supervisor)

    async def eliminar_supervisor(self, id_supervisor: UUID) -> bool:
        return await self.repository.eliminar_supervisor(id_supervisor)