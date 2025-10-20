import graphene
from app.modules.especie.interface.graphql_type import EspecieType


class QueryEspecie(graphene.ObjectType):
    """GraphQL queries for Especie module."""
    especies = graphene.List(
        EspecieType,
        description="List all species"
    )

    def resolve_especies(self, info):
        """Resolver for 'especies' query that returns all species."""
        repo = info.context.get('especie_repo')
        return repo.list_all()
