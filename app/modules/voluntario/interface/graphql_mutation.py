import strawberry
from typing import Optional
from uuid import UUID
from app.modules.voluntario.interface.graphql_type import VoluntarioType, CreateVoluntarioInput, UpdateVoluntarioInput
from app.modules.voluntario.application.voluntario_service import VoluntarioService
from app.modules.voluntario.domain.entities import NewVoluntario, UpdateVoluntario
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository

@strawberry.type
class VoluntarioMutation:
    """Mutations GraphQL para Voluntario"""

    @strawberry.mutation
    async def crear_voluntario(self, input: CreateVoluntarioInput) -> VoluntarioType:
        """Crear un nuevo voluntario"""
        service = VoluntarioService()
        
        nuevo_voluntario = NewVoluntario(
            rol=input.rol,
            estado=input.estado,
            id_usuario=input.id_usuario,
            id_campania=input.id_campania
        )
        
        voluntario = await service.crear_voluntario(nuevo_voluntario)
        
        return VoluntarioType(
            id_voluntario=voluntario.id_voluntario,
            rol=voluntario.rol,
            estado=voluntario.estado,
            id_usuario=voluntario.id_usuario,
            id_campania=voluntario.id_campania
        )
    
    @strawberry.mutation
    async def actualizar_voluntario(self, id_voluntario: strawberry.ID, input: UpdateVoluntarioInput) -> Optional[VoluntarioType]:
        """Actualizar un voluntario existente"""
        service = VoluntarioService()
        
        voluntario_actualizado = UpdateVoluntario(
            rol=input.rol,
            estado=input.estado,
            id_usuario=input.id_usuario,
            id_campania=input.id_campania
        )
        
        voluntario = await service.actualizar_voluntario(voluntario_actualizado, UUID(id_voluntario))
        
        if voluntario is None:
            return None
        
        return VoluntarioType(
            id_voluntario=voluntario.id_voluntario,
            rol=voluntario.rol,
            estado=voluntario.estado,
            id_usuario=voluntario.id_usuario,
            id_campania=voluntario.id_campania
        )
    
    @strawberry.mutation
    async def eliminar_voluntario(self, id_voluntario: strawberry.ID) -> bool:
        """Eliminar un voluntario por su ID"""
        service = VoluntarioService()
        resultado = await service.eliminar_voluntario(UUID(id_voluntario))
        return resultado