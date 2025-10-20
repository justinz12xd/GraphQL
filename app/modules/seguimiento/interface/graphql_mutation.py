import strawberry
from typing import Optional
from uuid import UUID
from app.modules.seguimiento.interface.graphql_type import SeguimientoType, CreateSeguimientoInput, UpdateSeguimientoInput
from app.modules.seguimiento.application.seguimiento_service import SeguimientoService
from app.modules.seguimiento.infrastructure.seguimiento_repository import SeguimientoRepository
from app.modules.seguimiento.domain.entities import NewSeguimiento, UpdateSeguimiento


@strawberry.type
class SeguimientoMutation:
    """Mutations GraphQL para Seguimiento"""

    @strawberry.mutation
    async def crear_seguimiento(self, input: CreateSeguimientoInput) -> SeguimientoType:
        """Crear un nuevo seguimiento"""
        adapter = SeguimientoRepository()
        service = SeguimientoService(adapter)

        nuevo_seguimiento = NewSeguimiento(
            fecha=input.fecha,
            descripcion=input.descripcion,
            tipo=input.tipo,
            id_referencia=UUID(input.id_referencia) if input.id_referencia else None,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None,
        )

        seguimiento = await service.crear_seguimiento(nuevo_seguimiento)

        return SeguimientoType(
            id_seguimiento=strawberry.ID(str(seguimiento.id_seguimiento)),
            fecha=seguimiento.fecha,
            descripcion=seguimiento.descripcion,
            tipo=seguimiento.tipo,
            id_referencia=strawberry.ID(str(seguimiento.id_referencia)) if seguimiento.id_referencia else None,
            id_usuario=strawberry.ID(str(seguimiento.id_usuario)) if seguimiento.id_usuario else None,
        )

    @strawberry.mutation
    async def actualizar_seguimiento(self, input: UpdateSeguimientoInput) -> Optional[SeguimientoType]:
        """Actualizar un seguimiento existente"""
        adapter = SeguimientoRepository()
        service = SeguimientoService(adapter)

        seguimiento_actualizado = UpdateSeguimiento(
            id_seguimiento=UUID(input.id_seguimiento),
            fecha=input.fecha,
            descripcion=input.descripcion,
            tipo=input.tipo,
            id_referencia=UUID(input.id_referencia) if input.id_referencia else None,
            id_usuario=UUID(input.id_usuario) if input.id_usuario else None,
        )

        seguimiento = await service.actualizar_seguimiento(seguimiento_actualizado)

        if seguimiento is None:
            return None

        return SeguimientoType(
            id_seguimiento=strawberry.ID(str(seguimiento.id_seguimiento)),
            fecha=seguimiento.fecha,
            descripcion=seguimiento.descripcion,
            tipo=seguimiento.tipo,
            id_referencia=strawberry.ID(str(seguimiento.id_referencia)) if seguimiento.id_referencia else None,
            id_usuario=strawberry.ID(str(seguimiento.id_usuario)) if seguimiento.id_usuario else None,
        )

    @strawberry.mutation
    async def eliminar_seguimiento(self, id_seguimiento: strawberry.ID) -> bool:
        """Eliminar un seguimiento"""
        adapter = SeguimientoRepository()
        service = SeguimientoService(adapter)

        return await service.eliminar_seguimiento(UUID(id_seguimiento))
