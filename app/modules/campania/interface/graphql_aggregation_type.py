"""
Tipos de agregación para estadísticas de campañas.
"""

import strawberry
from typing import Optional


@strawberry.type(description="Estadísticas agregadas de campañas")
class EstadisticasCampaniasType:
    """Estadísticas financieras y de cumplimiento de campañas."""
    
    total_campanias: int = strawberry.field(description="Total de campañas registradas")
    campanias_activas: int = strawberry.field(description="Campañas actualmente activas")
    campanias_completadas: int = strawberry.field(description="Campañas finalizadas exitosamente")
    
    # Métricas financieras
    monto_total_recaudado: float = strawberry.field(
        description="Suma total de dinero recaudado (S/)"
    )
    meta_total: float = strawberry.field(
        description="Suma de todas las metas de campañas (S/)"
    )
    porcentaje_cumplimiento_global: float = strawberry.field(
        description="Porcentaje de cumplimiento global de todas las metas (%)"
    )
    
    # Agregaciones
    campania_mas_exitosa: Optional[str] = strawberry.field(
        description="Nombre de la campaña con mayor recaudación"
    )
    promedio_recaudado_por_campania: float = strawberry.field(
        description="Promedio de recaudación por campaña (S/)"
    )


@strawberry.type(description="Detalle de recaudación de una campaña")
class RecaudacionCampaniaType:
    """Información detallada de recaudación de una campaña específica."""
    
    id_campania: strawberry.ID = strawberry.field(description="ID de la campaña")
    titulo: str = strawberry.field(description="Título de la campaña")
    
    # Métricas financieras
    meta: float = strawberry.field(description="Meta de recaudación (S/)")
    monto_recaudado: float = strawberry.field(description="Monto actualmente recaudado (S/)")
    monto_faltante: float = strawberry.field(description="Monto faltante para alcanzar la meta (S/)")
    porcentaje_avance: float = strawberry.field(description="Porcentaje de avance hacia la meta (%)")
    
    # Métricas de participación
    total_donaciones: int = strawberry.field(description="Número total de donaciones recibidas")
    donacion_promedio: float = strawberry.field(description="Monto promedio por donación (S/)")
    donacion_minima: Optional[float] = strawberry.field(description="Donación mínima recibida (S/)")
    donacion_maxima: Optional[float] = strawberry.field(description="Donación máxima recibida (S/)")
