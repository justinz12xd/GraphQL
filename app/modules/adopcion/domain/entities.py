from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Adopcion:
    id_adopcion: UUID
    fecha_adopcion: datetime
    estado: str
    id_publicacion: UUID
    id_usuario: UUID

@dataclass
class NewAdopcion:
    fecha_adopcion: datetime
    estado: str
    id_publicacion: UUID
    id_usuario: UUID

@dataclass
class UpdateAdopcion:
    fecha_adopcion: Optional[datetime]
    estado: Optional[str]
    id_publicacion: Optional[UUID]
    id_usuario: Optional[UUID]

