import strawberry
from app.modules.usuario.interface.graphql_query import UsuarioQuery
from app.modules.usuario.interface.graphql_mutation import UsuarioMutation


@strawberry.type
class Query(UsuarioQuery):
    """Query principal que agrupa todas las queries de los módulos"""
    pass


@strawberry.type
class Mutation(UsuarioMutation):
    """Mutation principal que agrupa todas las mutations de los módulos"""
    pass


# Crear el schema principal
schema = strawberry.Schema(query=Query, mutation=Mutation)
