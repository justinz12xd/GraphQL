import strawberry
from typing import Optional


@strawberry.type
class EspecieType:
    """Tipo GraphQL que representa la entidad Especie."""
    id: int
    nombre: str
