"""
Tipos de agregación para estadísticas generales del sistema.
"""

import strawberry
from typing import List


@strawberry.type(description="Actividad mensual del sistema")
class ActividadMensualType:
    """Estadísticas de actividad mensual combinando adopciones, publicaciones y donaciones."""
    
    periodo: str = strawberry.field(description="Mes en formato YYYY-MM")
    total_adopciones: int = strawberry.field(description="Total de adopciones en el mes")
    total_publicaciones: int = strawberry.field(description="Total de publicaciones en el mes")
    total_donaciones: int = strawberry.field(description="Total de donaciones en el mes")
    monto_total_donado: float = strawberry.field(description="Monto total donado en el mes (S/)")
