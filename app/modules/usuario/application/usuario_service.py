from app.modules.usuario.infrastructure.rest_adapter import UsuarioRESTAdapter
from app.modules.usuario.domain.entities import Usuario, NewUsuario, UpdateUsuario
from typing import List, Optional
from uuid import UUID


class UsuarioService:
    """Servicio de aplicación para gestionar usuarios"""
    
    def __init__(self, adapter: UsuarioRESTAdapter):
        self.adapter = adapter
    
    async def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        return await self.adapter.listar_usuarios()
    
    async def obtener_usuario_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        """Obtener un usuario por ID"""
        return await self.adapter.obtener_usuario_por_id(id_usuario)
    
    async def crear_usuario(self, nuevo_usuario: NewUsuario) -> Usuario:
        """Crear un nuevo usuario"""
        # Aquí podrías agregar validaciones de negocio antes de crear
        # Por ejemplo: validar formato de email, verificar que no exista, etc.
        return await self.adapter.crear_usuario(nuevo_usuario)
    
    async def actualizar_usuario(self, usuario_actualizado: UpdateUsuario) -> Optional[Usuario]:
        """Actualizar un usuario existente"""
        # Aquí podrías agregar validaciones de negocio
        return await self.adapter.actualizar_usuario(usuario_actualizado)
    
    async def eliminar_usuario(self, id_usuario: UUID) -> bool:
        """Eliminar un usuario"""
        return await self.adapter.eliminar_usuario(id_usuario)