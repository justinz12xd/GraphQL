"""
Tipos de agregación para estadísticas de voluntarios.
"""

import strawberry
from typing import List


@strawberry.type(description="Conteo agrupado de elementos")
class ConteoType:
    """Representa un conteo agrupado genérico."""
    
    categoria: str = strawberry.field(description="Nombre de la categoría")
    cantidad: int = strawberry.field(description="Cantidad de elementos en esta categoría")
    porcentaje: float = strawberry.field(description="Porcentaje del total (%)")


@strawberry.type(description="Participación de voluntarios por tipo de campaña")
class ParticipacionVoluntariosType:
    """Estadísticas de participación de voluntarios agrupadas por tipo de campaña."""
    
    tipo_campania: str = strawberry.field(description="Nombre del tipo de campaña")
    total_voluntarios: int = strawberry.field(description="Total de voluntarios en este tipo")
    porcentaje_participacion: float = strawberry.field(description="Porcentaje del total de voluntarios (%)")
    voluntarios_activos: int = strawberry.field(description="Voluntarios con estado activo")
    voluntarios_inactivos: int = strawberry.field(description="Voluntarios con estado inactivo")
