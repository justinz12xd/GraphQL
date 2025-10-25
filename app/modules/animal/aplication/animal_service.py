from app.modules.animal.infraestructure.animal_repository import AnimalRepository
from app.modules.animal.domain.entities import Animal
from uuid import UUID
from typing import List, Optional


class AnimalService:
    def __init__(self, repo: AnimalRepository):
        self.repo = repo

    async def obtener_animales(self) -> List[Animal]:
        return await self.repo.listar_animales()

    async def obtener_animal_por_id(self, id_animal: UUID) -> Optional[Animal]:
        return await self.repo.obtener_animal_por_id(id_animal)