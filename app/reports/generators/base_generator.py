"""Generador base abstracto para reportes."""

from abc import ABC, abstractmethod
from io import BytesIO
from typing import List, Dict, Any
from datetime import datetime

from app.reports.schemas import ReportMetadata


class BaseReportGenerator(ABC):
    """Clase base abstracta para generadores de reportes."""
    
    def __init__(self):
        """Inicializa el generador base."""
        self.metadata: ReportMetadata = None
    
    @abstractmethod
    def generate(self, data: List[Dict[str, Any]], **kwargs) -> BytesIO:
        """
        Genera el reporte.
        
        Args:
            data: Datos para el reporte
            **kwargs: Parámetros adicionales
            
        Returns:
            BytesIO con el contenido del reporte
        """
        pass
    
    def _create_metadata(
        self,
        titulo: str,
        total_registros: int
    ) -> ReportMetadata:
        """
        Crea metadata para el reporte.
        
        Args:
            titulo: Título del reporte
            total_registros: Total de registros en el reporte
            
        Returns:
            ReportMetadata con los datos del reporte
        """
        return ReportMetadata(
            titulo=titulo,
            fecha_generacion=datetime.now(),
            total_registros=total_registros
        )
    
    def _sanitize_text(self, text: str, max_length: int = None) -> str:
        """
        Sanitiza texto para evitar problemas en el reporte.
        
        Args:
            text: Texto a sanitizar
            max_length: Longitud máxima del texto
            
        Returns:
            Texto sanitizado
        """
        if not text:
            return "N/A"
        
        # Eliminar caracteres problemáticos
        text = text.strip()
        
        # Truncar si es necesario
        if max_length and len(text) > max_length:
            text = text[:max_length - 3] + "..."
        
        return text
