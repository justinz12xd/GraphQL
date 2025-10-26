"""
Queries de agregación para estadísticas de adopciones.
"""

import strawberry
from typing import List
from app.modules.adopcion.interface.graphql_aggregation_type import (
    EstadisticasAdopcionesType,
    TendenciaAdopcionesType,
    ConteoType
)
from app.modules.adopcion.application.adopcion_aggregation_service import AdopcionAggregationService
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository


@strawberry.type
class AdopcionAggregationQuery:
    """Queries de estadísticas y agregaciones para adopciones"""
    
    @strawberry.field(description="Obtiene estadísticas generales de adopciones con agregaciones")
    async def estadisticas_adopciones(self) -> EstadisticasAdopcionesType:
        """
        Retorna estadísticas agregadas de adopciones:
        - Total de adopciones
        - Adopciones del mes y año actual
        - Especies más adoptadas
        - Refugios con más adopciones
        - Tendencia mensual (últimos 12 meses)
        """
        repository = AdopcionRepository()
        service = AdopcionAggregationService(repository)
        
        # Obtener estadísticas
        stats = await service.obtener_estadisticas_generales()
        
        # Convertir especies_mas_adoptadas a ConteoType
        especies_mas_adoptadas = [
            ConteoType(
                categoria=item["categoria"],
                cantidad=item["cantidad"],
                porcentaje=item["porcentaje"]
            )
            for item in stats["especies_mas_adoptadas"]
        ]
        
        # Convertir refugios_mas_adopciones a ConteoType
        refugios_mas_adopciones = [
            ConteoType(
                categoria=item["categoria"],
                cantidad=item["cantidad"],
                porcentaje=item["porcentaje"]
            )
            for item in stats["refugios_mas_adopciones"]
        ]
        
        # Convertir tendencia_mensual a TendenciaAdopcionesType
        tendencia_mensual = [
            TendenciaAdopcionesType(
                periodo=item["periodo"],
                total_adopciones=item["total_adopciones"],
                especies_adoptadas=[
                    ConteoType(
                        categoria=esp["categoria"],
                        cantidad=esp["cantidad"],
                        porcentaje=esp["porcentaje"]
                    )
                    for esp in item["especies_adoptadas"]
                ]
            )
            for item in stats["tendencia_mensual"]
        ]
        
        return EstadisticasAdopcionesType(
            total_adopciones=stats["total_adopciones"],
            adopciones_mes_actual=stats["adopciones_mes_actual"],
            adopciones_anio_actual=stats["adopciones_anio_actual"],
            promedio_dias_adopcion=stats["promedio_dias_adopcion"],
            especies_mas_adoptadas=especies_mas_adoptadas,
            refugios_mas_adopciones=refugios_mas_adopciones,
            tendencia_mensual=tendencia_mensual
        )
    
    @strawberry.field(description="Ranking de especies más adoptadas")
    async def especies_mas_adoptadas(self) -> List[ConteoType]:
        """
        Query 1: ¿Qué especies son más adoptadas?
        
        Retorna un ranking de especies ordenado por cantidad de adopciones,
        incluyendo el porcentaje que representa cada especie.
        """
        repository = AdopcionRepository()
        service = AdopcionAggregationService(repository)
        
        especies = await service.obtener_especies_mas_adoptadas()
        
        return [
            ConteoType(
                categoria=item["categoria"],
                cantidad=item["cantidad"],
                porcentaje=item["porcentaje"]
            )
            for item in especies
        ]
    
    @strawberry.field(description="Tendencia de adopciones por mes")
    async def adopciones_por_mes(self, meses: int = 12) -> List[TendenciaAdopcionesType]:
        """
        Query 2: ¿Cuántas adopciones hubo por mes?
        
        Args:
            meses: Número de meses hacia atrás a consultar (default: 12)
        
        Retorna el número de adopciones agrupadas por mes,
        incluyendo la distribución de especies adoptadas en cada período.
        """
        repository = AdopcionRepository()
        service = AdopcionAggregationService(repository)
        
        tendencia = await service.obtener_adopciones_por_mes(meses)
        
        return [
            TendenciaAdopcionesType(
                periodo=item["periodo"],
                total_adopciones=item["total_adopciones"],
                especies_adoptadas=[
                    ConteoType(
                        categoria=esp["categoria"],
                        cantidad=esp["cantidad"],
                        porcentaje=esp["porcentaje"]
                    )
                    for esp in item["especies_adoptadas"]
                ]
            )
            for item in tendencia
        ]
