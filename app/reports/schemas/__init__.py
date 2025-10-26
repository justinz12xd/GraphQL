"""Exporta los schemas del módulo."""

from .report_schemas import (
    AnimalReportDTO,
    RefugioReportDTO,
    CampaniaReportDTO,
    ReportFilterDTO,
    ReportMetadata
)

__all__ = [
    "AnimalReportDTO",
    "RefugioReportDTO", 
    "CampaniaReportDTO",
    "ReportFilterDTO",
    "ReportMetadata"
]
