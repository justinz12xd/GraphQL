import strawberry
from typing import Optional, List
from uuid import UUID
from app.modules.supervisor.interface.graphql_type import SupervisorType
from app.modules.supervisor.application.supervisor_service import SupervisorService
from app.modules.supervisor.infrastructure.supervisor_repository import SupervisorRepository

@strawberry.type
class SupervisorQuery:
    """Queries GraphQL para Supervisor"""

    @strawberry.field
    async def supervisores(self) -> List[SupervisorType]:
        """Obtener todos los supervisores"""
        service = SupervisorService()
        supervisores = await service.listar_supervisores()
        return [SupervisorType(
            id_supervisor=supervisor.id_supervisor,
            nombre=supervisor.nombre,
            total_animales=supervisor.total_animales,
            id_refugio=supervisor.id_refugio,
            id_usuario=supervisor.id_usuario) for supervisor in supervisores]

    @strawberry.field
    async def supervisor_por_id(self, id_supervisor: strawberry.ID) -> Optional[SupervisorType]:
        """Obtener un supervisor por ID"""
        service = SupervisorService()
        supervisor = await service.obtener_supervisor_por_id(UUID(id_supervisor))
        if supervisor is None:
            return None
        return SupervisorType(
            id_supervisor=supervisor.id_supervisor,
            nombre=supervisor.nombre,
            total_animales=supervisor.total_animales,
            id_refugio=supervisor.id_refugio,
            id_usuario=supervisor.id_usuario)