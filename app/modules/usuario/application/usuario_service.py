from typing import List, Optional
from uuid import UUID
from app.modules.usuario.domain.entities import Usuario
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
