from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    id_usuario: UUID
    nombre: str
    email: str
    contrasenia: str
    fecha_registro: datetime
    telefono: Optional[str] = None
    direccion: Optional[str] = None

@dataclass
class NewUsuario:
    nombre: str
    email: str
    contrasenia: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

@dataclass
class UpdateUsuario:
    id_usuario: UUID
    nombre: Optional[str] = None
    email: Optional[str] = None
    contrasenia: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None