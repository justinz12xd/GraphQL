import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.refugio.domain.entities import Refugio, NewRefugio, UpdateRefugio


class RefugioRepository:
    """Repositorio para gestionar refugios mediante REST API"""

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

    def _parse_refugio(self, data: dict) -> Refugio:
        """Convierte la respuesta del API REST en una entidad Refugio"""
        return Refugio(
            id_refugio=UUID(data["id_refugio"]) if isinstance(data["id_refugio"], str) else data["id_refugio"],
            nombre=data.get("nombre"),
            direccion=data.get("direccion"),
            telefono=data.get("telefono"),
            capacidad=int(data.get("capacidad")) if data.get("capacidad") is not None else 0,
            estado=data.get("estado"),
            fecha_creacion=(datetime.fromisoformat(data["fecha_creacion"].replace("Z", "+00:00"))
                           if isinstance(data.get("fecha_creacion"), str) else data.get("fecha_creacion")),
        )

    async def listar_refugios(self) -> list[Refugio]:
        """GET /refugios - Obtener todos los refugios"""
        async with await self._get_client() as client:
            response = await client.get("/refugios")
            response.raise_for_status()
            refugios_data = response.json()
            return [self._parse_refugio(data) for data in refugios_data]

    async def obtener_refugio_por_id(self, id_refugio: UUID) -> Optional[Refugio]:
        """GET /refugios/{id} - Obtener un refugio por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/refugios/{str(id_refugio)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_refugio(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
