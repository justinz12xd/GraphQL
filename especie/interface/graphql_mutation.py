import graphene
from app.modules.especie.interface.graphql_type import EspecieType
from app.modules.especie.domain.entities import Especie


class CreateEspecie(graphene.Mutation):
    """Mutación GraphQL para crear una nueva Especie."""
    class Arguments:
        nombre = graphene.String(
            required=True,
            description="Nombre de la nueva especie a crear"
        )

    especie = graphene.Field(
        EspecieType,
        description="Objeto Especie recién creado"
    )

    def mutate(self, info, nombre):
        """Crear una nueva especie usando el repositorio del contexto y devolverla."""
        repo = info.context.get('especie_repo')  # Repositorio inyectado en el contexto
        nueva_especie = Especie(id=None, nombre=nombre)
        especie_creada = repo.save(nueva_especie)
        return CreateEspecie(especie=especie_creada)


class MutationEspecie(graphene.ObjectType):
    """Contenedor de las mutaciones para Especie."""
    create_especie = CreateEspecie.Field(
        description="Campo para crear una especie"
    )
