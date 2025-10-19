import strawberry
from typing import List, Optional
from uuid import UUID
from datetime import datetime

@strawberry.type
class CausaUrgenteType:
    id_causa_urgente: UUID
    titulo: str
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None

@strawberry.input
class CreateCausaUrgenteInput:
    titulo: str
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None

@strawberry.input
class UpdateCausaUrgenteInput:
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None
