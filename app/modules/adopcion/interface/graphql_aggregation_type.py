"""
Tipos de agregación para estadísticas de adopciones.
"""

import strawberry
from typing import List, Optional


@strawberry.type(description="Conteo agrupado de elementos")
class ConteoType:
    """Representa un conteo agrupado genérico."""
    
    categoria: str = strawberry.field(description="Nombre de la categoría")
    cantidad: int = strawberry.field(description="Cantidad de elementos en esta categoría")
    porcentaje: float = strawberry.field(description="Porcentaje del total (%)")


@strawberry.type(description="Tendencia temporal de adopciones")
class TendenciaAdopcionesType:
    """Representa datos de adopciones en un período de tiempo."""
    
    periodo: str = strawberry.field(description="Período de tiempo (ej: '2024-01', 'Enero 2024')")
    total_adopciones: int = strawberry.field(description="Número de adopciones en el período")
    especies_adoptadas: List[ConteoType] = strawberry.field(
        description="Distribución de especies adoptadas en el período"
    )


@strawberry.type(description="Estadísticas de adopciones")
class EstadisticasAdopcionesType:
    """Estadísticas agregadas del proceso de adopción."""
    
    total_adopciones: int = strawberry.field(description="Total de adopciones realizadas")
    adopciones_mes_actual: int = strawberry.field(
        description="Adopciones realizadas en el mes actual"
    )
    adopciones_anio_actual: int = strawberry.field(
        description="Adopciones realizadas en el año actual"
    )
    
    # Métricas de tiempo
    promedio_dias_adopcion: Optional[float] = strawberry.field(
        description="Promedio de días desde ingreso hasta adopción"
    )
    
    # Distribuciones
    especies_mas_adoptadas: List[ConteoType] = strawberry.field(
        description="Ranking de especies más adoptadas"
    )
    refugios_mas_adopciones: List[ConteoType] = strawberry.field(
        description="Ranking de refugios con más adopciones"
    )
    
    # Tendencias temporales
    tendencia_mensual: List[TendenciaAdopcionesType] = strawberry.field(
        description="Tendencia de adopciones por mes (últimos 12 meses)"
    )
