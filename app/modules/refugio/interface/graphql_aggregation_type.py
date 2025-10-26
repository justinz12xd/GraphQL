"""
Tipos de agregación para estadísticas de refugios.
"""

import strawberry
from typing import List, Optional


@strawberry.type(description="Conteo agrupado de elementos")
class ConteoType:
    """Representa un conteo agrupado genérico."""
    
    categoria: str = strawberry.field(description="Nombre de la categoría")
    cantidad: int = strawberry.field(description="Cantidad de elementos en esta categoría")
    porcentaje: float = strawberry.field(description="Porcentaje del total (%)")


@strawberry.type(description="Estadísticas de un refugio específico")
class EstadisticasRefugioType:
    """Estadísticas y métricas de un refugio."""
    
    id_refugio: strawberry.ID = strawberry.field(description="ID único del refugio")
    nombre: str = strawberry.field(description="Nombre del refugio")
    
    # Métricas de capacidad
    capacidad_total: int = strawberry.field(description="Capacidad máxima del refugio")
    total_animales: int = strawberry.field(description="Total de animales alojados actualmente")
    capacidad_utilizada_porcentaje: float = strawberry.field(
        description="Porcentaje de capacidad utilizada (%)"
    )
    espacios_disponibles: int = strawberry.field(description="Espacios libres disponibles")
    
    # Distribución por especie
    animales_por_especie: List[ConteoType] = strawberry.field(
        description="Distribución de animales por especie en este refugio"
    )
    
    # Métricas de adopción
    total_adoptados: int = strawberry.field(
        description="Total de animales adoptados desde este refugio"
    )
    tasa_adopcion_porcentaje: Optional[float] = strawberry.field(
        description="Porcentaje de adopciones exitosas (%)"
    )
