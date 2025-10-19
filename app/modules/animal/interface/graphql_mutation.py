import strawberry
from uuid import UUID
from app.modules.animal.interface.graphql_type import AnimalType, NewAnimalInput, UpdateAnimalInput
from app.modules.animal.aplication.animal_service import AnimalService
from app.modules.animal.infraestructure.animal_repository import AnimalRepository
from app.modules.animal.domain.entities import NewAnimal, UpdateAnimal


@strawberry.type
class AnimalMutation:
    @strawberry.mutation
    async def crear_animal(self, input: NewAnimalInput) -> AnimalType:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        nuevo_animal = NewAnimal(
            nombre=input.nombre,
            id_especie=UUID(input.id_especie) if input.id_especie else None,
            edad=input.edad,
            estado=input.estado,
            descripcion=input.descripcion,
            fotos=input.fotos,
            estado_adopcion=input.estado_adopcion,
            id_refugio=UUID(input.id_refugio) if input.id_refugio else None
        )
        animal = await service.crear_animal(nuevo_animal)

        return AnimalType(
            id_animal=strawberry.ID(str(animal.id_animal)),
            nombre=animal.nombre,
            id_especie=strawberry.ID(str(animal.id_especie)) if animal.id_especie else None,
            especie=animal.especie,
            edad=animal.edad,
            estado=animal.estado,
            descripcion=animal.descripcion,
            fotos=animal.fotos,
            estado_adopcion=animal.estado_adopcion,
            id_refugio=strawberry.ID(str(animal.id_refugio)) if animal.id_refugio else None
        )

    @strawberry.mutation
    async def actualizar_animal(self, id_animal: strawberry.ID, input: UpdateAnimalInput) -> AnimalType:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animal_actualizado = UpdateAnimal(
            id_animal=UUID(id_animal),
            nombre=input.nombre,
            id_especie=UUID(input.id_especie) if input.id_especie else None,
            edad=input.edad,
            estado=input.estado,
            descripcion=input.descripcion,
            fotos=input.fotos,
            estado_adopcion=input.estado_adopcion,
            id_refugio=UUID(input.id_refugio) if input.id_refugio else None
        )

        animal = await service.actualizar_animal(animal_actualizado)

        if animal is None:
            return None

        return AnimalType(
            id_animal=strawberry.ID(str(animal.id_animal)),
            nombre=animal.nombre,
            id_especie=strawberry.ID(str(animal.id_especie)) if animal.id_especie else None,
            especie=animal.especie,
            edad=animal.edad,
            estado=animal.estado,
            descripcion=animal.descripcion,
                fotos=animal.fotos,
            estado_adopcion=animal.estado_adopcion,
            id_refugio=strawberry.ID(str(animal.id_refugio)) if animal.id_refugio else None
        )

    @strawberry.mutation
    async def eliminar_animal(self, id_animal: strawberry.ID) -> bool:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        return await service.eliminar_animal(UUID(id_animal))