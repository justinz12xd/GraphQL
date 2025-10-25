from typing import List, Optional
from uuid import UUID
from app.modules.tipo_campania.domain.entities import TipoCampania
from app.modules.tipo_campania.infrastructure.tipo_campania_repository import TipoCampaniaRepository

class TipoCampaniaService:
    """Servicio de aplicacion que orquesta la logica de negocio de los usuarios"""

    def __init__(self, repo: TipoCampaniaRepository):
        """Recibe el repositorio como dependencia externa."""
        self.repo = repo

    async def obtener_todos(self) -> List[TipoCampania]:
        """Obtiene todos los tipos de campaña."""
        return await self.repo.listar_tipos_campania()

    async def obtener_por_id(self, id_tipo_campania: UUID) -> Optional[TipoCampania]:
        """Obtiene un tipo de campaña por su ID."""
        return await self.repo.obtener_tipo_campania_por_id(id_tipo_campania)
