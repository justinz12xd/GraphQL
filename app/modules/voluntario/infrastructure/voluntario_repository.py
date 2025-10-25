import httpx
from typing import Optional
from uuid import UUID
from app.config.settings import settings
from app.modules.voluntario.domain.entities import Voluntario, NewVoluntario, UpdateVoluntario

class VoluntarioRepository:
    """Repositorio para gestionar voluntarios mediante REST API"""

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
    
    def _parse_voluntario(self, data: dict) -> Voluntario:
        """Convierte la respuesta de la API REST en una entidad Voluntario"""
        return Voluntario(
            id_voluntario=UUID(data["id_voluntario"]) if isinstance(data["id_voluntario"], str) else data["id_voluntario"],
            rol=data["rol"],
            estado=data["estado"],
            id_usuario=UUID(data["id_usuario"]) if data.get("id_usuario") and isinstance(data["id_usuario"], str) else data.get("id_usuario"),
            id_campania=UUID(data["id_campania"]) if data.get("id_campania") and isinstance(data["id_campania"], str) else data.get("id_campania"),
        )
    
    async def listar_voluntarios(self) -> list[Voluntario]:
        """GET /voluntarios - Obtener todos los voluntarios"""
        async with await self._get_client() as client:
            response = await client.get("/voluntarios")
            response.raise_for_status()
            voluntarios_data = response.json()
            return [self._parse_voluntario(data) for data in voluntarios_data]
        
    async def obtener_voluntario_por_id(self, id_voluntario: UUID) -> Optional[Voluntario]:
        """GET /voluntarios/{id} - Obtener un voluntario por ID"""
        async with await self._get_client() as client: 
            try: 
                response = await client.get(f"/voluntarios/{str(id_voluntario)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_voluntario(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise