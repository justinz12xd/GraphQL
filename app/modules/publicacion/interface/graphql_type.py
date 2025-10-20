import strawberry
from datetime import datetime
from uuid import UUID
from typing import Optional


@strawberry.type
class PublicacionType:
    """Tipo GraphQL para Publicacion"""
    id_publicacion: strawberry.ID
    titulo: str
    descripcion: str
    fecha_publicacion: datetime
    estado: str
    id_usuario: Optional[strawberry.ID] = None


@strawberry.input
class CreatePublicacionInput:
    """Input para crear una nueva publicación"""
    titulo: str
    descripcion: str
    fecha_publicacion: datetime
    estado: str
    id_usuario: strawberry.ID


@strawberry.input
class UpdatePublicacionInput:
    """Input para actualizar una publicación existente"""
    id_publicacion: strawberry.ID
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    estado: Optional[str] = None
    id_usuario: Optional[strawberry.ID] = None
