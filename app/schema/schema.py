import strawberry
from app.modules.animal.interface.graphql_query import AnimalQuery
from app.modules.tipo_campania.interface.graphql_mutation import TipoCampaniaMutation
from app.modules.tipo_campania.interface.graphql_query import TipoCampaniaQuery
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
from app.modules.voluntario.interface.graphql_query import VoluntarioQuery
from app.modules.voluntario.interface.graphql_mutation import VoluntarioMutation
from app.modules.campania.interface.graphql_query import CampaniaQuery
from app.modules.campania.interface.graphql_mutation import CampaniaMutation

@strawberry.type
class Query(AnimalQuery, UsuarioQuery, AdopcionQuery, CausaUrgenteQuery, PagoQuery, CampaniaQuery, TipoCampaniaQuery, VoluntarioQuery):
    """Root Query - Combina todas las queries de los módulos"""
    pass

@strawberry.type
class Mutation(AnimalMutation, UsuarioMutation, AdopcionMutation, CausaUrgenteMutation, PagoMutation, TipoCampaniaMutation, CampaniaMutation, VoluntarioMutation):
    """Root Mutation - Combina todas las mutations de los módulos"""
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)