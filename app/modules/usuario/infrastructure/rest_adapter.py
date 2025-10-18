import httpx
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.config.settings import REST_API_URL, HTTP_TIMEOUT
from app.modules.usuario.domain.entities import Usuario, NewUsuario, UpdateUsuario


class UsuarioRESTAdapter:
    """Adaptador para consumir la API REST de usuarios en Rust"""
    
    def __init__(self):
        self.base_url = REST_API_URL
        self.timeout = HTTP_TIMEOUT
    
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
            telefono=data.get("telefono"),
            direccion=data.get("direccion"),
            fecha_registro=datetime.fromisoformat(data["fecha_registro"].replace("Z", "+00:00")) 
                          if isinstance(data["fecha_registro"], str) 
                          else data["fecha_registro"]
        )
    
    async def listar_usuarios(self) -> List[Usuario]:
        """GET /usuarios - Obtener todos los usuarios"""
        async with await self._get_client() as client:
            response = await client.get("/usuarios")
            response.raise_for_status()
            data = response.json()
            return [self._parse_usuario(item) for item in data]
    
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
    
    async def crear_usuario(self, nuevo_usuario: NewUsuario) -> Usuario:
        """POST /usuarios - Crear un nuevo usuario"""
        async with await self._get_client() as client:
            payload = {
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "contrasenia": nuevo_usuario.contrasenia,
                "telefono": nuevo_usuario.telefono,
                "direccion": nuevo_usuario.direccion
            }
            response = await client.post("/usuarios", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_usuario(data)
    
    async def actualizar_usuario(self, usuario_actualizado: UpdateUsuario) -> Optional[Usuario]:
        """PUT /usuarios/{id} - Actualizar un usuario"""
        async with await self._get_client() as client:
            payload = {}
            if usuario_actualizado.nombre is not None:
                payload["nombre"] = usuario_actualizado.nombre
            if usuario_actualizado.email is not None:
                payload["email"] = usuario_actualizado.email
            if usuario_actualizado.contrasenia is not None:
                payload["contrasenia"] = usuario_actualizado.contrasenia
            if usuario_actualizado.telefono is not None:
                payload["telefono"] = usuario_actualizado.telefono
            if usuario_actualizado.direccion is not None:
                payload["direccion"] = usuario_actualizado.direccion
            
            try:
                response = await client.put(
                    f"/usuarios/{str(usuario_actualizado.id_usuario)}", 
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_usuario(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
    
    async def eliminar_usuario(self, id_usuario: UUID) -> bool:
        """DELETE /usuarios/{id} - Eliminar un usuario"""
        async with await self._get_client() as client:
            try:
                response = await client.delete(f"/usuarios/{str(id_usuario)}")
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise
