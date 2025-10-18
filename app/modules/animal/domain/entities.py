from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Optional, List

@dataclass
class Animal:
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

@dataclass
class NewAnimal:
    nombre: str
    id_especie: Optional[UUID]
    edad: Optional[int]
    estado: Optional[str]
    descripcion: Optional[str]
    fotos: Optional[List[str]]
    estado_adopcion: Optional[str]
    id_refugio: Optional[UUID]

@dataclass
class UpdateAnimal:
    nombre: Optional[str]
    id_especie: Optional[UUID]
    edad: Optional[int]
    estado: Optional[str]
    descripcion: Optional[str]
    fotos: Optional[List[str]]
    estado_adopcion: Optional[str]
    id_refugio: Optional[UUID]