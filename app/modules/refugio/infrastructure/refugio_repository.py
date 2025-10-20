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

    async def crear_refugio(self, nuevo_refugio: NewRefugio) -> Refugio:
        """POST /refugios - Crear un nuevo refugio"""
        async with await self._get_client() as client:
            payload = {
                "nombre": nuevo_refugio.nombre,
                "direccion": nuevo_refugio.direccion,
                "telefono": nuevo_refugio.telefono,
                "capacidad": nuevo_refugio.capacidad,
                "estado": nuevo_refugio.estado,
                "fecha_creacion": nuevo_refugio.fecha_creacion.isoformat(),
            }
            response = await client.post("/refugios", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_refugio(data)

    async def actualizar_refugio(self, refugio_actualizado: UpdateRefugio) -> Optional[Refugio]:
        """PUT /refugios/{id} - Actualizar un refugio"""
        async with await self._get_client() as client:
            payload = {}

            if refugio_actualizado.nombre is not None:
                payload["nombre"] = refugio_actualizado.nombre
            if refugio_actualizado.direccion is not None:
                payload["direccion"] = refugio_actualizado.direccion
            if refugio_actualizado.telefono is not None:
                payload["telefono"] = refugio_actualizado.telefono
            if refugio_actualizado.capacidad is not None:
                payload["capacidad"] = refugio_actualizado.capacidad
            if refugio_actualizado.estado is not None:
                payload["estado"] = refugio_actualizado.estado
            if refugio_actualizado.fecha_creacion is not None:
                payload["fecha_creacion"] = refugio_actualizado.fecha_creacion.isoformat()

            try:
                response = await client.put(
                    f"/refugios/{str(refugio_actualizado.id_refugio)}",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_refugio(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def eliminar_refugio(self, id_refugio: UUID) -> bool:
        """DELETE /refugios/{id} - Eliminar un refugio"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/refugios/{str(id_refugio)}")
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise
