"""
Servicio de agregación para estadísticas generales del sistema.
Implementa lógica de negocio para queries analíticas que combinan múltiples módulos.
"""

from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository
from app.modules.publicacion.infrastructure.publicacion_repository import PublicacionRepository
from app.modules.pago.infrastructure.pago_repository import PagoRepository


class GeneralAggregationService:
    """Servicio para consultas de agregación general del sistema"""
    
    def __init__(self):
        self.adopcion_repo = AdopcionRepository()
        self.publicacion_repo = PublicacionRepository()
        self.pago_repo = PagoRepository()
    
    async def obtener_actividad_mensual(self, meses: int = 12) -> List[Dict[str, any]]:
        """
        Calcula la actividad mensual del sistema combinando adopciones, publicaciones y donaciones.
        
        Args:
            meses: Número de meses hacia atrás a consultar (default: 12)
        
        Returns:
            Lista de diccionarios con actividad por mes
        """
        # Fecha límite
        fecha_limite = datetime.now(timezone.utc) - timedelta(days=30 * meses)
        
        # Inicializar contadores por mes
        actividad_por_mes = defaultdict(lambda: {
            "total_adopciones": 0,
            "total_publicaciones": 0,
            "total_donaciones": 0,
            "monto_total_donado": 0.0
        })
        
        # 1. Contar adopciones por mes
        try:
            adopciones = await self.adopcion_repo.listar_adopciones()
            estados_excluidos = ['rechazada', 'rechazado', 'cancelada', 'cancelado']
            
            for adopcion in adopciones:
                if adopcion.fecha_adopcion and (adopcion.estado and adopcion.estado.lower() not in estados_excluidos):
                    # Normalizar timezone
                    fecha = adopcion.fecha_adopcion
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
                    
                    if fecha >= fecha_limite:
                        periodo = fecha.strftime("%Y-%m")
                        actividad_por_mes[periodo]["total_adopciones"] += 1
        except Exception:
            pass
        
        # 2. Contar publicaciones por mes
        try:
            publicaciones = await self.publicacion_repo.listar_publicaciones()
            
            for publicacion in publicaciones:
                if publicacion.fecha_publicacion:
                    # Normalizar timezone
                    fecha = publicacion.fecha_publicacion
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
                    
                    if fecha >= fecha_limite:
                        periodo = fecha.strftime("%Y-%m")
                        actividad_por_mes[periodo]["total_publicaciones"] += 1
        except Exception:
            pass
        
        # 3. Contar donaciones (pagos) por mes
        try:
            pagos = await self.pago_repo.listar_pagos()
            
            for pago in pagos:
                # Usar fecha_pago_completado si existe, sino create_at
                fecha_pago = pago.fecha_pago_completado if pago.fecha_pago_completado else pago.create_at
                
                if fecha_pago and pago.estado_pago and pago.estado_pago.lower() in ['completado', 'succeeded', 'success']:
                    # Normalizar timezone
                    fecha = fecha_pago
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
                    
                    if fecha >= fecha_limite:
                        periodo = fecha.strftime("%Y-%m")
                        actividad_por_mes[periodo]["total_donaciones"] += 1
                        actividad_por_mes[periodo]["monto_total_donado"] += float(pago.monto) if pago.monto else 0.0
        except Exception:
            pass
        
        # Convertir a lista ordenada por fecha
        resultado = []
        for periodo in sorted(actividad_por_mes.keys()):
            stats = actividad_por_mes[periodo]
            resultado.append({
                "periodo": periodo,
                "total_adopciones": stats["total_adopciones"],
                "total_publicaciones": stats["total_publicaciones"],
                "total_donaciones": stats["total_donaciones"],
                "monto_total_donado": round(stats["monto_total_donado"], 2)
            })
        
        return resultado
