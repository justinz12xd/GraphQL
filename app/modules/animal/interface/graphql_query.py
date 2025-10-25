import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.animal.interface.graphql_type import AnimalType, AnimalesPaginadosType
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
    
    @strawberry.field
    async def buscar_animales(self, nombre: str) -> List[AnimalType]:
        """Buscar animales por nombre (búsqueda parcial, case-insensitive)"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.buscar_animales_por_nombre(nombre)
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
    async def animales_por_edad(
        self, 
        edad_min: Optional[int] = None, 
        edad_max: Optional[int] = None
    ) -> List[AnimalType]:
        """Filtrar animales por rango de edad (ambos parámetros opcionales)"""
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        animales = await service.obtener_animales_por_rango_edad(edad_min, edad_max)
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
    async def animales_filtrados(
        self,
        nombre: Optional[str] = None,
        id_especie: Optional[strawberry.ID] = None,
        id_refugio: Optional[strawberry.ID] = None,
        estado_adopcion: Optional[str] = None,
        edad_min: Optional[int] = None,
        edad_max: Optional[int] = None
    ) -> List[AnimalType]:
        """
        Filtrar animales con múltiples criterios combinados.
        Todos los parámetros son opcionales.
        """
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        
        # Convertir IDs de strawberry.ID a UUID si existen
        especie_uuid = UUID(id_especie) if id_especie else None
        refugio_uuid = UUID(id_refugio) if id_refugio else None
        
        animales = await service.obtener_animales_filtrados(
            nombre=nombre,
            id_especie=especie_uuid,
            id_refugio=refugio_uuid,
            estado_adopcion=estado_adopcion,
            edad_min=edad_min,
            edad_max=edad_max
        )
        
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
    async def animales_paginados(
        self,
        limit: int = 20,
        offset: int = 0,
        nombre: Optional[str] = None,
        id_especie: Optional[strawberry.ID] = None,
        id_refugio: Optional[strawberry.ID] = None,
        estado_adopcion: Optional[str] = None,
        edad_min: Optional[int] = None,
        edad_max: Optional[int] = None
    ) -> AnimalesPaginadosType:
        """
        Obtener animales con paginación y filtros opcionales.
        Retorna resultados paginados con metadata.
        """
        adapter = AnimalRepository()
        service = AnimalService(adapter)
        
        # Convertir IDs de strawberry.ID a UUID si existen
        especie_uuid = UUID(id_especie) if id_especie else None
        refugio_uuid = UUID(id_refugio) if id_refugio else None
        
        resultado = await service.obtener_animales_paginados(
            limit=limit,
            offset=offset,
            nombre=nombre,
            id_especie=especie_uuid,
            id_refugio=refugio_uuid,
            estado_adopcion=estado_adopcion,
            edad_min=edad_min,
            edad_max=edad_max
        )
        
        animales_types = [AnimalType(
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
        ) for animal in resultado["animales"]]
        
        return AnimalesPaginadosType(
            animales=animales_types,
            total_count=resultado["total_count"],
            has_more=resultado["has_more"],
            total_pages=resultado["total_pages"],
            current_page=resultado["current_page"],
            limit=resultado["limit"],
            offset=resultado["offset"]
        )

