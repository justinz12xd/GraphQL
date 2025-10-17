
import strawberry
from app.modules.animal.interface.graphql_query import AnimalQuery, AnimalMutation

@strawberry.type
class Query(AnimalQuery):
    pass

@strawberry.type
class Mutation(AnimalMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
