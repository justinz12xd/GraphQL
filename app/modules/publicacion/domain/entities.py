from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional


# Entidades del dominio para Publicacion
# Aquí definimos las representaciones in-memory (DTOs/Entities) que
# se usan a través de la capa de aplicación y los adaptadores.

@dataclass
class Publicacion:
    id_publicacion: UUID
    titulo: str
    descripcion: str
    fecha_publicacion: datetime
    estado: str
    id_usuario: UUID


@dataclass
class NewPublicacion:
    titulo: str
    descripcion: str
    fecha_publicacion: datetime
    estado: str
    id_usuario: UUID


@dataclass
class UpdatePublicacion:
    id_publicacion: UUID
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    estado: Optional[str] = None
    id_usuario: Optional[UUID] = None
