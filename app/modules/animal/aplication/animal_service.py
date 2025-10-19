from app.modules.animal.infraestructure.animal_repository import AnimalRepository
from app.modules.animal.domain.entities import Animal, NewAnimal, UpdateAnimal
from uuid import UUID
from typing import List, Optional



class AnimalService:
    def __init__(self, repo: AnimalRepository):
        self.repo = repo

    async def obtener_animales(self) -> List[Animal]:
        return await self.repo.listar_animales()

    async def obtener_animal_por_id(self, id_animal: UUID) -> Optional[Animal]:
        return await self.repo.obtener_animal_por_id(id_animal)

    async def crear_animal(self, new_animal: NewAnimal) -> Animal:
        return await self.repo.crear_animal(new_animal)

    async def actualizar_animal(self, id_animal: UUID, update: UpdateAnimal) -> Optional[Animal]:
        return await self.repo.actualizar_animal(id_animal, update)

    async def eliminar_animal(self, id_animal: UUID) -> bool:
        return await self.repo.eliminar_animal(id_animal)