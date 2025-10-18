"""
Schema GraphQL del módulo de Usuario
"""
from app.modules.usuario.interface.graphql_query import UsuarioQuery
from app.modules.usuario.interface.graphql_mutation import UsuarioMutation

# Exportar las queries y mutations para ser utilizadas en el schema principal
__all__ = ['UsuarioQuery', 'UsuarioMutation']
