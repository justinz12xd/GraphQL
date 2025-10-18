import strawberry
from typing import Optional
from uuid import UUID
from app.modules.usuario.interface.graphql_type import UsuarioType, CreateUsuarioInput, UpdateUsuarioInput
from app.modules.usuario.application.usuario_service import UsuarioService
from app.modules.usuario.infrastructure.rest_adapter import UsuarioRESTAdapter
from app.modules.usuario.domain.entities import NewUsuario, UpdateUsuario


@strawberry.type
class UsuarioMutation:
    """Mutations GraphQL para Usuario"""
    
    @strawberry.mutation
    async def crear_usuario(self, input: CreateUsuarioInput) -> UsuarioType:
        """Crear un nuevo usuario"""
        adapter = UsuarioRESTAdapter()
        service = UsuarioService(adapter)
        
        nuevo_usuario = NewUsuario(
            nombre=input.nombre,
            email=input.email,
            contrasenia=input.contrasenia,
            telefono=input.telefono,
            direccion=input.direccion
        )
        
        usuario = await service.crear_usuario(nuevo_usuario)
        
        return UsuarioType(
            id_usuario=strawberry.ID(str(usuario.id_usuario)),
            nombre=usuario.nombre,
            email=usuario.email,
            telefono=usuario.telefono,
            direccion=usuario.direccion,
            fecha_registro=usuario.fecha_registro
        )
    
    @strawberry.mutation
    async def actualizar_usuario(self, input: UpdateUsuarioInput) -> Optional[UsuarioType]:
        """Actualizar un usuario existente"""
        adapter = UsuarioRESTAdapter()
        service = UsuarioService(adapter)
        
        usuario_actualizado = UpdateUsuario(
            id_usuario=UUID(input.id_usuario),
            nombre=input.nombre,
            email=input.email,
            contrasenia=input.contrasenia,
            telefono=input.telefono,
            direccion=input.direccion
        )
        
        usuario = await service.actualizar_usuario(usuario_actualizado)
        
        if usuario is None:
            return None
        
        return UsuarioType(
            id_usuario=strawberry.ID(str(usuario.id_usuario)),
            nombre=usuario.nombre,
            email=usuario.email,
            telefono=usuario.telefono,
            direccion=usuario.direccion,
            fecha_registro=usuario.fecha_registro
        )
    
    @strawberry.mutation
    async def eliminar_usuario(self, id_usuario: strawberry.ID) -> bool:
        """Eliminar un usuario"""
        adapter = UsuarioRESTAdapter()
        service = UsuarioService(adapter)
        
        return await service.eliminar_usuario(UUID(id_usuario))
