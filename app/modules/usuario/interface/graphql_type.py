import strawberry
from typing import Optional
from datetime import datetime
from uuid import UUID


@strawberry.type
class UsuarioType:
    """Tipo GraphQL para Usuario"""
    id_usuario: strawberry.ID
    nombre: str
    email: str
    telefono: Optional[str]
    direccion: Optional[str]
    fecha_registro: datetime


@strawberry.input
class CreateUsuarioInput:
    """Input para crear un nuevo usuario"""
    nombre: str
    email: str
    contrasenia: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None


@strawberry.input
class UpdateUsuarioInput:
    """Input para actualizar un usuario"""
    id_usuario: strawberry.ID
    nombre: Optional[str] = None
    email: Optional[str] = None
    contrasenia: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
