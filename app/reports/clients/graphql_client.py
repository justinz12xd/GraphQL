"""Cliente GraphQL para obtener datos de reportes."""

import logging
from typing import Dict, Any, List, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from app.reports.config import settings

logger = logging.getLogger(__name__)


class GraphQLClient:
    """Cliente para realizar consultas GraphQL al servidor."""
    
    def __init__(self, graphql_url: Optional[str] = None):
        """
        Inicializa el cliente GraphQL.
        
        Args:
            graphql_url: URL del servidor GraphQL. Si es None, usa settings.
        """
        self.graphql_url = graphql_url or settings.graphql_url
        self.transport = AIOHTTPTransport(
            url=self.graphql_url,
            timeout=settings.graphql_timeout
        )
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True
        )
        logger.info(f"GraphQL Client inicializado: {self.graphql_url}")
    
    async def execute_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta una consulta GraphQL.
        
        Args:
            query: String con la consulta GraphQL
            variables: Diccionario con las variables de la consulta
            
        Returns:
            Diccionario con la respuesta de GraphQL
            
        Raises:
            TransportQueryError: Si hay error en la consulta
        """
        try:
            async with self.client as session:
                result = await session.execute(
                    gql(query),
                    variable_values=variables
                )
                logger.debug(f"Query ejecutada exitosamente")
                return result
        except TransportQueryError as e:
            logger.error(f"Error en query GraphQL: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise
    
    # ========== QUERIES PARA ANIMALES ==========
    
    async def obtener_todos_animales(self) -> List[Dict[str, Any]]:
        """Obtiene todos los animales disponibles."""
        query = """
        query {
            animalesDisponibles {
                idAnimal
                nombre
                idEspecie
                especie
                edad
                estadoAdopcion
                descripcion
                fotos
                idRefugio
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("animalesDisponibles", [])
    
    async def obtener_animales_por_especie(
        self,
        id_especie: str
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales filtrados por especie.
        
        Args:
            id_especie: UUID de la especie
        """
        query = """
        query AnimalesPorEspecie($idEspecie: ID!) {
            animalesPorEspecie(idEspecie: $idEspecie) {
                idAnimal
                nombre
                idEspecie
                especie
                edad
                estadoAdopcion
                descripcion
                fotos
                idRefugio
            }
        }
        """
        result = await self.execute_query(
            query,
            variables={"idEspecie": id_especie}
        )
        return result.get("animalesPorEspecie", [])
    
    async def obtener_animales_por_refugio(
        self,
        id_refugio: str
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales filtrados por refugio.
        
        Args:
            id_refugio: UUID del refugio
        """
        query = """
        query AnimalesPorRefugio($idRefugio: ID!) {
            animalesPorRefugio(idRefugio: $idRefugio) {
                idAnimal
                nombre
                idEspecie
                especie
                edad
                estadoAdopcion
                descripcion
                idRefugio
            }
        }
        """
        result = await self.execute_query(
            query,
            variables={"idRefugio": id_refugio}
        )
        return result.get("animalesPorRefugio", [])
    
    async def obtener_animales_filtrados(
        self,
        nombre: Optional[str] = None,
        id_especie: Optional[str] = None,
        id_refugio: Optional[str] = None,
        estado_adopcion: Optional[str] = None,
        edad_min: Optional[int] = None,
        edad_max: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales con filtros combinados.
        
        Args:
            nombre: Nombre parcial del animal
            id_especie: UUID de la especie
            id_refugio: UUID del refugio
            estado_adopcion: Estado de adopción
            edad_min: Edad mínima
            edad_max: Edad máxima
        """
        query = """
        query AnimalesFiltrados(
            $nombre: String
            $idEspecie: ID
            $idRefugio: ID
            $estadoAdopcion: String
            $edadMin: Int
            $edadMax: Int
        ) {
            animalesFiltrados(
                nombre: $nombre
                idEspecie: $idEspecie
                idRefugio: $idRefugio
                estadoAdopcion: $estadoAdopcion
                edadMin: $edadMin
                edadMax: $edadMax
            ) {
                idAnimal
                nombre
                idEspecie
                especie
                edad
                estadoAdopcion
                descripcion
                fotos
                idRefugio
            }
        }
        """
        # Construir variables solo con valores no None
        variables = {}
        if nombre:
            variables["nombre"] = nombre
        if id_especie:
            variables["idEspecie"] = id_especie
        if id_refugio:
            variables["idRefugio"] = id_refugio
        if estado_adopcion:
            variables["estadoAdopcion"] = estado_adopcion
        if edad_min is not None:
            variables["edadMin"] = edad_min
        if edad_max is not None:
            variables["edadMax"] = edad_max
        
        result = await self.execute_query(query, variables=variables)
        return result.get("animalesFiltrados", [])
    
    # ========== QUERIES PARA REFUGIOS ==========
    
    async def obtener_refugios(self) -> List[Dict[str, Any]]:
        """Obtiene todos los refugios."""
        query = """
        query {
            listarRefugios {
                idRefugio
                nombre
                direccion
                telefono
                capacidad
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("listarRefugios", [])
    
    async def obtener_refugio_por_id(self, id_refugio: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un refugio por ID.
        
        Args:
            id_refugio: UUID del refugio
        """
        query = """
        query RefugioPorId($idRefugio: ID!) {
            refugio(idRefugio: $idRefugio) {
                idRefugio
                nombre
                direccion
                telefono
                capacidad
            }
        }
        """
        result = await self.execute_query(
            query,
            variables={"idRefugio": id_refugio}
        )
        return result.get("refugio")
    
    # ========== QUERIES PARA ESPECIES ==========
    
    async def obtener_especies(self) -> List[Dict[str, Any]]:
        """Obtiene todas las especies."""
        query = """
        query {
            especies {
                id
                nombre
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("especies", [])
    
    # ========== QUERIES PARA CAMPAÑAS ==========
    
    async def obtener_campanias(self) -> List[Dict[str, Any]]:
        """Obtiene todas las campañas."""
        query = """
        query {
            listarCampanias {
                idCampania
                titulo
                descripcion
                fechaInicio
                fechaFin
                lugar
                organizador
                estado
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("listarCampanias", [])
    
    # ========== QUERIES PARA CAUSAS URGENTES ==========
    
    async def obtener_causas_urgentes(self) -> List[Dict[str, Any]]:
        """Obtiene todas las causas urgentes."""
        query = """
        query {
            listarCausasUrgentes {
                idCausaUrgente
                titulo
                descripcion
                meta
                montoRecaudado
                fechaLimite
                idAnimal
            }
        }
        """
        result = await self.execute_query(query)
        return result.get("listarCausasUrgentes", [])
