from typing import List, Optional
from uuid import UUID
from app.modules.usuario.domain.entities import Usuario, NewUsuario, UpdateUsuario
from app.modules.usuario.infrastructure.usuario_repository import UsuarioRepository

class UsuarioService:
    """Servicio de aplicación que orquesta la lógica de negocio de los usuarios."""

    def __init__(self, repo: UsuarioRepository):
        """Recibe el repositorio como dependencia externa."""
        self.repo = repo

    async def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        return await self.repo.listar_usuarios()

    async def obtener_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        return await self.repo.obtener_usuario_por_id(id_usuario)

    async def crear(self, nuevo_usuario: NewUsuario) -> Usuario:
        """Crea un nuevo usuario aplicando validaciones de negocio."""
        # Ejemplo: validar email o existencia previa
        return await self.repo.crear_usuario(nuevo_usuario)

    async def actualizar(self, id_usuario: UUID, datos: UpdateUsuario) -> Optional[Usuario]:
        """Actualiza un usuario existente."""
        return await self.repo.actualizar_usuario(id_usuario, datos)

    async def eliminar(self, id_usuario: UUID) -> bool:
        """Elimina un usuario."""
        return await self.repo.eliminar_usuario(id_usuario)
