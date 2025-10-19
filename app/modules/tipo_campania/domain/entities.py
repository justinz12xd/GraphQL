from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class TipoCampania:
    id_tipo_campania: UUID
    nombre: str
    descripcion: Optional[str] = None

@dataclass
class NewTipoCampania:
    nombre: str
    descripcion: Optional[str] = None

@dataclass
class UpdateTipoCampania:
    id_tipo_campania: UUID
    nombre: Optional[str] = None
    descripcion: Optional[str] = None