from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional
from typing import List

@dataclass 
class Campania:
    id_campania: UUID
    id_tipo_campania: UUID
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None

@dataclass
class NewCampania:
    id_tipo_campania: UUID
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None

@dataclass 
class UpdateCampania:
    id_tipo_campania: Optional[UUID] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar: Optional[str] = None
    organizador: Optional[str] = None
    estado: Optional[str] = None