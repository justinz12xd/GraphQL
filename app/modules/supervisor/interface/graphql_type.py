import strawberry
from typing import Optional
from uuid import UUID

@strawberry.type
class SupervisorType:
    """Tipo GraphQL para representar un supervisor"""
    id_supervisor: UUID
    nombre: str
    total_animales: int
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None

@strawberry.input
class CreateSupervisorInput:
    """Input para crear un nuevo supervisor"""
    nombre: str
    total_animales: int
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None

@strawberry.input
class UpdateSupervisorInput:
    """Input para actualizar un supervisor"""
    nombre: Optional[str] = None
    total_animales: Optional[int] = None
    id_refugio: Optional[UUID] = None
    id_usuario: Optional[UUID] = None