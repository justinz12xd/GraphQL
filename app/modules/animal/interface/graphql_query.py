import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.animal.interface.graphql_type import AnimalType
from app.modules.animal.aplication.animal_service import AnimalService
from app.modules.animal.infraestructure.animal_repository import AnimalRepository


@strawberry.type
class AnimalQuery:
    @strawberry.field
    async def animales(self, estado_adopcion: Optional[str] = None) -> List[AnimalType]:
        """Obtener todos los animales, opcionalmente filtrados por estado de adopción"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        
        if estado_adopcion:
            animales = await service.obtener_animales_por_estado_adopcion(estado_adopcion)
        else:
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
    async def animal(self, id_animal: strawberry.ID) -> Optional[AnimalType]:
        """Obtener un animal específico por ID"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animal = await service.obtener_animal_por_id(UUID(id_animal))
        
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

    @strawberry.field
    async def animales_por_especie(self, id_especie: strawberry.ID) -> List[AnimalType]:
        """Obtener animales filtrados por especie"""
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

    @strawberry.field
    async def animales_por_refugio(self, id_refugio: strawberry.ID) -> List[AnimalType]:
        """Obtener animales filtrados por refugio"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.obtener_animales_por_refugio(UUID(id_refugio))
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
    async def animales_disponibles(self) -> List[AnimalType]:
        """Obtener solo animales disponibles para adopción"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.obtener_animales_por_estado_adopcion("disponible")
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

