import httpx
from uuid import UUID
from app.config.settings import settings
from app.modules.animal.domain.entities import Animal, NewAnimal, UpdateAnimal

class AnimalRepository:
    """Adapter que consume el API REST en Rust y transforma a entidades de dominio."""

    async def listar_animales(self) -> list[Animal]:
        async with httpx.AsyncClient(base_url=settings.REST_API_URL) as client:
            resp = await client.get("/animals")
            resp.raise_for_status()
            data = resp.json()
            return [self._to_entity(animal) for animal in data]

    async def obtener_animal(self, id_animal: UUID) -> Animal:
        async with httpx.AsyncClient(base_url=settings.REST_API_URL) as client:
            resp = await client.get(f"/animals/{id_animal}")
            resp.raise_for_status()
            data = resp.json()
            return self._to_entity(data)

    async def crear_animal(self, new_animal: NewAnimal) -> Animal:
        async with httpx.AsyncClient(base_url=settings.REST_API_URL) as client:
            payload = new_animal.__dict__
            resp = await client.post("/animals", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return self._to_entity(data)

    async def actualizar_animal(self, id_animal: UUID, update: UpdateAnimal) -> Animal:
        async with httpx.AsyncClient(base_url=settings.REST_API_URL) as client:
            payload = {k: v for k, v in update.__dict__.items() if v is not None}
            resp = await client.patch(f"/animals/{id_animal}", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return self._to_entity(data)

    def _to_entity(self, data: dict) -> Animal:
        """Convierte el JSON del REST en la entidad de dominio"""
        return Animal(
            id_animal=UUID(data["id_animal"]),
            nombre=data["nombre"],
            id_especie=UUID(data["id_especie"]) if data.get("id_especie") else None,
            especie=data.get("especie"),
            edad=data.get("edad"),
            estado=data.get("estado"),
            descripcion=data.get("descripcion"),
            fotos=data.get("fotos"),
            estado_adopcion=data.get("estado_adopcion"),
            id_refugio=UUID(data["id_refugio"]) if data.get("id_refugio") else None
        )
