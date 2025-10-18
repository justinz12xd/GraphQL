import strawberry
from typing import List
from uuid import UUID
from app.modules.animal.interface.graphql_type import AnimalType
from app.modules.animal.aplication.animal_service import AnimalService
from app.modules.animal.infraestructure.animal_repository import AnimalRepository
from app.modules.animal.domain.entities import Animal



@strawberry.type
class AnimalQuery:
    @strawberry.field
    async def animales(self) -> List[AnimalType]:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.obtener_animales()
        return [AnimalType(
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
        ) for animal in animales]   

    @strawberry.field
    async def animal(self, id_animal: strawberry.ID) -> AnimalType:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animal = await service.obtener_animal_por_id(UUID(id_animal))
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

    @strawberry.field
    async def animales_por_especie(self, id_especie: strawberry.ID) -> List[AnimalType]:
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.obtener_animales_por_especie(UUID(id_especie))
        return [AnimalType(
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
        ) for animal in animales]

