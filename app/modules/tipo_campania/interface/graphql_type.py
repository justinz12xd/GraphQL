import strawberry
from typing import Optional

@strawberry.type
class TipoCampaniaType:
    """Tipo GraphQL para TipoCampania"""
    id_tipo_campania: strawberry.ID
    nombre: str
    descripcion: Optional[str]

@strawberry.input
class CreateTipoCampaniaInput:
    """Input para crear un nuevo TipoCampania"""
    nombre: str
    descripcion: Optional[str] = None

@strawberry.input
class UpdateTipoCampaniaInput:
    """Input para actualizar un TipoCampania"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None