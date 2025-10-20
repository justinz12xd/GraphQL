from dataclasses import dataclass
from typing import Optional


@dataclass
class Especie:
    """Entidad de dominio que representa una especie (por ejemplo, perro, gato, etc.)."""

    id: Optional[int]  # Identificador único de la especie
    nombre: str        # Nombre de la especie
