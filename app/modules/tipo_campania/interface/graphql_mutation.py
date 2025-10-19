import strawberry
from typing import Optional
from uuid import UUID
from app.modules.tipo_campania.interface.graphql_type import TipoCampaniaType, CreateTipoCampaniaInput, UpdateTipoCampaniaInput
from app.modules.tipo_campania.application.tipo_campania_service import TipoCampaniaService
from app.modules.tipo_campania.infrastructure.tipo_campania_repository import TipoCampaniaRepository
from app.modules.tipo_campania.domain.entities import NewTipoCampania, UpdateTipoCampania

@strawberry.type
class TipoCampaniaMutation:
    """Mutations GraphQL para TipoCampania"""

    @strawberry.mutation
    async def crear_tipo_campania(self, input: CreateTipoCampaniaInput) -> TipoCampaniaType:
        """Crear un nuevo tipo de campaña"""
        adapter = TipoCampaniaRepository()
        service = TipoCampaniaService(adapter)
        
        nuevo_tipo_campania = NewTipoCampania(
            nombre=input.nombre,
            descripcion=input.descripcion
        )
        
        tipo_campania = await service.crear(nuevo_tipo_campania)
        
        return TipoCampaniaType(
            id_tipo_campania=strawberry.ID(str(tipo_campania.id_tipo_campania)),
            nombre=tipo_campania.nombre,
            descripcion=tipo_campania.descripcion
        )
    
    @strawberry.mutation
    async def actualizar_tipo_campania(self, id_tipo_campania: strawberry.ID, input: UpdateTipoCampaniaInput) -> Optional[TipoCampaniaType]:
        """Actualizar un tipo de campaña existente"""
        adapter = TipoCampaniaRepository()
        service = TipoCampaniaService(adapter)
        
        tipo_campania_actualizada = UpdateTipoCampania(
            id_tipo_campania=UUID(id_tipo_campania),
            nombre=input.nombre,
            descripcion=input.descripcion
        )
        
        tipo_campania = await service.actualizar(tipo_campania_actualizada)
        
        if tipo_campania is None:
            return None
        
        return TipoCampaniaType(
            id_tipo_campania=strawberry.ID(str(tipo_campania.id_tipo_campania)),
            nombre=tipo_campania.nombre,
            descripcion=tipo_campania.descripcion
        )
    
    @strawberry.mutation
    async def eliminar_tipo_campania(self, id_tipo_campania: strawberry.ID) -> bool:
        """Eliminar un tipo de campaña por su ID"""
        adapter = TipoCampaniaRepository()
        service = TipoCampaniaService(adapter)
        
        resultado = await service.eliminar(UUID(id_tipo_campania))
        
        return resultado
    
