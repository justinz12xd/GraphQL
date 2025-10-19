import strawberry
from typing import Optional
from uuid import UUID
from app.modules.supervisor.interface.graphql_type import SupervisorType, CreateSupervisorInput, UpdateSupervisorInput
from app.modules.supervisor.application.supervisor_service import SupervisorService
from app.modules.supervisor.domain.entities import NewSupervisor, UpdateSupervisor
from app.modules.supervisor.infrastructure.supervisor_repository import SupervisorRepository

@strawberry.type
class SupervisorMutation:
    """Mutations GraphQL para Supervisor"""

    @strawberry.mutation
    async def crear_supervisor(self, input: CreateSupervisorInput) -> SupervisorType:
        """Crear un nuevo supervisor"""
        service = SupervisorService()
        
        nuevo_supervisor = NewSupervisor(
            nombre=input.nombre,
            total_animales=input.total_animales,
            id_refugio=input.id_refugio,
            id_usuario=input.id_usuario
        )
        
        supervisor = await service.crear_supervisor(nuevo_supervisor)
        
        return SupervisorType(
            id_supervisor=supervisor.id_supervisor,
            nombre=supervisor.nombre,
            total_animales=supervisor.total_animales,
            id_refugio=supervisor.id_refugio,
            id_usuario=supervisor.id_usuario
        )
    
    @strawberry.mutation
    async def actualizar_supervisor(self, id_supervisor: strawberry.ID, input: UpdateSupervisorInput) -> Optional[SupervisorType]:
        """Actualizar un supervisor existente"""
        service = SupervisorService()
        
        supervisor_actualizado = UpdateSupervisor(
            nombre=input.nombre,
            total_animales=input.total_animales,
            id_refugio=input.id_refugio,
            id_usuario=input.id_usuario
        )
        
        supervisor = await service.actualizar_supervisor(supervisor_actualizado, UUID(id_supervisor))
        
        if supervisor is None:
            return None
        
        return SupervisorType(
            id_supervisor=supervisor.id_supervisor,
            nombre=supervisor.nombre,
            total_animales=supervisor.total_animales,
            id_refugio=supervisor.id_refugio,
            id_usuario=supervisor.id_usuario
        )
    
    @strawberry.mutation
    async def eliminar_supervisor(self, id_supervisor: strawberry.ID) -> bool:
        """Eliminar un supervisor por ID"""
        service = SupervisorService()
        resultado = await service.eliminar_supervisor(UUID(id_supervisor))
        return resultado
    