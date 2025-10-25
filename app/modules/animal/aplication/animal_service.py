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
    
    async def obtener_animales_por_especie(self, id_especie: UUID) -> List[Animal]:
        """Obtener animales filtrados por especie"""
        todos_animales = await self.repo.listar_animales()
        return [animal for animal in todos_animales if animal.id_especie == id_especie]
    
    async def obtener_animales_por_refugio(self, id_refugio: UUID) -> List[Animal]:
        """Obtener animales filtrados por refugio"""
        todos_animales = await self.repo.listar_animales()
        return [animal for animal in todos_animales if animal.id_refugio == id_refugio]
    
    async def obtener_animales_por_estado_adopcion(self, estado: str) -> List[Animal]:
        """Obtener animales filtrados por estado de adopción"""
        todos_animales = await self.repo.listar_animales()
        return [animal for animal in todos_animales if animal.estado_adopcion == estado]
    
    async def buscar_animales_por_nombre(self, nombre: str) -> List[Animal]:
        """Buscar animales por nombre (búsqueda parcial, case-insensitive)"""
        todos_animales = await self.repo.listar_animales()
        nombre_lower = nombre.lower()
        return [
            animal for animal in todos_animales 
            if animal.nombre and nombre_lower in animal.nombre.lower()
        ]
    
    async def obtener_animales_por_rango_edad(self, edad_min: Optional[int] = None, edad_max: Optional[int] = None) -> List[Animal]:
        """Filtrar animales por rango de edad (ambos parámetros opcionales)"""
        todos_animales = await self.repo.listar_animales()
        
        resultado = []
        for animal in todos_animales:
            # Si no tiene edad, no incluir en resultados filtrados
            if animal.edad is None:
                continue
            
            # Verificar edad mínima
            if edad_min is not None and animal.edad < edad_min:
                continue
            
            # Verificar edad máxima
            if edad_max is not None and animal.edad > edad_max:
                continue
            
            resultado.append(animal)
        
        return resultado