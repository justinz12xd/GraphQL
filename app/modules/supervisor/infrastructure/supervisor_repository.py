import httpx
from typing import Optional
from uuid import UUID
from app.config.settings import settings
from app.modules.supervisor.domain.entities import Supervisor, NewSupervisor, UpdateSupervisor

class SupervisorRepository:
    """Repositorio para gestionar supervisores mediante REST API"""

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
    
    def _parse_supervisor(self, data: dict) -> Supervisor:
        """Convierte la respuesta de la API REST en una entidad Supervisor"""
        return Supervisor(
            id_supervisor=UUID(data["id_supervisor"]) if isinstance(data["id_supervisor"], str) else data["id_supervisor"],
            nombre=data["nombre"],
            total_animales=data["total_animales"],
            id_refugio=UUID(data["id_refugio"]) if data.get("id_refugio") and isinstance(data["id_refugio"], str) else data.get("id_refugio"),
            id_usuario=UUID(data["id_usuario"]) if data.get("id_usuario") and isinstance(data["id_usuario"], str) else data.get("id_usuario"),
        )
    
    async def listar_supervisores(self) -> list[Supervisor]:
        """GET /supervisores - Obtener todos los supervisores"""
        async with await self._get_client() as client:
            response = await client.get("/supervisores")
            response.raise_for_status()
            supervisores_data = response.json()
            return [self._parse_supervisor(data) for data in supervisores_data]
        
    async def obtener_supervisor_por_id(self, id_supervisor: UUID) -> Optional[Supervisor]:
        """GET /supervisores/{id} - Obtener un supervisor por ID"""
        async with await self._get_client() as client: 
            try: 
                response = await client.get(f"/supervisores/{str(id_supervisor)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_supervisor(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def crear_supervisor(self, nuevo_supervisor: NewSupervisor) -> Supervisor:
        """POST /supervisores - Crear un nuevo supervisor"""
        async with await self._get_client() as client:
            payload = {
                "nombre": nuevo_supervisor.nombre,
                "total_animales": nuevo_supervisor.total_animales,
                "id_refugio": str(nuevo_supervisor.id_refugio) if nuevo_supervisor.id_refugio else None,
                "id_usuario": str(nuevo_supervisor.id_usuario) if nuevo_supervisor.id_usuario else None
            }
            response = await client.post("/supervisores", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_supervisor(data)
        

    async def actualizar_supervisor(self, supervisor_actualizado: UpdateSupervisor, id_supervisor: UUID) -> Optional[Supervisor]:
        """PUT /supervisores/{id} - Actualizar un supervisor existente"""
        async with await self._get_client() as client:
            payload = {}
            if supervisor_actualizado.nombre is not None:
                payload["nombre"] = supervisor_actualizado.nombre
            if supervisor_actualizado.total_animales is not None:
                payload["total_animales"] = supervisor_actualizado.total_animales
            if supervisor_actualizado.id_refugio is not None:
                payload["id_refugio"] = str(supervisor_actualizado.id_refugio)
            if supervisor_actualizado.id_usuario is not None:
                payload["id_usuario"] = str(supervisor_actualizado.id_usuario)
            try:
                response = await client.put(f"/supervisores/{str(id_supervisor)}", json=payload)
                response.raise_for_status()
                data = response.json()
                return self._parse_supervisor(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def eliminar_supervisor(self, id_supervisor: UUID) -> bool:
        """DELETE /supervisores/{id} - Eliminar un supervisor por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/supervisores/{str(id_supervisor)}")
                response.raise_for_status()
                return response.status_code == 204
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise

