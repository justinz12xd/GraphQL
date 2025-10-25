from typing import Optional
from uuid import UUID
from app.modules.voluntario.domain.entities import Voluntario
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository

class VoluntarioService:
    def __init__(self):
        self.repository = VoluntarioRepository()

    async def listar_voluntarios(self) -> list[Voluntario]:
        return await self.repository.listar_voluntarios()

    async def obtener_voluntario_por_id(self, id_voluntario: UUID) -> Optional[Voluntario]:
        return await self.repository.obtener_voluntario_por_id(id_voluntario)
