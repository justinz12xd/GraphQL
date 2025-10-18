from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional
from typing import List

@dataclass
class CausaUrgente:
    id_causa_urgente: UUID
    titulo: str
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None


@dataclass
class NewCausaUrgente:
    titulo: str
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None

@dataclass
class UpdateCausaUrgente:
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    fecha_limite: Optional[datetime] = None
    id_refugio: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    fotos: Optional[List[str]] = None
