from typing import List, Optional
from uuid import UUID
from app.modules.pago.domain.entitie import Pago
from app.modules.pago.infrastructure.pago_repository import PagoRepository

class PagoApplicationService:
    def __init__(self):
        self.repo = PagoRepository()

    async def obtener_pago(self, id_pago: UUID) -> Optional[Pago]:
        return await self.repo.obtener_pago(id_pago)

    async def listar_pagos(self, limit: int = 50, offset: int = 0) -> List[Pago]:
        return await self.repo.listar_pagos(limit, offset)

    async def obtener_pagos_por_donacion(self, id_donacion: UUID) -> List[Pago]:
        return await self.repo.obtener_pagos_por_donacion(id_donacion)