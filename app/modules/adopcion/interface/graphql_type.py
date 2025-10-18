import strawberry
from datetime import datetime
from uuid import UUID
from typing import Optional


@strawberry.type
class AdopcionType:
    """Tipo GraphQL para Adopción"""
    id_adopcion: strawberry.ID
    fecha_adopcion: datetime
    estado: str
    id_publicacion: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None


@strawberry.input
class CreateAdopcionInput:
    """Input para crear una nueva adopción"""
    fecha_adopcion: datetime
    estado: str
    id_publicacion: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None


@strawberry.input
class UpdateAdopcionInput:
    """Input para actualizar una adopción existente"""
    id_adopcion: strawberry.ID
    fecha_adopcion: Optional[datetime] = None
    estado: Optional[str] = None
    id_publicacion: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None
