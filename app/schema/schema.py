import strawberry
from app.modules.animal.interface.graphql_query import AnimalQuery
from app.modules.animal.interface.graphql_mutation import AnimalMutation
from app.modules.usuario.interface.graphql_query import UsuarioQuery
from app.modules.usuario.interface.graphql_mutation import UsuarioMutation
from app.modules.adopcion.interface.graphql_query import AdopcionQuery
from app.modules.adopcion.interface.graphql_mutation import AdopcionMutation
from app.modules.causa_urgente.interface.graphql_mutation import CausaUrgenteMutation
from app.modules.causa_urgente.interface.graphql_query import CausaUrgenteQuery
from app.modules.pago.interface.graphql_query import PagoQuery
from app.modules.pago.interface.graphql_mutation import PagoMutation

@strawberry.type
class Query(AnimalQuery, AnimalMutation, UsuarioQuery, AdopcionQuery, CausaUrgenteQuery, PagoQuery):
    """Root Query - Combina todas las queries de los módulos"""
    pass

@strawberry.type
class Mutation(AnimalMutation, UsuarioMutation, AdopcionMutation, CausaUrgenteMutation, PagoMutation):
    """Root Mutation - Combina todas las mutations de los módulos"""
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)