from app.modules.animal.infraestructure.animal_repository import AnimalRepository
from app.modules.animal.domain.entities import Animal, NewAnimal, UpdateAnimal
from uuid import UUID

class AnimalService:
    def __init__(self):
        self.repo = AnimalRepository()

    async def listar_animales(self) -> list[Animal]:
        return await self.repo.listar_animales()

    async def obtener_animal(self, id_animal: UUID) -> Animal:
        return await self.repo.obtener_animal(id_animal)

    async def crear_animal(self, new_animal: NewAnimal) -> Animal:
        return await self.repo.crear_animal(new_animal)

    async def actualizar_animal(self, id_animal: UUID, update: UpdateAnimal) -> Animal:
        return await self.repo.actualizar_animal(id_animal, update)