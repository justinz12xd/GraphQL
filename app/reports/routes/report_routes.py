"""Rutas FastAPI para generación de reportes PDF."""

import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional

from app.reports.services import ReportService
from app.reports.schemas import ReportFilterDTO

logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
    responses={
        404: {"description": "No se encontraron datos"},
        500: {"description": "Error interno del servidor"}
    }
)

# Instancia del servicio (singleton)
report_service = ReportService()


# ========== ENDPOINT DE PRUEBA ==========

@router.get(
    "/test/pdf",
    summary="Genera PDF de prueba",
    description="Genera un PDF de prueba con datos ficticios. No requiere datos reales."
)
async def test_generar_pdf():
    """
    Endpoint de prueba para verificar que el generador de PDF funciona.
    
    **No requiere parámetros ni datos reales de GraphQL.**
    
    Ejemplo: `GET /api/reports/test/pdf`
    """
    try:
        logger.info("Solicitud de reporte de prueba recibida")
        
        pdf_buffer, filename = report_service.generar_reporte_prueba()
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except Exception as e:
        logger.error(f"Error generando PDF de prueba: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando PDF de prueba: {str(e)}"
        )


# ========== REPORTES DE ANIMALES ==========

@router.get(
    "/animales/por-especie/pdf",
    summary="Reporte de animales por especie",
    description="Genera PDF con todos los animales de una especie específica"
)
async def generar_pdf_animales_por_especie(
    id_especie: str = Query(
        ...,
        description="UUID de la especie",
        example="uuid-de-especie-aqui"
    )
):
    """
    Genera PDF con animales filtrados por especie.
    
    **Parámetros:**
    - `id_especie`: UUID de la especie (requerido)
    
    **Ejemplo:** `GET /api/reports/animales/por-especie/pdf?id_especie=uuid-aqui`
    """
    try:
        logger.info(f"Solicitud de reporte por especie: {id_especie}")
        
        pdf_buffer, filename = await report_service.generar_reporte_animales_por_especie(
            id_especie
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValueError as e:
        logger.warning(f"No se encontraron datos: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/animales/por-refugio/pdf",
    summary="Reporte de animales por refugio",
    description="Genera PDF con inventario de animales de un refugio específico"
)
async def generar_pdf_animales_por_refugio(
    id_refugio: str = Query(
        ...,
        description="UUID del refugio",
        example="uuid-de-refugio-aqui"
    )
):
    """
    Genera PDF con animales de un refugio específico.
    
    **Parámetros:**
    - `id_refugio`: UUID del refugio (requerido)
    
    **Ejemplo:** `GET /api/reports/animales/por-refugio/pdf?id_refugio=uuid-aqui`
    """
    try:
        logger.info(f"Solicitud de reporte por refugio: {id_refugio}")
        
        pdf_buffer, filename = await report_service.generar_reporte_animales_por_refugio(
            id_refugio
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValueError as e:
        logger.warning(f"No se encontraron datos: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/animales/general/pdf",
    summary="Reporte general de animales",
    description="Genera PDF con reporte general de todos los animales disponibles"
)
async def generar_pdf_general_animales():
    """
    Genera PDF con reporte general de todos los animales disponibles.
    
    **No requiere parámetros.**
    
    **Ejemplo:** `GET /api/reports/animales/general/pdf`
    """
    try:
        logger.info("Solicitud de reporte general de animales")
        
        pdf_buffer, filename = await report_service.generar_reporte_animales_general()
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValueError as e:
        logger.warning(f"No se encontraron datos: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/animales/filtrados/pdf",
    summary="Reporte de animales con filtros",
    description="Genera PDF con animales usando filtros combinados"
)
async def generar_pdf_animales_filtrados(
    nombre: Optional[str] = Query(
        None,
        description="Búsqueda parcial por nombre",
        example="Max"
    ),
    id_especie: Optional[str] = Query(
        None,
        description="UUID de la especie",
        example="uuid-especie"
    ),
    id_refugio: Optional[str] = Query(
        None,
        description="UUID del refugio",
        example="uuid-refugio"
    ),
    estado_adopcion: Optional[str] = Query(
        None,
        description="Estado de adopción",
        example="disponible"
    ),
    edad_min: Optional[int] = Query(
        None,
        description="Edad mínima",
        example=1,
        ge=0
    ),
    edad_max: Optional[int] = Query(
        None,
        description="Edad máxima",
        example=5,
        ge=0
    )
):
    """
    Genera PDF con animales usando filtros combinados.
    
    **Parámetros (todos opcionales):**
    - `nombre`: Búsqueda parcial por nombre
    - `id_especie`: UUID de la especie
    - `id_refugio`: UUID del refugio
    - `estado_adopcion`: Estado de adopción (disponible, adoptado, etc.)
    - `edad_min`: Edad mínima
    - `edad_max`: Edad máxima
    
    **Ejemplo:** `GET /api/reports/animales/filtrados/pdf?id_especie=uuid&edad_min=1&edad_max=3`
    """
    try:
        logger.info("Solicitud de reporte de animales filtrados")
        
        # Crear DTO con los filtros
        filtros = ReportFilterDTO(
            nombre=nombre,
            id_especie=id_especie,
            id_refugio=id_refugio,
            estado_adopcion=estado_adopcion,
            edad_min=edad_min,
            edad_max=edad_max
        )
        
        pdf_buffer, filename = await report_service.generar_reporte_animales_filtrados(
            filtros
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValueError as e:
        logger.warning(f"No se encontraron datos: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== REPORTES DE CAMPAÑAS ==========

@router.get(
    "/campanias/pdf",
    summary="Reporte de campañas activas",
    description="Genera PDF con reporte de todas las campañas activas"
)
async def generar_pdf_campanias():
    """
    Genera PDF con reporte de campañas activas.
    
    **No requiere parámetros.**
    
    **Ejemplo:** `GET /api/reports/campanias/pdf`
    """
    try:
        logger.info("Solicitud de reporte de campañas")
        
        pdf_buffer, filename = await report_service.generar_reporte_campanias()
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValueError as e:
        logger.warning(f"No se encontraron datos: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== HEALTH CHECK ==========

@router.get(
    "/health",
    summary="Health check del módulo de reportes",
    description="Verifica que el módulo de reportes esté funcionando"
)
async def health_check():
    """
    Verifica que el módulo de reportes esté funcionando correctamente.
    
    **Ejemplo:** `GET /api/reports/health`
    """
    return {
        "status": "healthy",
        "module": "reports",
        "version": "1.0.0",
        "endpoints": {
            "test": "/api/reports/test/pdf",
            "animales_especie": "/api/reports/animales/por-especie/pdf",
            "animales_refugio": "/api/reports/animales/por-refugio/pdf",
            "animales_general": "/api/reports/animales/general/pdf",
            "animales_filtrados": "/api/reports/animales/filtrados/pdf",
            "campanias": "/api/reports/campanias/pdf"
        }
    }
