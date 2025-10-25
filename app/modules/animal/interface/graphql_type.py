import strawberry
from uuid import UUID
from typing import Optional, List

@strawberry.type
class AnimalType:
    id_animal: UUID
    nombre: str
    id_especie: Optional[UUID]
    especie: Optional[str]
    edad: Optional[int]
    estado: Optional[str]
    descripcion: Optional[str]
    fotos: Optional[List[str]]
    estado_adopcion: Optional[str]
    id_refugio: Optional[UUID]

@strawberry.type
class AnimalesPaginadosType:
    """Tipo de respuesta para queries con paginación"""
    animales: List[AnimalType]
    total_count: int
    has_more: bool
    total_pages: int
    current_page: int
    limit: int
    offset: int

@strawberry.input
class NewAnimalInput:
    nombre: str
    id_especie: Optional[UUID]
    edad: Optional[int]
    estado: Optional[str]
    descripcion: Optional[str]
    fotos: Optional[List[str]]
    estado_adopcion: Optional[str]
    id_refugio: Optional[UUID]

@strawberry.input
class UpdateAnimalInput:
    nombre: Optional[str]
    id_especie: Optional[UUID]
    edad: Optional[int]
    estado: Optional[str]
    descripcion: Optional[str]
    fotos: Optional[List[str]]
    estado_adopcion: Optional[str]
    id_refugio: Optional[UUID]
