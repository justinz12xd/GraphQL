import strawberry
from datetime import datetime
from typing import Optional


@strawberry.type
class RefugioType:
    """Tipo GraphQL para Refugio"""
    id_refugio: strawberry.ID
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    capacidad: int
    estado: str
    fecha_creacion: datetime


@strawberry.input
class CreateRefugioInput:
    """Input para crear un nuevo refugio"""
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    capacidad: int
    estado: str
    fecha_creacion: datetime


@strawberry.input
class UpdateRefugioInput:
    """Input para actualizar un refugio existente"""
    id_refugio: strawberry.ID
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
