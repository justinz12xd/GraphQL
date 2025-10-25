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
