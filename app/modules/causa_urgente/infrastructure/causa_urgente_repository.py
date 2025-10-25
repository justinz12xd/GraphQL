import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.causa_urgente.domain.entities import CausaUrgente, NewCausaUrgente, UpdateCausaUrgente

class CausaUrgenteRepository:
    """Repositorio para gestionar causas urgentes mediante REST API"""

    def __init__(self):
        self.base_url = settings.REST_API_URL
        self.timeout = 30

    async def _get_client(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asíncrono"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
    
    def _parse_causa_urgente(self, data: dict) -> CausaUrgente:
        """Convierte la respuesta del API REST en una entidad CausaUrgente"""
        return CausaUrgente(
            id_causa_urgente=UUID(data["id_causa_urgente"]) if isinstance(data["id_causa_urgente"], str) else data["id_causa_urgente"], 
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            meta=data.get("meta"),
            fecha_limite=datetime.fromisoformat(data["fecha_limite"].replace("Z", "+00:00")) if isinstance(data["fecha_limite"], str) else data["fecha_limite"],
            id_refugio=UUID(data["id_refugio"]) if data.get("id_refugio") and isinstance(data["id_refugio"], str) else data.get("id_refugio"),
            id_animal=UUID(data["id_animal"]) if data.get("id_animal") and isinstance(data["id_animal"], str) else data.get("id_animal"),
            fotos=data.get("fotos"),
        )
    
    async def obtener_causas_urgentes(self) -> list[CausaUrgente]:
        """GET /causas_urgentes - Obtener todas las causas urgentes"""
        async with await self._get_client() as client:
            response = await client.get("/causas_urgentes")
            response.raise_for_status()
            causas_urgentes_data = response.json()
            return [self._parse_causa_urgente(data) for data in causas_urgentes_data]
    
    async def obtener_causa_urgente_por_id(self, id_causa_urgente: UUID) -> Optional[CausaUrgente]:
        """GET /causas_urgentes/{id} - Obtener una causa urgente por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/causas_urgentes/{str(id_causa_urgente)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_causa_urgente(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise