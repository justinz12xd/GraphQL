import strawberry
from typing import List
from uuid import UUID
from app.modules.animal.interface.graphql_type import AnimalType, NewAnimalInput, UpdateAnimalInput
from app.modules.animal.aplication.animal_service import AnimalService
from app.modules.animal.infraestructure.animal_repository import AnimalRepository


@strawberry.type
class AnimalQuery:
    @strawberry.field
    async def animales(self) -> List[AnimalType]:
        service = AnimalService()
        ls = await service.listar_animales()
        return [AnimalType(**a.__dict__) for a in ls]
    @strawberry.field
    async def animal(self, id_animal: UUID) -> AnimalType:
        service = AnimalService(AnimalRepository())
        return await service.obtener_animal(id_animal)
    
@strawberry.type
class AnimalMutation:
    @strawberry.mutation
    async def crear_animal(self, input: NewAnimalInput) -> AnimalType:
        service = AnimalService(AnimalRepository())
        return await service.crear_animal(input)

    @strawberry.mutation
    async def actualizar_animal(self, id_animal: UUID, input: UpdateAnimalInput) -> AnimalType:
        service = AnimalService(AnimalRepository())
        return await service.actualizar_animal(id_animal, input)
