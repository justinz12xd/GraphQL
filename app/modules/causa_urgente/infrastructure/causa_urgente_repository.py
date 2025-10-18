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
    
    async def listar_causas_urgentes(self) -> list[CausaUrgente]:
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
    
    async def crear_causa_urgente(self, nueva_causa_urgente: NewCausaUrgente) -> CausaUrgente:
        """POST /causas_urgentes - Crear una nueva causa urgente"""
        async with await self._get_client() as client:
            payload = {
                "titulo": nueva_causa_urgente.titulo,
                "descripcion": nueva_causa_urgente.descripcion,
                "meta": nueva_causa_urgente.meta,
                "fecha_limite": nueva_causa_urgente.fecha_limite,
                "id_refugio": nueva_causa_urgente.id_refugio,
                "id_animal": nueva_causa_urgente.id_animal,
                "fotos": nueva_causa_urgente.fotos,
            }
            response = await client.post("/causas_urgentes", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_causa_urgente(data)
    
    async def actualizar_causa_urgente(self, id_causa_urgente: UUID, causa_urgente_actualizada: UpdateCausaUrgente) -> Optional[CausaUrgente]:
        """PUT /causas_urgentes/{id} - Actualizar una causa urgente"""
        async with await self._get_client() as client:
            payload = {
                "titulo": causa_urgente_actualizada.titulo,
                "descripcion": causa_urgente_actualizada.descripcion,
                "meta": causa_urgente_actualizada.meta,
                "fecha_limite": causa_urgente_actualizada.fecha_limite,
                "id_refugio": causa_urgente_actualizada.id_refugio,
                "id_animal": causa_urgente_actualizada.id_animal,
                "fotos": causa_urgente_actualizada.fotos,
            }
            response = await client.put(f"/causas_urgentes/{str(id_causa_urgente)}", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_causa_urgente(data)
    
    async def eliminar_causa_urgente(self, id_causa_urgente: UUID) -> bool:
        """DELETE /causas_urgentes/{id} - Eliminar una causa urgente"""
        async with await self._get_client() as client:
            response = await client.delete(f"/causas_urgentes/{str(id_causa_urgente)}")
            response.raise_for_status()
            return True