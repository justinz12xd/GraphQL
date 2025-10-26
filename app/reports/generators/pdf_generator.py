"""Generador de reportes en formato PDF."""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.reports.generators.base_generator import BaseReportGenerator
from app.reports.config import settings

logger = logging.getLogger(__name__)


class PDFGenerator(BaseReportGenerator):
    """Generador de reportes PDF para el sistema de refugio."""
    
    def __init__(self):
        """Inicializa el generador de PDF."""
        super().__init__()
        self.page_size = A4 if settings.pdf_page_size == "A4" else letter
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info("PDF Generator inicializado")
    
    def _setup_custom_styles(self):
        """Define estilos personalizados para el PDF."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(settings.pdf_secondary_color),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor(settings.pdf_secondary_color),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor(settings.pdf_secondary_color),
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Fecha del reporte
        self.styles.add(ParagraphStyle(
            name='ReportDate',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_RIGHT,
            spaceAfter=20
        ))
    
    def _create_header(self, title: str) -> List:
        """
        Crea el encabezado del PDF.
        
        Args:
            title: Título del reporte
        """
        elements = []
        
        # Título
        elements.append(Paragraph(
            f"{settings.pdf_title_prefix}{title}",
            self.styles['CustomTitle']
        ))
        
        # Fecha de generación
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(
            f"Generado el: {fecha_actual}",
            self.styles['ReportDate']
        ))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_table(
        self,
        data: List[List[Any]],
        col_widths: Optional[List[float]] = None,
        header_color: Optional[str] = None,
        alt_row_color: Optional[str] = None
    ) -> Table:
        """
        Crea una tabla formateada.
        
        Args:
            data: Datos de la tabla (primera fila = encabezados)
            col_widths: Anchos de columnas personalizados
            header_color: Color del encabezado
            alt_row_color: Color de filas alternas
        """
        header_color = header_color or settings.pdf_primary_color
        alt_row_color = alt_row_color or settings.pdf_background_color
        
        table = Table(data, colWidths=col_widths)
        
        # Estilo de tabla
        style = TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_color)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor(settings.pdf_secondary_color)),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ])
        
        # Filas alternas
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.add('BACKGROUND', (0, i), (-1, i),
                         colors.HexColor(alt_row_color))
        
        table.setStyle(style)
        return table
    
    def generate(
        self,
        data: List[Dict[str, Any]],
        report_type: str,
        **kwargs
    ) -> BytesIO:
        """
        Genera el reporte PDF según el tipo especificado.
        
        Args:
            data: Datos para el reporte
            report_type: Tipo de reporte (animales_especie, animales_refugio, etc.)
            **kwargs: Parámetros adicionales según el tipo de reporte
            
        Returns:
            BytesIO con el PDF generado
        """
        generators = {
            "animales_especie": self._generate_animales_por_especie,
            "animales_refugio": self._generate_animales_por_refugio,
            "animales_general": self._generate_animales_general,
            "campanias": self._generate_campanias
        }
        
        generator_func = generators.get(report_type)
        if not generator_func:
            raise ValueError(f"Tipo de reporte no soportado: {report_type}")
        
        logger.info(f"Generando reporte: {report_type}")
        return generator_func(data, **kwargs)
    
    def _generate_animales_por_especie(
        self,
        animales: List[Dict[str, Any]],
        nombre_especie: str
    ) -> BytesIO:
        """Genera PDF con animales filtrados por especie."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            author=settings.pdf_author
        )
        elements = []
        
        # Encabezado
        elements.extend(self._create_header(
            f"Animales - {nombre_especie}"
        ))
        
        # Estadísticas
        total_animales = len(animales)
        disponibles = sum(
            1 for a in animales
            if a.get('estadoAdopcion') == 'disponible'
        )
        
        stats = f"""
        <b>Total de animales:</b> {total_animales}<br/>
        <b>Disponibles para adopción:</b> {disponibles}<br/>
        <b>Especie:</b> {nombre_especie}
        """
        elements.append(Paragraph(stats, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Tabla de animales
        if animales:
            table_data = [['Nombre', 'Edad', 'Estado', 'Descripción']]
            
            for animal in animales:
                nombre = self._sanitize_text(animal.get('nombre'), 30)
                edad_val = animal.get('edad')
                edad = f"{edad_val} años" if edad_val else 'N/A'
                estado = self._sanitize_text(
                    animal.get('estadoAdopcion', 'N/A').title(),
                    20
                )
                descripcion = self._sanitize_text(
                    animal.get('descripcion', 'Sin descripción'),
                    50
                )
                
                table_data.append([nombre, edad, estado, descripcion])
            
            table = self._create_table(
                table_data,
                col_widths=[1.5*inch, 1*inch, 1.2*inch, 3*inch]
            )
            elements.append(table)
        else:
            elements.append(Paragraph(
                "No se encontraron animales para esta especie.",
                self.styles['CustomBody']
            ))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        logger.info(f"PDF generado: {total_animales} animales")
        return buffer
    
    def _generate_animales_por_refugio(
        self,
        animales: List[Dict[str, Any]],
        nombre_refugio: str
    ) -> BytesIO:
        """Genera PDF con animales de un refugio específico."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            author=settings.pdf_author
        )
        elements = []
        
        # Encabezado
        elements.extend(self._create_header(
            f"Inventario - {nombre_refugio}"
        ))
        
        # Estadísticas por especie
        especies_count = {}
        for animal in animales:
            especie = animal.get('especie', 'Desconocida')
            especies_count[especie] = especies_count.get(especie, 0) + 1
        
        stats = f"<b>Total de animales:</b> {len(animales)}<br/>"
        for especie, count in sorted(especies_count.items()):
            stats += f"<b>{especie}:</b> {count}<br/>"
        
        elements.append(Paragraph(stats, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Tabla de animales
        if animales:
            table_data = [
                ['Nombre', 'Especie', 'Edad', 'Estado', 'Fecha Ingreso']
            ]
            
            for animal in animales:
                nombre = self._sanitize_text(animal.get('nombre'), 25)
                especie = self._sanitize_text(animal.get('especie'), 15)
                edad_val = animal.get('edad')
                edad = str(edad_val) if edad_val else 'N/A'
                estado = self._sanitize_text(
                    animal.get('estadoAdopcion', 'N/A').title(),
                    15
                )
                fecha_raw = animal.get('fechaCreacion', 'N/A')
                fecha = fecha_raw[:10] if fecha_raw and fecha_raw != 'N/A' else 'N/A'
                
                table_data.append([nombre, especie, edad, estado, fecha])
            
            table = self._create_table(
                table_data,
                col_widths=[1.3*inch, 1.2*inch, 0.8*inch, 1.2*inch, 1.2*inch]
            )
            elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        logger.info(f"PDF inventario generado: {len(animales)} animales")
        return buffer
    
    def _generate_animales_general(
        self,
        animales: List[Dict[str, Any]]
    ) -> BytesIO:
        """Genera PDF con reporte general de todos los animales."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            author=settings.pdf_author
        )
        elements = []
        
        # Encabezado
        elements.extend(self._create_header(
            "Reporte General de Animales"
        ))
        
        # Estadísticas generales
        total = len(animales)
        disponibles = sum(
            1 for a in animales
            if a.get('estadoAdopcion') == 'disponible'
        )
        
        # Distribución por especie
        especies_count = {}
        for animal in animales:
            especie = animal.get('especie', 'Desconocida')
            especies_count[especie] = especies_count.get(especie, 0) + 1
        
        stats = f"""
        <b>Total de animales registrados:</b> {total}<br/>
        <b>Disponibles para adopción:</b> {disponibles}<br/>
        <b>En proceso de adopción:</b> {total - disponibles}<br/><br/>
        <b>Distribución por especie:</b><br/>
        """
        
        for especie, count in sorted(especies_count.items()):
            porcentaje = (count / total * 100) if total > 0 else 0
            stats += f"• {especie}: {count} ({porcentaje:.1f}%)<br/>"
        
        elements.append(Paragraph(stats, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Subtítulo
        elements.append(Paragraph(
            "Listado Completo de Animales",
            self.styles['CustomSubtitle']
        ))
        
        # Tabla de animales
        if animales:
            table_data = [['#', 'Nombre', 'Especie', 'Edad', 'Estado']]
            
            for idx, animal in enumerate(animales, 1):
                nombre = self._sanitize_text(animal.get('nombre'), 30)
                especie = self._sanitize_text(animal.get('especie'), 15)
                edad_val = animal.get('edad')
                edad = str(edad_val) if edad_val else 'N/A'
                estado = self._sanitize_text(
                    animal.get('estadoAdopcion', 'N/A').title(),
                    15
                )
                
                table_data.append([str(idx), nombre, especie, edad, estado])
            
            table = self._create_table(
                table_data,
                col_widths=[0.5*inch, 1.5*inch, 1.2*inch, 0.8*inch, 1.5*inch]
            )
            elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        logger.info(f"PDF general generado: {total} animales")
        return buffer
    
    def _generate_campanias(
        self,
        campanias: List[Dict[str, Any]]
    ) -> BytesIO:
        """Genera PDF con reporte de campañas activas."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            author=settings.pdf_author
        )
        elements = []
        
        # Encabezado
        elements.extend(self._create_header("Campañas Activas"))
        
        # Estadísticas
        total_recaudado = sum(c.get('montoRecaudado', 0) for c in campanias)
        total_meta = sum(c.get('meta', 0) for c in campanias)
        porcentaje_global = (
            (total_recaudado / total_meta * 100) if total_meta > 0 else 0
        )
        
        stats = f"""
        <b>Total de campañas activas:</b> {len(campanias)}<br/>
        <b>Monto total recaudado:</b> S/ {total_recaudado:,.2f}<br/>
        <b>Meta total:</b> S/ {total_meta:,.2f}<br/>
        <b>Progreso global:</b> {porcentaje_global:.1f}%
        """
        
        elements.append(Paragraph(stats, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Tabla de campañas
        if campanias:
            table_data = [
                ['Campaña', 'Meta', 'Recaudado', 'Progreso', 'Fecha Fin']
            ]
            
            for campania in campanias:
                titulo = self._sanitize_text(campania.get('titulo'), 30)
                meta = f"S/ {campania.get('meta', 0):,.0f}"
                recaudado = f"S/ {campania.get('montoRecaudado', 0):,.0f}"
                progreso_pct = (
                    campania.get('montoRecaudado', 0) /
                    campania.get('meta', 1) * 100
                )
                progreso = f"{progreso_pct:.1f}%"
                fecha_fin = campania.get('fechaFin', 'N/A')[:10]
                
                table_data.append([titulo, meta, recaudado, progreso, fecha_fin])
            
            table = self._create_table(
                table_data,
                col_widths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch]
            )
            elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        logger.info(f"PDF campañas generado: {len(campanias)} campañas")
        return buffer
