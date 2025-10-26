"""
Tipos de agregación para estadísticas de donaciones y pagos.
"""

import strawberry
from typing import List, Optional


@strawberry.type(description="Conteo agrupado de elementos")
class ConteoType:
    """Representa un conteo agrupado genérico."""
    
    categoria: str = strawberry.field(description="Nombre de la categoría")
    cantidad: int = strawberry.field(description="Cantidad de elementos en esta categoría")
    porcentaje: float = strawberry.field(description="Porcentaje del total (%)")


@strawberry.type(description="Estadísticas de donaciones y pagos")
class EstadisticasDonacionesType:
    """Estadísticas financieras de donaciones y pagos."""
    
    total_donaciones: int = strawberry.field(description="Número total de donaciones")
    monto_total_donado: float = strawberry.field(description="Suma total donada (S/)")
    
    # Métricas de donaciones
    donacion_promedio: float = strawberry.field(description="Monto promedio por donación (S/)")
    donacion_minima: Optional[float] = strawberry.field(description="Donación más pequeña (S/)")
    donacion_maxima: Optional[float] = strawberry.field(description="Donación más grande (S/)")
    
    # Distribución por método de pago
    donaciones_por_metodo: List[ConteoType] = strawberry.field(
        description="Distribución de donaciones por método de pago"
    )
    
    # Distribución por estado
    donaciones_por_estado: List[ConteoType] = strawberry.field(
        description="Distribución de donaciones por estado (completado, pendiente, etc.)"
    )
    
    # Tendencias
    total_mes_actual: float = strawberry.field(description="Total donado en el mes actual (S/)")
    total_anio_actual: float = strawberry.field(description="Total donado en el año actual (S/)")
