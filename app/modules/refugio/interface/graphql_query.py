import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.refugio.interface.graphql_type import RefugioType
from app.modules.refugio.application.refugio_service import RefugioService
from app.modules.refugio.infrastructure.refugio_repository import RefugioRepository


@strawberry.type
class RefugioQuery:
    """Queries GraphQL para Refugio"""

    @strawberry.field
    async def refugios(self) -> List[RefugioType]:
        """Obtener todos los refugios"""
        adapter = RefugioRepository()
        service = RefugioService(adapter)
        refugios = await service.obtener_todos()

        return [
            RefugioType(
                id_refugio=strawberry.ID(str(r.id_refugio)),
                nombre=r.nombre,
                direccion=r.direccion,
                telefono=r.telefono,
                capacidad=r.capacidad,
                estado=r.estado,
                fecha_creacion=r.fecha_creacion,
            )
            for r in refugios
        ]

    @strawberry.field
    async def refugio(self, id_refugio: strawberry.ID) -> Optional[RefugioType]:
        """Obtener un refugio por ID"""
        adapter = RefugioRepository()
        service = RefugioService(adapter)
        refugio = await service.obtener_refugio_por_id(UUID(id_refugio))

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
