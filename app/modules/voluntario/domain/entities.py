from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class Voluntario:
    id_voluntario: UUID
    rol: str
    estado: str
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None

@dataclass
class NewVoluntario:
    rol: str
    estado: str
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None

@dataclass
class UpdateVoluntario:
    rol: Optional[str] = None
    estado: Optional[str] = None
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None