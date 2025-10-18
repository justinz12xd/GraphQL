import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.usuario.interface.graphql_type import UsuarioType
from app.modules.usuario.application.usuario_service import UsuarioService
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository


@strawberry.type
class UsuarioQuery:
    """Queries GraphQL para Usuario"""
    
    @strawberry.field
    async def usuarios(self) -> List[UsuarioType]:
        """Obtener todos los usuarios"""
        adapter = UsuarioRepository()
        service = UsuarioService(adapter)
        usuarios = await service.obtener_todos()
        
        return [
            UsuarioType(
                id_usuario=strawberry.ID(str(usuario.id_usuario)),
                nombre=usuario.nombre,
                email=usuario.email,
                telefono=usuario.telefono,
                direccion=usuario.direccion,
                fecha_registro=usuario.fecha_registro
            )
            for usuario in usuarios
        ]
    
    @strawberry.field
    async def usuario(self, id_usuario: strawberry.ID) -> Optional[UsuarioType]:
        """Obtener un usuario por ID"""
        adapter = UsuarioRepository()
        service = UsuarioService(adapter)
        usuario = await service.obtener_usuario_por_id(UUID(id_usuario))
        
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
