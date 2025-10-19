from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class Supervisor:
    id_supervisor: UUID
    nombre: str
    total_animales: int
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None

@dataclass
class NewSupervisor:
    nombre: str
    total_animales: int
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None

@dataclass
class UpdateSupervisor:
    nombre: Optional[str] = None
    total_animales: Optional[int] = None
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None
