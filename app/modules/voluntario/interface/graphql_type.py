import strawberry
from typing import Optional
from uuid import UUID

@strawberry.type
class VoluntarioType:
    """Tipo GraphQL para representar un voluntario"""
    id_voluntario: UUID
    rol: str
    estado: str
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None

@strawberry.input
class CreateVoluntarioInput:
    """Input para crear un nuevo voluntario"""
    rol: str
    estado: str
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None

@strawberry.input
class UpdateVoluntarioInput:
    """Input para actualizar un voluntario"""
    rol: Optional[str] = None
    estado: Optional[str] = None
    id_usuario: Optional[UUID] = None
    id_campania: Optional[UUID] = None

