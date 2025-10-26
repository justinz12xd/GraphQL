"""Configuración del módulo de reportes."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class ReportSettings(BaseSettings):
    """Configuración para el módulo de reportes."""
    
    # GraphQL Configuration
    graphql_url: str = os.getenv("GRAPHQL_URL", "http://localhost:8000/graphql")
    graphql_timeout: int = 30
    
    # PDF Configuration
    pdf_page_size: str = "A4"  # A4 o letter
    pdf_author: str = "Sistema de Refugio Animal"
    pdf_title_prefix: str = "Reporte - "
    
    # Colors (HEX)
    pdf_primary_color: str = "#3498DB"
    pdf_secondary_color: str = "#2C3E50"
    pdf_accent_color: str = "#E74C3C"
    pdf_background_color: str = "#ECF0F1"
    
    # Paths
    temp_dir: str = os.getenv("TEMP_DIR", "./temp_reports")
    
    class Config:
        env_prefix = "REPORT_"
        case_sensitive = False


# Instancia global de configuración
settings = ReportSettings()
