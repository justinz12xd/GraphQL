import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.seguimiento.interface.graphql_type import SeguimientoType
from app.modules.seguimiento.application.seguimiento_service import SeguimientoService
from app.modules.seguimiento.infrastructure.seguimiento_repository import SeguimientoRepository


@strawberry.type
class SeguimientoQuery:
    """Queries GraphQL para Seguimiento"""

    @strawberry.field
    async def seguimientos(self) -> List[SeguimientoType]:
        """Obtener todos los seguimientos"""
        adapter = SeguimientoRepository()
        service = SeguimientoService(adapter)
        seguimientos = await service.obtener_todos()

        return [
            SeguimientoType(
                id_seguimiento=strawberry.ID(str(s.id_seguimiento)),
                fecha=s.fecha,
                descripcion=s.descripcion,
                tipo=s.tipo,
                id_referencia=strawberry.ID(str(s.id_referencia)) if s.id_referencia else None,
                id_usuario=strawberry.ID(str(s.id_usuario)) if s.id_usuario else None,
            )
            for s in seguimientos
        ]

    @strawberry.field
    async def seguimiento(self, id_seguimiento: strawberry.ID) -> Optional[SeguimientoType]:
        """Obtener un seguimiento por ID"""
        adapter = SeguimientoRepository()
        service = SeguimientoService(adapter)
        seguimiento = await service.obtener_seguimiento_por_id(UUID(id_seguimiento))

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
