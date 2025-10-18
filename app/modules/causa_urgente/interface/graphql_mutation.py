import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.causa_urgente.interface.graphql_type import CausaUrgenteType, CreateCausaUrgenteInput, UpdateCausaUrgenteInput
from app.modules.causa_urgente.application.causa_urgente_service import CausaUrgenteService
from app.modules.causa_urgente.infrastructure.causa_urgente_repository import CausaUrgenteRepository
from app.modules.causa_urgente.domain.entities import UpdateCausaUrgente, NewCausaUrgente
@strawberry.type
class CausaUrgenteMutation:

    @strawberry.mutation
    async def crear_causa_urgente(self, input: CreateCausaUrgenteInput) -> CausaUrgenteType:
        adapter = CausaUrgenteRepository()
        service = CausaUrgenteService(adapter)
        causa_urgente = await service.crear_causa_urgente(NewCausaUrgente(
            titulo=input.titulo,
            descripcion=input.descripcion,
            meta=input.meta,
            fecha_limite=input.fecha_limite,
            id_refugio=UUID(input.id_refugio) if input.id_refugio else None,
            id_animal=UUID(input.id_animal) if input.id_animal else None,
            fotos=input.fotos))

        causa_urgente = await service.crear_causa_urgente(causa_urgente)

        return CausaUrgenteType(
            id_causa_urgente=strawberry.ID(str(causa_urgente.id_causa_urgente)),
            titulo=causa_urgente.titulo,
            descripcion=causa_urgente.descripcion,
            meta=causa_urgente.meta,
            fecha_limite=causa_urgente.fecha_limite,
            id_refugio=strawberry.ID(str(causa_urgente.id_refugio)) if causa_urgente.id_refugio else None,
            id_animal=strawberry.ID(str(causa_urgente.id_animal)) if causa_urgente.id_animal else None,
            fotos=causa_urgente.fotos)

    @strawberry.mutation
    async def actualizar_causa_urgente(self, input: UpdateCausaUrgenteInput) -> CausaUrgenteType:
        adapter = CausaUrgenteRepository()
        service = CausaUrgenteService(adapter)

        causa_actualizada = UpdateCausaUrgente(
            titulo=input.titulo,
            descripcion=input.descripcion,
            meta=input.meta,
            fecha_limite=input.fecha_limite,
            id_refugio=UUID(input.id_refugio) if input.id_refugio else None,
            id_animal=UUID(input.id_animal) if input.id_animal else None,
            fotos=input.fotos)
        
        causa_urgente = await service.actualizar_causa_urgente(causa_actualizada)
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

    @strawberry.mutation
    async def eliminar_causa_urgente(self, id_causa_urgente: strawberry.ID) -> bool:
        adapter = CausaUrgenteRepository()
        service = CausaUrgenteService(adapter)
        return await service.eliminar_causa_urgente(UUID(id_causa_urgente))