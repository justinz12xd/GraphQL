import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.campania.interface.graphql_type import CampaniaType
from app.modules.campania.application.campania_service import CampaniaApplicationService
from app.modules.campania.infrastructure.campania_respository import CampaniaRepository

@strawberry.type
class CampaniaMutation:
    #mutaciones de campania
    @strawberry.mutation
    async def crear_campania(self, nombre: str, descripcion: str, fecha_inicio: str, fecha_fin: str, lugar: str, organizador: str, estado: str) -> CampaniaType:
        adapter = CampaniaRepository()
        service = CampaniaApplicationService(adapter)
        campania = await service.crear_campania(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            lugar=lugar,
            organizador=organizador,
            estado=estado
        )

        campania= await service.crear_campania(campania)   
    
        return CampaniaType(
            id_campania=strawberry.ID(str(campania.id_campania)),
            nombre=campania.nombre,
            descripcion=campania.descripcion,
            fecha_inicio=campania.fecha_inicio,
            fecha_fin=campania.fecha_fin,
            lugar=campania.lugar,
            organizador=campania.organizador,
            estado=campania.estado
        )
    
@strawberry.mutation
async def actualizar_campania(self, id_campania: strawberry.ID, nombre: Optional[str] = None, descripcion: Optional[str] = None, fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None, lugar: Optional[str] = None, organizador: Optional[str] = None, estado: Optional[str] = None) -> CampaniaType:
        adapter = CampaniaRepository()
        service = CampaniaApplicationService(adapter)

        campania_actualizada = await service.actualizar_campania(
            id_campania=UUID(id_campania),
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            lugar=lugar,
            organizador=organizador,
            estado=estado
        )
        
        if campania_actualizada is None:
            return None

        return CampaniaType(
            id_campania=strawberry.ID(str(campania_actualizada.id_campania)),
            nombre=campania_actualizada.nombre,
            descripcion=campania_actualizada.descripcion,
            fecha_inicio=campania_actualizada.fecha_inicio,
            fecha_fin=campania_actualizada.fecha_fin,
            lugar=campania_actualizada.lugar,
            organizador=campania_actualizada.organizador,
            estado=campania_actualizada.estado
        )
@strawberry.mutation
async def eliminar_campania(self, id_campania: strawberry.ID) -> bool:
    adapter = CampaniaRepository()
    service = CampaniaApplicationService(adapter)
    return await service.eliminar_campania(UUID(id_campania))    