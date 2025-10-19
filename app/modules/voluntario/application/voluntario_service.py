from typing import Optional
from uuid import UUID
from app.modules.voluntario.domain.entities import Voluntario, NewVoluntario, UpdateVoluntario
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository

class VoluntarioService:
    def __init__(self):
        self.repository = VoluntarioRepository()

    async def listar_voluntarios(self) -> list[Voluntario]:
        return await self.repository.listar_voluntarios()

    async def obtener_voluntario_por_id(self, id_voluntario: UUID) -> Optional[Voluntario]:
        return await self.repository.obtener_voluntario_por_id(id_voluntario)

    async def crear_voluntario(self, nuevo_voluntario: NewVoluntario) -> Voluntario:
        return await self.repository.crear_voluntario(nuevo_voluntario)

    async def actualizar_voluntario(self, voluntario_actualizado: UpdateVoluntario, id_voluntario: UUID) -> Optional[Voluntario]:
        return await self.repository.actualizar_voluntario(voluntario_actualizado, id_voluntario)

    async def eliminar_voluntario(self, id_voluntario: UUID) -> bool:
        return await self.repository.eliminar_voluntario(id_voluntario)
