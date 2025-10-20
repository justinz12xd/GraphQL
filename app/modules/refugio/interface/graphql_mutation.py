import strawberry
from typing import Optional
from uuid import UUID
from app.modules.refugio.interface.graphql_type import RefugioType, CreateRefugioInput, UpdateRefugioInput
from app.modules.refugio.application.refugio_service import RefugioService
from app.modules.refugio.infrastructure.refugio_repository import RefugioRepository
from app.modules.refugio.domain.entities import NewRefugio, UpdateRefugio


@strawberry.type
class RefugioMutation:
    """Mutations GraphQL para Refugio"""

    @strawberry.mutation
    async def crear_refugio(self, input: CreateRefugioInput) -> RefugioType:
        """Crear un nuevo refugio"""
        adapter = RefugioRepository()
        service = RefugioService(adapter)

        nuevo_refugio = NewRefugio(
            nombre=input.nombre,
            direccion=input.direccion,
            telefono=input.telefono,
            capacidad=input.capacidad,
            estado=input.estado,
            fecha_creacion=input.fecha_creacion,
        )

        refugio = await service.crear_refugio(nuevo_refugio)

        return RefugioType(
            id_refugio=strawberry.ID(str(refugio.id_refugio)),
            nombre=refugio.nombre,
            direccion=refugio.direccion,
            telefono=refugio.telefono,
            capacidad=refugio.capacidad,
            estado=refugio.estado,
            fecha_creacion=refugio.fecha_creacion,
        )

    @strawberry.mutation
    async def actualizar_refugio(self, input: UpdateRefugioInput) -> Optional[RefugioType]:
        """Actualizar un refugio existente"""
        adapter = RefugioRepository()
        service = RefugioService(adapter)

        refugio_actualizado = UpdateRefugio(
            id_refugio=UUID(input.id_refugio),
            nombre=input.nombre,
            direccion=input.direccion,
            telefono=input.telefono,
            capacidad=input.capacidad,
            estado=input.estado,
            fecha_creacion=input.fecha_creacion,
        )

        refugio = await service.actualizar_refugio(refugio_actualizado)

        if refugio is None:
            return None

        return RefugioType(
            id_refugio=strawberry.ID(str(refugio.id_refugio)),
            nombre=refugio.nombre,
            direccion=refugio.direccion,
            telefono=refugio.telefono,
            capacidad=refugio.capacidad,
            estado=refugio.estado,
            fecha_creacion=refugio.fecha_creacion,
        )

    @strawberry.mutation
    async def eliminar_refugio(self, id_refugio: strawberry.ID) -> bool:
        """Eliminar un refugio"""
        adapter = RefugioRepository()
        service = RefugioService(adapter)

        return await service.eliminar_refugio(UUID(id_refugio))
