import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.adopcion.domain.entities import Adopcion, NewAdopcion, UpdateAdopcion


class AdopcionRepository:
    """Repositorio para gestionar adopciones mediante REST API"""
    
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
    
    def _parse_adopcion(self, data: dict) -> Adopcion:
        """Convierte la respuesta del API REST en una entidad Adopcion"""
        return Adopcion(
            id_adopcion=UUID(data["id_adopcion"]) if isinstance(data["id_adopcion"], str) else data["id_adopcion"],
            fecha_adopcion=datetime.fromisoformat(data["fecha_adopcion"].replace("Z", "+00:00")) 
                          if isinstance(data["fecha_adopcion"], str) 
                          else data["fecha_adopcion"],
            estado=data["estado"],
            id_publicacion=UUID(data["id_publicacion"]) if data.get("id_publicacion") and isinstance(data["id_publicacion"], str) else data.get("id_publicacion"),
            id_usuario=UUID(data["id_usuario"]) if data.get("id_usuario") and isinstance(data["id_usuario"], str) else data.get("id_usuario")
        )
    
    async def listar_adopciones(self) -> list[Adopcion]:
        """GET /adopciones - Obtener todas las adopciones"""
        async with await self._get_client() as client:
            response = await client.get("/adopciones")
            response.raise_for_status()
            adopciones_data = response.json()
            return [self._parse_adopcion(data) for data in adopciones_data]
    
    async def obtener_adopcion_por_id(self, id_adopcion: UUID) -> Optional[Adopcion]:
        """GET /adopciones/{id} - Obtener una adopción por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/adopciones/{str(id_adopcion)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_adopcion(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
