from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional


# Entidades del dominio para Seguimiento
# Representan los registros de seguimiento que pueden estar asociados a publicaciones,
# campañas, usuarios o animales según el modelo del sistema.

@dataclass
class Seguimiento:
    id_seguimiento: UUID
    fecha: datetime
    descripcion: str
    tipo: str  # e.g., 'comentario', 'estado', 'evento'
    id_referencia: Optional[UUID]  # id de la entidad referenciada (publicacion/usuario/etc.)
    id_usuario: Optional[UUID]


@dataclass
class NewSeguimiento:
    fecha: datetime
    descripcion: str
    tipo: str
    id_referencia: Optional[UUID]
    id_usuario: Optional[UUID]


@dataclass
class UpdateSeguimiento:
    id_seguimiento: UUID
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    id_referencia: Optional[UUID] = None
    id_usuario: Optional[UUID] = None
