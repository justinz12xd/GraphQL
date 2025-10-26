"""Schemas para validación de datos de reportes."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class AnimalReportDTO(BaseModel):
    """DTO para datos de animales en reportes."""
    
    id_animal: str = Field(..., alias="idAnimal")
    nombre: Optional[str] = None
    especie: Optional[str] = None
    edad: Optional[int] = None
    estado_adopcion: Optional[str] = Field(None, alias="estadoAdopcion")
    descripcion: Optional[str] = None
    fotos: Optional[List[str]] = None
    id_refugio: Optional[str] = Field(None, alias="idRefugio")
    fecha_creacion: Optional[str] = Field(None, alias="fechaCreacion")
    
    class Config:
        populate_by_name = True


class RefugioReportDTO(BaseModel):
    """DTO para datos de refugios en reportes."""
    
    id_refugio: str = Field(..., alias="idRefugio")
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    capacidad: Optional[int] = None
    
    class Config:
        populate_by_name = True


class CampaniaReportDTO(BaseModel):
    """DTO para datos de campañas en reportes."""
    
    id_campania: str = Field(..., alias="idCampania")
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    meta: Optional[float] = None
    monto_recaudado: Optional[float] = Field(None, alias="montoRecaudado")
    fecha_inicio: Optional[str] = Field(None, alias="fechaInicio")
    fecha_fin: Optional[str] = Field(None, alias="fechaFin")
    
    class Config:
        populate_by_name = True


class ReportFilterDTO(BaseModel):
    """DTO para filtros de reportes."""
    
    nombre: Optional[str] = None
    id_especie: Optional[str] = None
    id_refugio: Optional[str] = None
    estado_adopcion: Optional[str] = None
    edad_min: Optional[int] = None
    edad_max: Optional[int] = None


class ReportMetadata(BaseModel):
    """Metadata de un reporte generado."""
    
    titulo: str
    fecha_generacion: datetime = Field(default_factory=datetime.now)
    total_registros: int
    autor: str = "Sistema de Refugio Animal"
    version: str = "1.0.0"
