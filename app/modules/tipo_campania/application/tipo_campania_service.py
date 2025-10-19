from typing import List, Optional
from uuid import UUID
from app.modules.tipo_campania.domain.entities import TipoCampania, NewTipoCampania, UpdateTipoCampania
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

    async def crear(self, nuevo_tipo_campania: NewTipoCampania) -> TipoCampania:
        """Crea un nuevo tipo de campaña."""
        return await self.repo.crear_tipo_campania(nuevo_tipo_campania)

    async def actualizar(self, tipo_campania_actualizada: UpdateTipoCampania) -> Optional[TipoCampania]:
        """Actualiza un tipo de campaña existente."""
        return await self.repo.actualizar_tipo_campania(tipo_campania_actualizada)

    async def eliminar(self, id_tipo_campania: UUID) -> bool:
        """Elimina un tipo de campaña por su ID."""
        return await self.repo.eliminar_tipo_campania(id_tipo_campania)
