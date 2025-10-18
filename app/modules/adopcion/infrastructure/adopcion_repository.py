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
    
    async def crear_adopcion(self, nueva_adopcion: NewAdopcion) -> Adopcion:
        """POST /adopciones - Crear una nueva adopción"""
        async with await self._get_client() as client:
            payload = {
                "fecha_adopcion": nueva_adopcion.fecha_adopcion.isoformat(),
                "estado": nueva_adopcion.estado,
                "id_publicacion": str(nueva_adopcion.id_publicacion) if nueva_adopcion.id_publicacion else None,
                "id_usuario": str(nueva_adopcion.id_usuario) if nueva_adopcion.id_usuario else None
            }
            response = await client.post("/adopciones", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_adopcion(data)
    
    async def actualizar_adopcion(self, adopcion_actualizada: UpdateAdopcion) -> Optional[Adopcion]:
        """PUT /adopciones/{id} - Actualizar una adopción"""
        async with await self._get_client() as client:
            payload = {}
            
            if adopcion_actualizada.fecha_adopcion is not None:
                payload["fecha_adopcion"] = adopcion_actualizada.fecha_adopcion.isoformat()
            if adopcion_actualizada.estado is not None:
                payload["estado"] = adopcion_actualizada.estado
            if adopcion_actualizada.id_publicacion is not None:
                payload["id_publicacion"] = str(adopcion_actualizada.id_publicacion)
            if adopcion_actualizada.id_usuario is not None:
                payload["id_usuario"] = str(adopcion_actualizada.id_usuario)
            
            try:
                response = await client.put(
                    f"/adopciones/{str(adopcion_actualizada.id_adopcion)}", 
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_adopcion(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
    
    async def eliminar_adopcion(self, id_adopcion: UUID) -> bool:
        """DELETE /adopciones/{id} - Eliminar una adopción"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/adopciones/{str(id_adopcion)}")
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise
