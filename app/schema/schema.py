import strawberry
from app.modules.animal.interface.graphql_query import AnimalQuery
from app.modules.tipo_campania.interface.graphql_query import TipoCampaniaQuery
from app.modules.usuario.interface.graphql_query import UsuarioQuery
from app.modules.adopcion.interface.graphql_query import AdopcionQuery
from app.modules.causa_urgente.interface.graphql_query import CausaUrgenteQuery
from app.modules.pago.interface.graphql_query import PagoQuery
from app.modules.voluntario.interface.graphql_query import VoluntarioQuery
from app.modules.campania.interface.graphql_query import CampaniaQuery
from app.modules.supervisor.interface.graphql_query import SupervisorQuery
from app.modules.especie.interface.graphql_query import EspecieQuery
from app.modules.refugio.interface.graphql_query import RefugioQuery
from app.modules.publicacion.interface.graphql_query import PublicacionQuery
from app.modules.seguimiento.interface.graphql_query import SeguimientoQuery

@strawberry.type
class Query(
    AnimalQuery, 
    UsuarioQuery, 
    AdopcionQuery, 
    CausaUrgenteQuery, 
    PagoQuery, 
    CampaniaQuery, 
    TipoCampaniaQuery, 
    VoluntarioQuery, 
    SupervisorQuery,
    EspecieQuery,
    RefugioQuery,
    PublicacionQuery,
    SeguimientoQuery
):
    """Root Query - Combina todas las queries de los módulos"""
    pass

schema = strawberry.Schema(query=Query)