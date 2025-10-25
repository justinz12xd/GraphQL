import httpx
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.usuario.domain.entities import Usuario, NewUsuario, UpdateUsuario


class UsuarioRepository:
    """Repositorio para gestionar usuarios mediante REST API"""
    
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
    
    def _parse_usuario(self, data: dict) -> Usuario:
        """Convierte la respuesta del API REST en una entidad Usuario"""
        return Usuario(
            id_usuario=UUID(data["id_usuario"]) if isinstance(data["id_usuario"], str) else data["id_usuario"],
            nombre=data["nombre"],
            email=data["email"],
            contrasenia=data["contrasenia"],
            fecha_registro=datetime.fromisoformat(data["fecha_registro"].replace("Z", "+00:00")) 
                          if isinstance(data["fecha_registro"], str) 
                          else data["fecha_registro"],
            telefono=data.get("telefono"),
            direccion=data.get("direccion")
        )
    
    async def listar_usuarios(self) -> list[Usuario]:
        """GET /usuarios - Obtener todos los usuarios"""
        async with await self._get_client() as client:
            response = await client.get("/usuarios")
            response.raise_for_status()
            usuarios_data = response.json()
            return [self._parse_usuario(data) for data in usuarios_data]
    
    async def obtener_usuario_por_id(self, id_usuario: UUID) -> Optional[Usuario]:
        """GET /usuarios/{id} - Obtener un usuario por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/usuarios/{str(id_usuario)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_usuario(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise