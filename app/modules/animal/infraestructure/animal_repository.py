import httpx
from typing import Optional
from uuid import UUID
from app.config.settings import settings
from app.modules.animal.domain.entities import Animal, NewAnimal, UpdateAnimal



class AnimalRepository:
    """Repositorio para gestionar animales mediante REST API"""
    
    def __init__(self):
        self.base_url = settings.REST_API_URL
        self.timeout = 30

    async def _get_animal(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asíncrono"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
    
    def _parse_animal(self, data: dict) -> Animal:
        """Convierte la respuesta del API REST en una entidad Animal"""
        return Animal(
            id_animal=UUID(data["id_animal"]) if isinstance(data["id_animal"], str) else data["id_animal"],
            nombre=data["nombre"],
            id_especie=UUID(data["id_especie"]) if data.get("id_especie") and isinstance(data["id_especie"], str) else data.get("id_especie"),
            especie=data.get("especie"),
            edad=data.get("edad"),
            estado=data.get("estado"),
            descripcion=data.get("descripcion"),
            fotos=data.get("fotos"),
            estado_adopcion=data.get("estado_adopcion"),
            id_refugio=UUID(data["id_refugio"]) if data.get("id_refugio") and isinstance(data["id_refugio"], str) else data.get("id_refugio")

        )

    async def listar_animales(self) -> list[Animal]:
        """GET /animals - Obtener todos los animales"""
        async with await self._get_animal() as client:
            response = await client.get("/animals")
            response.raise_for_status()
            animales_data = response.json()
            return [self._parse_animal(data) for data in animales_data]

    async def obtener_animal_por_id(self, id_animal: UUID) -> Optional[Animal]:
        """GET /animals/{id} - Obtener un animal por ID"""
        async with await self._get_animal() as client:
            try:
                response = await client.get(f"/animals/{str(id_animal)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_animal(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def crear_animal(self, nuevo_animal: NewAnimal) -> Animal:
        """POST /animals - Crear un nuevo animal"""
        async with await self._get_animal () as client:
            payload = {
                "nombre": nuevo_animal.nombre,
                "id_especie": nuevo_animal.id_especie,
                "edad": nuevo_animal.edad,
                "estado": nuevo_animal.estado,
                "descripcion": nuevo_animal.descripcion,
                "fotos": nuevo_animal.fotos,
                "estado_adopcion": nuevo_animal.estado_adopcion,
                "id_refugio": nuevo_animal.id_refugio
            }
            response = await client.post("/animals", json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_animal(data)

    async def actualizar_animal(self, animal_actualizado: UpdateAnimal) -> Optional[Animal]:
        """PUT /animals/{id} - Actualizar un animal"""
        async with await self._get_animal() as client:
            payload = {}
            if animal_actualizado.nombre is not None:
                payload["nombre"] = animal_actualizado.nombre
            if animal_actualizado.id_especie is not None:
                payload["id_especie"] = animal_actualizado.id_especie
            if animal_actualizado.edad is not None:
                payload["edad"] = animal_actualizado.edad
            if animal_actualizado.estado is not None:
                payload["estado"] = animal_actualizado.estado
            if animal_actualizado.descripcion is not None:
                payload["descripcion"] = animal_actualizado.descripcion
            if animal_actualizado.fotos is not None:
                payload["fotos"] = animal_actualizado.fotos
            if animal_actualizado.estado_adopcion is not None:
                payload["estado_adopcion"] = animal_actualizado.estado_adopcion
            if animal_actualizado.id_refugio is not None:
                payload["id_refugio"] = animal_actualizado.id_refugio  
            if animal_actualizado.contrasenia is not None:
                payload["contrasenia"] = animal_actualizado.contrasenia
            if animal_actualizado.telefono is not None:
                payload["telefono"] = animal_actualizado.telefono
            if animal_actualizado.direccion is not None:
                payload["direccion"] = animal_actualizado.direccion

            try:
                response = await client.put(
                    f"/animales/{str(animal_actualizado.id)}",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return self._parse_animal(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def eliminar_animal(self, id_animal: UUID) -> bool:
        """DELETE /animals/{id} - Eliminar un animal"""
        async with await self._get_animal() as client:
            try:
                response = await client.delete(f"/animals/{str(id_animal)}")
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return False
                raise