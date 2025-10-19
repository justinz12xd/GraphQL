import httpx
from typing import Optional
from uuid import UUID
from app.config.settings import settings
from app.modules.tipo_campania.domain.entities import TipoCampania, NewTipoCampania, UpdateTipoCampania

class TipoCampaniaRepository:
    """Repositorio para gestionar tipos de campaña mediante Rest API"""

    def __init__(self):
        self.base_url = settings.REST_API_URL
        self.timeout = 30
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asincrono"""
        return httpx.AsyncClient(
            base_url = self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
    
    def _parse_tipo_campania(self, data: dict) -> TipoCampania:
        """Convierte la respuesta de la API REST en una entidad TipoCampania"""
        return TipoCampania(
            id_tipo_campania=UUID(data["id_tipo_campania"]) if isinstance(data["id_tipo_campania"], str) else data["id_tipo_campania"],
            nombre=data["nombre"],
            descripcion=data.get("descripcion")
        )
    
    async def listar_tipos_campania(self) -> list[TipoCampania]:
        """GET /tipo_campanias - Obtener todos los tipos campania"""
        async with await self._get_client() as client:
            response = await client.get("/tipo_campanias")
            response.raise_for_status()
            tipos_campania_data = response.json()
            return [self._parse_tipo_campania(data) for data in tipos_campania_data]
        
    async def obtener_tipo_campania_por_id(self, id_tipo_campania: UUID) -> Optional[TipoCampania]:
        """GET /tipo_campanias/{id} - Obtener un tipo campania por ID"""
        async with await self._get_client() as client: 
            try: 
                response = await client.get(f"/tipo_campanias/{str(id_tipo_campania)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_tipo_campania(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
        
    async def crear_tipo_campania(self, nuevo_tipo_campania: NewTipoCampania) -> TipoCampania:
        """POST /tipo_campanias - Crear un nuevo tipo campania"""
        async with await self._get_client() as client:
            payload = {
                "nombre": nuevo_tipo_campania.nombre,
                "descripcion": nuevo_tipo_campania.descripcion
            }
            response = await client.post("/tipo_campanias", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_tipo_campania(data)
    
    async def actualizar_tipo_campania(self, tipo_campania_actualizada: UpdateTipoCampania) -> Optional[TipoCampania]:
        """PUT /tipo_campanias/{id} - Actualizar un tipo campania existente"""
        async with await self._get_client() as client:
            payload = {}
            if tipo_campania_actualizada.nombre is not None:
                payload["nombre"] = tipo_campania_actualizada.nombre
            if tipo_campania_actualizada.descripcion is not None:
                payload["descripcion"] = tipo_campania_actualizada.descripcion
            try:
                response = await client.put(f"/tipo_campanias/{str(tipo_campania_actualizada.id_tipo_campania)}", json=payload)
                response.raise_for_status()
                data = response.json()
                return self._parse_tipo_campania(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def eliminar_tipo_campania(self, id_tipo_campania: UUID) -> bool:
        """DELETE /tipo_campanias/{id} - Eliminar un tipo campania por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/tipo_campanias/{str(id_tipo_campania)}")
                response.raise_for_status()
                return response.status_code == 204
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise
