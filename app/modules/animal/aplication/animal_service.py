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
    
    async def obtener_animales_filtrados(
        self,
        nombre: Optional[str] = None,
        id_especie: Optional[UUID] = None,
        id_refugio: Optional[UUID] = None,
        estado_adopcion: Optional[str] = None,
        edad_min: Optional[int] = None,
        edad_max: Optional[int] = None
    ) -> List[Animal]:
        """
        Filtrar animales con múltiples criterios combinados.
        Todos los parámetros son opcionales.
        """
        todos_animales = await self.repo.listar_animales()
        
        resultado = []
        for animal in todos_animales:
            # Filtro por nombre (búsqueda parcial, case-insensitive)
            if nombre:
                if not animal.nombre or nombre.lower() not in animal.nombre.lower():
                    continue
            
            # Filtro por especie
            if id_especie:
                if animal.id_especie != id_especie:
                    continue
            
            # Filtro por refugio
            if id_refugio:
                if animal.id_refugio != id_refugio:
                    continue
            
            # Filtro por estado de adopción
            if estado_adopcion:
                if animal.estado_adopcion != estado_adopcion:
                    continue
            
            # Filtro por edad mínima
            if edad_min is not None:
                if animal.edad is None or animal.edad < edad_min:
                    continue
            
            # Filtro por edad máxima
            if edad_max is not None:
                if animal.edad is None or animal.edad > edad_max:
                    continue
            
            # Si pasó todos los filtros, agregarlo
            resultado.append(animal)
        
        return resultado
    
    async def obtener_animales_paginados(
        self,
        limit: int = 20,
        offset: int = 0,
        nombre: Optional[str] = None,
        id_especie: Optional[UUID] = None,
        id_refugio: Optional[UUID] = None,
        estado_adopcion: Optional[str] = None,
        edad_min: Optional[int] = None,
        edad_max: Optional[int] = None
    ) -> dict:
        """
        Obtener animales con paginación y filtros opcionales.
        Retorna un diccionario con los resultados paginados y metadata.
        """
        # Primero obtener todos los animales filtrados
        animales_filtrados = await self.obtener_animales_filtrados(
            nombre=nombre,
            id_especie=id_especie,
            id_refugio=id_refugio,
            estado_adopcion=estado_adopcion,
            edad_min=edad_min,
            edad_max=edad_max
        )
        
        # Calcular metadata de paginación
        total_count = len(animales_filtrados)
        has_more = offset + limit < total_count
        total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
        current_page = (offset // limit) + 1 if limit > 0 else 1
        
        # Aplicar paginación
        animales_paginados = animales_filtrados[offset:offset + limit]
        
        return {
            "animales": animales_paginados,
            "total_count": total_count,
            "has_more": has_more,
            "total_pages": total_pages,
            "current_page": current_page,
            "limit": limit,
            "offset": offset
        }