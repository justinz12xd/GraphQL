import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.tipo_campania.interface.graphql_type import TipoCampaniaType
from app.modules.tipo_campania.application.tipo_campania_service import TipoCampaniaService
from app.modules.tipo_campania.infrastructure.tipo_campania_repository import TipoCampaniaRepository

@strawberry.type
class TipoCampaniaQuery:
    """Queries GraphQL para TipoCampania"""

    @strawberry.field
    async def tipos_campania(self) -> List[TipoCampaniaType]:
        """Obtener todos los tipos de campaña"""
        adapter = TipoCampaniaRepository()
        service = TipoCampaniaService(adapter)
        tipos_campania = await service.obtener_todos()
        
        return [
            TipoCampaniaType(
                id_tipo_campania=strawberry.ID(str(tipo.id_tipo_campania)),
                nombre=tipo.nombre,
                descripcion=tipo.descripcion
            )
            for tipo in tipos_campania
        ]
    
    @strawberry.field
    async def tipo_campania(self, id_tipo_campania: strawberry.ID) -> Optional[TipoCampaniaType]:
        """Obtener un tipo de campaña por ID"""
        adapter = TipoCampaniaRepository()
        service = TipoCampaniaService(adapter)
        tipo_campania = await service.obtener_por_id(UUID(id_tipo_campania))
        
        if tipo_campania is None:
            return None
        
        return TipoCampaniaType(
            id_tipo_campania=strawberry.ID(str(tipo_campania.id_tipo_campania)),
            nombre=tipo_campania.nombre,
            descripcion=tipo_campania.descripcion
        )