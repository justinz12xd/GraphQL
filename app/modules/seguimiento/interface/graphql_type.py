import strawberry
from datetime import datetime
from typing import Optional
from uuid import UUID


@strawberry.type
class SeguimientoType:
    """Tipo GraphQL para Seguimiento"""
    id_seguimiento: strawberry.ID
    fecha: datetime
    descripcion: str
    tipo: str
    id_referencia: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None


@strawberry.input
class CreateSeguimientoInput:
    """Input para crear un nuevo seguimiento"""
    fecha: datetime
    descripcion: str
    tipo: str
    id_referencia: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None


@strawberry.input
class UpdateSeguimientoInput:
    """Input para actualizar un seguimiento existente"""
    id_seguimiento: strawberry.ID
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    id_referencia: Optional[strawberry.ID] = None
    id_usuario: Optional[strawberry.ID] = None
