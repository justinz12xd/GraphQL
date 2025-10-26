"""
Queries de agregación generales del sistema.
"""

import strawberry
from typing import List
from app.reports.schemas.aggregation_schemas import ActividadMensualType
from app.reports.services.aggregation_service import GeneralAggregationService


@strawberry.type
class GeneralAggregationQuery:
    """Queries de estadísticas generales que combinan múltiples módulos"""
    
    @strawberry.field(description="Actividad mensual del sistema (adopciones, publicaciones, donaciones)")
    async def actividad_mensual(self, meses: int = 12) -> List[ActividadMensualType]:
        """
        Query 7: Actividad mensual del sistema
        
        Retorna un resumen mensual de la actividad del sistema combinando:
        - Total de adopciones
        - Total de publicaciones
        - Total de donaciones
        - Monto total donado
        
        Args:
            meses: Número de meses hacia atrás (default: 12)
        """
        service = GeneralAggregationService()
        
        stats = await service.obtener_actividad_mensual(meses)
        
        return [
            ActividadMensualType(
                periodo=item["periodo"],
                total_adopciones=item["total_adopciones"],
                total_publicaciones=item["total_publicaciones"],
                total_donaciones=item["total_donaciones"],
                monto_total_donado=item["monto_total_donado"]
            )
            for item in stats
        ]
