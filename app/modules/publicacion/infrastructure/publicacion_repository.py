import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.publicacion.domain.entities import Publicacion, NewPublicacion, UpdatePublicacion


class PublicacionRepository:
    """Repositorio para gestionar publicaciones mediante REST API

    Este adaptador sigue la misma convención que los demás módulos:
    - usa `settings.REST_API_URL` como base
    - trabaja con `httpx.AsyncClient`
    - transforma las respuestas en entidades del dominio
    """

    def __init__(self):
        self.base_url = settings.REST_API_URL
        self.timeout = 30

    async def _get_client(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asíncrono configurado"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )

    def _parse_publicacion(self, data: dict) -> Publicacion:
        """Convierte la respuesta del API REST en una entidad Publicacion"""
        return Publicacion(
            id_publicacion=UUID(data["id_publicacion"]) if isinstance(data["id_publicacion"], str) else data["id_publicacion"],
            titulo=data.get("titulo"),
            descripcion=data.get("descripcion"),
            fecha_publicacion=(datetime.fromisoformat(data["fecha_publicacion"].replace("Z", "+00:00"))
                              if isinstance(data.get("fecha_publicacion"), str) else data.get("fecha_publicacion")),
            estado=data.get("estado"),
            id_usuario=UUID(data.get("id_usuario")) if data.get("id_usuario") and isinstance(data.get("id_usuario"), str) else data.get("id_usuario")
        )

    async def listar_publicaciones(self) -> list[Publicacion]:
        """GET /publicaciones - Obtener todas las publicaciones"""
        async with await self._get_client() as client:
            response = await client.get("/publicaciones")
            response.raise_for_status()
            publicaciones_data = response.json()
            return [self._parse_publicacion(data) for data in publicaciones_data]

    async def obtener_publicacion_por_id(self, id_publicacion: UUID) -> Optional[Publicacion]:
        """GET /publicaciones/{id} - Obtener una publicación por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/publicaciones/{str(id_publicacion)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_publicacion(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def crear_publicacion(self, nueva_publicacion: NewPublicacion) -> Publicacion:
        """POST /publicaciones - Crear una nueva publicación"""
        async with await self._get_client() as client:
            payload = {
                "titulo": nueva_publicacion.titulo,
                "descripcion": nueva_publicacion.descripcion,
                "fecha_publicacion": nueva_publicacion.fecha_publicacion.isoformat(),
                "estado": nueva_publicacion.estado,
                "id_usuario": str(nueva_publicacion.id_usuario) if nueva_publicacion.id_usuario else None
            }
            response = await client.post("/publicaciones", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_publicacion(data)

    async def actualizar_publicacion(self, publicacion_actualizada: UpdatePublicacion) -> Optional[Publicacion]:
        """PUT /publicaciones/{id} - Actualizar una publicación"""
        async with await self._get_client() as client:
            payload = {}

            if publicacion_actualizada.titulo is not None:
                payload["titulo"] = publicacion_actualizada.titulo
            if publicacion_actualizada.descripcion is not None:
                payload["descripcion"] = publicacion_actualizada.descripcion
            if publicacion_actualizada.fecha_publicacion is not None:
                payload["fecha_publicacion"] = publicacion_actualizada.fecha_publicacion.isoformat()
            if publicacion_actualizada.estado is not None:
                payload["estado"] = publicacion_actualizada.estado
            if publicacion_actualizada.id_usuario is not None:
                payload["id_usuario"] = str(publicacion_actualizada.id_usuario)

            try:
                response = await client.put(
                    f"/publicaciones/{str(publicacion_actualizada.id_publicacion)}",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_publicacion(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def eliminar_publicacion(self, id_publicacion: UUID) -> bool:
        """DELETE /publicaciones/{id} - Eliminar una publicación"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/publicaciones/{str(id_publicacion)}")
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise
