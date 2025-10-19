import strawberry
from typing import List, Optional
from uuid import UUID
from datetime import datetime


@strawberry.type
class CampaniaType:
    id_campania: UUID
    id_tipo_campania: UUID
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None

@strawberry.input
class CreateCampaniaInput:
    id_tipo_campania: UUID
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None

@strawberry.input
class UpdateCampaniaInput:
    id_tipo_campania: Optional[UUID] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None

