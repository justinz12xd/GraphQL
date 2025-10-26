"""Exporta los generadores del módulo."""

from .base_generator import BaseReportGenerator
from .pdf_generator import PDFGenerator

__all__ = ["BaseReportGenerator", "PDFGenerator"]
