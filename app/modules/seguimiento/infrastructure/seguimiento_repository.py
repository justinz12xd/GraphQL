import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.seguimiento.domain.entities import Seguimiento, NewSeguimiento, UpdateSeguimiento


class SeguimientoRepository:
    """Repositorio para gestionar seguimientos mediante REST API"""

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

    def _parse_seguimiento(self, data: dict) -> Seguimiento:
        """Convierte la respuesta del API REST en una entidad Seguimiento"""
        return Seguimiento(
            id_seguimiento=UUID(data["id_seguimiento"]) if isinstance(data["id_seguimiento"], str) else data["id_seguimiento"],
            fecha=(datetime.fromisoformat(data["fecha"].replace("Z", "+00:00")) if isinstance(data.get("fecha"), str) else data.get("fecha")),
            descripcion=data.get("descripcion"),
            tipo=data.get("tipo"),
            id_referencia=UUID(data.get("id_referencia")) if data.get("id_referencia") and isinstance(data.get("id_referencia"), str) else data.get("id_referencia"),
            id_usuario=UUID(data.get("id_usuario")) if data.get("id_usuario") and isinstance(data.get("id_usuario"), str) else data.get("id_usuario"),
        )

    async def listar_seguimientos(self) -> list[Seguimiento]:
        """GET /seguimientos - Obtener todos los seguimientos"""
        async with await self._get_client() as client:
            response = await client.get("/seguimientos")
            response.raise_for_status()
            datos = response.json()
            return [self._parse_seguimiento(d) for d in datos]

    async def obtener_seguimiento_por_id(self, id_seguimiento: UUID) -> Optional[Seguimiento]:
        """GET /seguimientos/{id} - Obtener un seguimiento por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/seguimientos/{str(id_seguimiento)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_seguimiento(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
