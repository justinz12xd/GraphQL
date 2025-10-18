import strawberry
from app.modules.animal.interface.graphql_query import AnimalQuery, AnimalMutation
from app.modules.usuario.interface.graphql_query import UsuarioQuery
from app.modules.usuario.interface.graphql_mutation import UsuarioMutation

@strawberry.type
class Query(AnimalQuery, UsuarioQuery):
    """Root Query - Combina todas las queries de los módulos"""
    pass

@strawberry.type
class Mutation(AnimalMutation, UsuarioMutation):
    """Root Mutation - Combina todas las mutations de los módulos"""
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
