import graphene


class EspecieType(graphene.ObjectType):
    """Tipo GraphQL que representa la entidad Especie."""
    id = graphene.Int(description="ID de la especie")  # Identificador único
    nombre = graphene.String(description="Nombre de la especie")  # Nombre descriptivo
