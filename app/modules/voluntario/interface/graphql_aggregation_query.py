"""
Queries de agregación para estadísticas de voluntarios.
"""

import strawberry
from typing import List
from app.modules.voluntario.interface.graphql_aggregation_type import ParticipacionVoluntariosType
from app.modules.voluntario.application.voluntario_aggregation_service import VoluntarioAggregationService
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository


@strawberry.type
class VoluntarioAggregationQuery:
    """Queries de estadísticas y agregaciones para voluntarios"""
    
    @strawberry.field(description="Participación de voluntarios agrupada por tipo de campaña")
    async def participacion_voluntarios_por_tipo_campania(self) -> List[ParticipacionVoluntariosType]:
        """
        Query 6: ¿Qué tipo de campañas atraen más voluntarios?
        
        Retorna estadísticas de participación de voluntarios agrupadas por tipo de campaña
        (educación, rescate, esterilización, etc.), mostrando:
        - Total de voluntarios por tipo
        - Porcentaje de participación
        - Voluntarios activos e inactivos
        """
        repository = VoluntarioRepository()
        service = VoluntarioAggregationService(repository)
        
        stats = await service.obtener_participacion_por_tipo_campania()
        
        return [
            ParticipacionVoluntariosType(
                tipo_campania=item["tipo_campania"],
                total_voluntarios=item["total_voluntarios"],
                porcentaje_participacion=item["porcentaje_participacion"],
                voluntarios_activos=item["voluntarios_activos"],
                voluntarios_inactivos=item["voluntarios_inactivos"]
            )
            for item in stats
        ]
