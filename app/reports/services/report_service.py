"""Servicio de reportes que coordina cliente GraphQL y generador PDF."""

import logging
from io import BytesIO
from typing import Optional

from app.reports.clients import GraphQLClient
from app.reports.generators import PDFGenerator
from app.reports.schemas import ReportFilterDTO

logger = logging.getLogger(__name__)


class ReportService:
    """
    Servicio de negocio para generación de reportes.
    
    Coordina la obtención de datos desde GraphQL y la generación de PDFs.
    """
    
    def __init__(
        self,
        graphql_client: Optional[GraphQLClient] = None,
        pdf_generator: Optional[PDFGenerator] = None
    ):
        """
        Inicializa el servicio de reportes.
        
        Args:
            graphql_client: Cliente GraphQL (se crea uno si es None)
            pdf_generator: Generador PDF (se crea uno si es None)
        """
        self.graphql_client = graphql_client or GraphQLClient()
        self.pdf_generator = pdf_generator or PDFGenerator()
        logger.info("ReportService inicializado")
    
    # ========== REPORTES DE ANIMALES ==========
    
    async def generar_reporte_animales_por_especie(
        self,
        id_especie: str
    ) -> tuple[BytesIO, str]:
        """
        Genera PDF con animales filtrados por especie.
        
        Args:
            id_especie: UUID de la especie
            
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
            
        Raises:
            ValueError: Si no se encuentran animales
        """
        logger.info(f"Generando reporte de animales por especie: {id_especie}")
        
        # Obtener especies primero para hacer el mapeo
        especies = await self.graphql_client.obtener_especies()
        especies_dict = {str(e['id']): e['nombre'] for e in especies}
        
        # Obtener datos
        animales = await self.graphql_client.obtener_animales_por_especie(
            id_especie
        )
        
        if not animales:
            raise ValueError(
                f"No se encontraron animales para la especie {id_especie}"
            )
        
        # Mapear nombres de especies a los animales si no vienen
        for animal in animales:
            if not animal.get('especie') and animal.get('idEspecie'):
                id_esp = str(animal['idEspecie'])
                animal['especie'] = especies_dict.get(id_esp, 'Desconocida')
        
        # Extraer nombre de especie
        nombre_especie = animales[0].get('especie', especies_dict.get(id_especie, 'Desconocida'))
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=animales,
            report_type="animales_especie",
            nombre_especie=nombre_especie
        )
        
        filename = f"animales_{nombre_especie.lower().replace(' ', '_')}.pdf"
        logger.info(f"Reporte generado exitosamente: {filename}")
        
        return pdf_buffer, filename
    
    async def generar_reporte_animales_por_refugio(
        self,
        id_refugio: str
    ) -> tuple[BytesIO, str]:
        """
        Genera PDF con animales de un refugio específico.
        
        Args:
            id_refugio: UUID del refugio
            
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
            
        Raises:
            ValueError: Si no se encuentran animales
        """
        logger.info(f"Generando reporte de animales por refugio: {id_refugio}")
        
        # Obtener especies primero para hacer el mapeo
        especies = await self.graphql_client.obtener_especies()
        especies_dict = {str(e['id']): e['nombre'] for e in especies}
        
        # Obtener animales
        animales = await self.graphql_client.obtener_animales_por_refugio(
            id_refugio
        )
        
        if not animales:
            raise ValueError(
                f"No se encontraron animales para el refugio {id_refugio}"
            )
        
        # Mapear nombres de especies a los animales si no vienen
        for animal in animales:
            if not animal.get('especie') and animal.get('idEspecie'):
                id_esp = str(animal['idEspecie'])
                animal['especie'] = especies_dict.get(id_esp, 'Desconocida')
        
        # Obtener nombre del refugio
        refugio = await self.graphql_client.obtener_refugio_por_id(id_refugio)
        nombre_refugio = refugio.get('nombre', 'Refugio Desconocido') if refugio else 'Refugio Desconocido'
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=animales,
            report_type="animales_refugio",
            nombre_refugio=nombre_refugio
        )
        
        filename = f"refugio_{nombre_refugio.lower().replace(' ', '_')}.pdf"
        logger.info(f"Reporte generado exitosamente: {filename}")
        
        return pdf_buffer, filename
    
    async def generar_reporte_animales_general(self) -> tuple[BytesIO, str]:
        """
        Genera PDF con reporte general de todos los animales disponibles.
        
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
            
        Raises:
            ValueError: Si no hay animales registrados
        """
        logger.info("Generando reporte general de animales")
        
        # Obtener especies primero para hacer el mapeo
        especies = await self.graphql_client.obtener_especies()
        especies_dict = {str(e['id']): e['nombre'] for e in especies}
        
        # Obtener datos
        animales = await self.graphql_client.obtener_todos_animales()
        
        if not animales:
            raise ValueError("No hay animales registrados en el sistema")
        
        # Mapear nombres de especies a los animales si no vienen
        for animal in animales:
            if not animal.get('especie') and animal.get('idEspecie'):
                id_esp = str(animal['idEspecie'])
                animal['especie'] = especies_dict.get(id_esp, 'Desconocida')
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=animales,
            report_type="animales_general"
        )
        
        filename = "reporte_general_animales.pdf"
        logger.info(f"Reporte generado exitosamente: {filename}")
        
        return pdf_buffer, filename
    
    async def generar_reporte_animales_filtrados(
        self,
        filtros: ReportFilterDTO
    ) -> tuple[BytesIO, str]:
        """
        Genera PDF con animales usando filtros combinados.
        
        Args:
            filtros: DTO con los filtros a aplicar
            
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
            
        Raises:
            ValueError: Si no se encuentran animales con los filtros
        """
        logger.info(f"Generando reporte de animales filtrados: {filtros}")
        
        # Obtener especies primero para hacer el mapeo
        especies = await self.graphql_client.obtener_especies()
        especies_dict = {str(e['id']): e['nombre'] for e in especies}
        
        # Obtener datos
        animales = await self.graphql_client.obtener_animales_filtrados(
            nombre=filtros.nombre,
            id_especie=filtros.id_especie,
            id_refugio=filtros.id_refugio,
            estado_adopcion=filtros.estado_adopcion,
            edad_min=filtros.edad_min,
            edad_max=filtros.edad_max
        )
        
        if not animales:
            raise ValueError(
                "No se encontraron animales con los filtros especificados"
            )
        
        # Mapear nombres de especies a los animales si no vienen
        for animal in animales:
            if not animal.get('especie') and animal.get('idEspecie'):
                id_esp = str(animal['idEspecie'])
                animal['especie'] = especies_dict.get(id_esp, 'Desconocida')
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=animales,
            report_type="animales_general"
        )
        
        filename = "animales_filtrados.pdf"
        logger.info(f"Reporte generado exitosamente: {filename}")
        
        return pdf_buffer, filename
    
    # ========== REPORTES DE CAMPAÑAS ==========
    
    async def generar_reporte_campanias(self) -> tuple[BytesIO, str]:
        """
        Genera PDF con reporte de campañas activas.
        
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
            
        Raises:
            ValueError: Si no hay campañas activas
        """
        logger.info("Generando reporte de campañas activas")
        
        # Obtener datos
        campanias = await self.graphql_client.obtener_campanias()
        
        if not campanias:
            raise ValueError("No hay campañas activas en el sistema")
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=campanias,
            report_type="campanias"
        )
        
        filename = "campanias_activas.pdf"
        logger.info(f"Reporte generado exitosamente: {filename}")
        
        return pdf_buffer, filename
    
    # ========== REPORTE DE PRUEBA ==========
    
    def generar_reporte_prueba(self) -> tuple[BytesIO, str]:
        """
        Genera un PDF de prueba con datos ficticios.
        No requiere conexión a GraphQL.
        
        Returns:
            Tuple con (BytesIO del PDF, nombre del archivo)
        """
        logger.info("Generando reporte de prueba")
        
        # Datos de prueba
        animales_prueba = [
            {
                "idAnimal": "test-1",
                "nombre": "Max",
                "especie": "Perro",
                "edad": 3,
                "estadoAdopcion": "disponible",
                "descripcion": "Perro amigable y juguetón",
                "fechaCreacion": "2024-01-15"
            },
            {
                "idAnimal": "test-2",
                "nombre": "Luna",
                "especie": "Gato",
                "edad": 2,
                "estadoAdopcion": "disponible",
                "descripcion": "Gata tranquila y cariñosa",
                "fechaCreacion": "2024-02-20"
            },
            {
                "idAnimal": "test-3",
                "nombre": "Rocky",
                "especie": "Perro",
                "edad": 5,
                "estadoAdopcion": "disponible",
                "descripcion": "Perro guardián y leal",
                "fechaCreacion": "2024-03-10"
            },
            {
                "idAnimal": "test-4",
                "nombre": "Bella",
                "especie": "Gato",
                "edad": 1,
                "estadoAdopcion": "disponible",
                "descripcion": "Gatita muy juguetona",
                "fechaCreacion": "2024-04-05"
            }
        ]
        
        # Generar PDF
        pdf_buffer = self.pdf_generator.generate(
            data=animales_prueba,
            report_type="animales_especie",
            nombre_especie="Datos de Prueba"
        )
        
        filename = "test_reporte.pdf"
        logger.info(f"Reporte de prueba generado: {filename}")
        
        return pdf_buffer, filename
