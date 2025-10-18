import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.causa_urgente.interface.graphql_type import CausaUrgenteType
from app.modules.causa_urgente.application.causa_urgente_service import CausaUrgenteService
from app.modules.causa_urgente.infrastructure.causa_urgente_repository import CausaUrgenteRepository

@strawberry.type
class CausaUrgenteQuery:
    @strawberry.field
    async def causas_urgentes(self) -> List[CausaUrgenteType]:
        service = CausaUrgenteService(CausaUrgenteRepository())
        causas_urgentes = await service.obtener_causas_urgentes()
        return [CausaUrgenteType(
            id_causa_urgente=strawberry.ID(str(causa.id_causa_urgente)),
            titulo=causa.titulo,
            descripcion=causa.descripcion,
            meta=causa.meta,
            fecha_limite=causa.fecha_limite,
            id_refugio=strawberry.ID(str(causa.id_refugio)) if causa.id_refugio else None,
            id_animal=strawberry.ID(str(causa.id_animal)) if causa.id_animal else None,
            fotos=causa.fotos) for causa in causas_urgentes]
    
    @strawberry.field
    async def causa_urgente_por_id(self, id_causa_urgente: strawberry.ID) -> CausaUrgenteType:
        service = CausaUrgenteService(CausaUrgenteRepository())
        causa_urgente = await service.obtener_causa_urgente_por_id(UUID(id_causa_urgente))
        if causa_urgente is None:
            return None
        return CausaUrgenteType(
            id_causa_urgente=strawberry.ID(str(causa_urgente.id_causa_urgente)),
            titulo=causa_urgente.titulo,
            descripcion=causa_urgente.descripcion,
            meta=causa_urgente.meta,
            fecha_limite=causa_urgente.fecha_limite,
            id_refugio=strawberry.ID(str(causa_urgente.id_refugio)) if causa_urgente.id_refugio else None,
            id_animal=strawberry.ID(str(causa_urgente.id_animal)) if causa_urgente.id_animal else None,
            fotos=causa_urgente.fotos)
    
    # NOTA: crear_causa_urgente se movió a CausaUrgenteMutation
    # NOTA: actualizar_causa_urgente se movió a CausaUrgenteMutation  
    # NOTA: eliminar_causa_urgente se movió a CausaUrgenteMutation
    # Las operaciones de creación, actualización y eliminación no deben estar en Query, solo en Mutation

#Queries por refugio a probar luego
    @strawberry.field
    async def causas_urgentes_por_refugio(self, id_refugio: strawberry.ID) -> List[CausaUrgenteType]:
        service = CausaUrgenteService(CausaUrgenteRepository())
        causas_urgentes = await service.obtener_causas_urgentes_por_refugio(UUID(id_refugio))
        return [CausaUrgenteType(
            id_causa_urgente=strawberry.ID(str(causa.id_causa_urgente)),
            titulo=causa.titulo,
            descripcion=causa.descripcion,
            meta=causa.meta,
            fecha_limite=causa.fecha_limite,
            id_refugio=strawberry.ID(str(causa.id_refugio)) if causa.id_refugio else None,
            id_animal=strawberry.ID(str(causa.id_animal)) if causa.id_animal else None,
            fotos=causa.fotos) for causa in causas_urgentes]
    @strawberry.field
    async def causas_urgentes_por_animal(self, id_animal: strawberry.ID) -> List[CausaUrgenteType]:
        service = CausaUrgenteService(CausaUrgenteRepository())
        causas_urgentes = await service.obtener_causas_urgentes_por_animal(UUID(id_animal))
        return [CausaUrgenteType(
            id_causa_urgente=strawberry.ID(str(causa.id_causa_urgente)),
            titulo=causa.titulo,
            descripcion=causa.descripcion,
            meta=causa.meta,
            fecha_limite=causa.fecha_limite,
            id_refugio=strawberry.ID(str(causa.id_refugio)) if causa.id_refugio else None,
            id_animal=strawberry.ID(str(causa.id_animal)) if causa.id_animal else None,
            fotos=causa.fotos) for causa in causas_urgentes]
