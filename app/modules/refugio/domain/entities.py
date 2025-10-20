from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional


# Entidades del dominio para Refugio
# Representan la estructura de los datos que atraviesan las capas.

@dataclass
class Refugio:
    id_refugio: UUID
    nombre: str
    direccion: str
    telefono: Optional[str]
    capacidad: int
    estado: str
    fecha_creacion: datetime


@dataclass
class NewRefugio:
    nombre: str
    direccion: str
    telefono: Optional[str]
    capacidad: int
    estado: str
    fecha_creacion: datetime


@dataclass
class UpdateRefugio:
    id_refugio: UUID
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
