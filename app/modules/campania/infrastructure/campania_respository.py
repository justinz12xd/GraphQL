import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.campania.domain.entitie import Campania, NewCampania, UpdateCampania

class CampaniaRepository:
    """Repositorio para gestionar campañas a través del backend REST"""
    
    def __init__(self):
        self.base_url = settings.REST_API_URL  # Solo la URL base sin /campanias
        self.timeout = 30

    async def _get_client(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asíncrono"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )

    def _parse_campania(self, data: dict) -> Campania:
        """Convierte la respuesta del API REST en una entidad Campania"""
        return Campania(
            id_campania=UUID(data["id_campania"]) if isinstance(data["id_campania"], str) else data["id_campania"],
            id_tipo_campania=UUID(data["id_tipo_campania"]) if isinstance(data["id_tipo_campania"], str) else data["id_tipo_campania"],
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            fecha_inicio=datetime.fromisoformat(data["fecha_inicio"]) if data.get("fecha_inicio") else None,
            fecha_fin=datetime.fromisoformat(data["fecha_fin"]) if data.get("fecha_fin") else None,
            lugar=data.get("lugar"),
            organizador=data.get("organizador"),
            estado=data.get("estado")
        )
    async def listar_campanias(self, limit: int = 50, offset: int = 0) -> list[Campania]:
        """GET /campanias - Obtener todas las campañas (sin paginación por ahora)"""
        async with await self._get_client() as client:
            # TEMPORAL: Removemos parámetros de paginación porque el backend no los soporta aún
            response = await client.get("/campanias")
            response.raise_for_status()
            campanias_data = response.json()
            
            # Aplicamos paginación manualmente en el lado del cliente
            campanias = [self._parse_campania(data) for data in campanias_data]
            start = offset
            end = offset + limit
            return campanias[start:end]
    async def obtener_campania_por_id(self, id_campania: UUID) -> Optional[Campania]:
        """GET /campanias/{id} - Obtener una campaña por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/campanias/{str(id_campania)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_campania(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

