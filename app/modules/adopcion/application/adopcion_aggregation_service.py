"""
Servicio de agregación para estadísticas de adopciones.
Implementa lógica de negocio para queries analíticas con agregaciones.
"""

from typing import List, Dict
from collections import Counter
from datetime import datetime, timedelta, timezone
from app.modules.adopcion.infrastructure.adopcion_repository import AdopcionRepository
from app.modules.publicacion.infrastructure.publicacion_repository import PublicacionRepository
from app.modules.animal.infraestructure.animal_repository import AnimalRepository


class AdopcionAggregationService:
    """Servicio para consultas de agregación y estadísticas de adopciones"""
    
    def __init__(self, repository: AdopcionRepository):
        self.repository = repository
        self.publicacion_repo = PublicacionRepository()
        self.animal_repo = AnimalRepository()
    
    async def obtener_especies_mas_adoptadas(self) -> List[Dict[str, any]]:
        """
        Calcula las especies más adoptadas con conteo y porcentaje.
        
        Returns:
            Lista de diccionarios con: categoria (especie), cantidad, porcentaje
        """
        # Obtener todas las adopciones
        adopciones = await self.repository.listar_adopciones()
        
        # Filtrar adopciones válidas (excluir rechazadas/canceladas)
        estados_excluidos = ['rechazada', 'rechazado', 'cancelada', 'cancelado']
        adopciones_completadas = [a for a in adopciones if a.estado and a.estado.lower() not in estados_excluidos]
        
        if not adopciones_completadas:
            return []
        
        # Para cada adopción, obtener la especie del animal
        especies_adoptadas = []
        
        for adopcion in adopciones_completadas:
            if adopcion.id_publicacion:
                try:
                    # 1. Obtener la publicación
                    publicacion = await self.publicacion_repo.obtener_publicacion_por_id(adopcion.id_publicacion)
                    
                    if publicacion and publicacion.id_animal:
                        # 2. Obtener el animal
                        animal = await self.animal_repo.obtener_animal_por_id(publicacion.id_animal)
                        
                        if animal and animal.especie:
                            # 3. Agregar la especie a la lista
                            especies_adoptadas.append(animal.especie)
                except Exception:
                    # Si hay error en alguna consulta, continuar con la siguiente
                    continue
        
        if not especies_adoptadas:
            return []
        
        # Contar especies
        contador_especies = Counter(especies_adoptadas)
        total_adopciones = len(especies_adoptadas)
        
        # Convertir a formato de salida
        resultado = []
        for especie, cantidad in contador_especies.most_common():
            porcentaje = (cantidad / total_adopciones * 100) if total_adopciones > 0 else 0
            resultado.append({
                "categoria": especie,
                "cantidad": cantidad,
                "porcentaje": round(porcentaje, 2)
            })
        
        return resultado
    
    async def obtener_adopciones_por_mes(self, meses: int = 12) -> List[Dict[str, any]]:
        """
        Calcula cuántas adopciones hubo por mes en los últimos N meses.
        
        Args:
            meses: Número de meses hacia atrás a consultar (default: 12)
        
        Returns:
            Lista de diccionarios con: periodo, total_adopciones, especies_adoptadas
        """
        # Obtener todas las adopciones
        adopciones = await self.repository.listar_adopciones()
        
        # Filtrar adopciones válidas (excluir rechazadas/canceladas)
        estados_excluidos = ['rechazada', 'rechazado', 'cancelada', 'cancelado']
        adopciones_completadas = [a for a in adopciones if a.estado and a.estado.lower() not in estados_excluidos]
        
        # Fecha límite (N meses atrás) - con timezone aware
        fecha_limite = datetime.now(timezone.utc) - timedelta(days=30 * meses)
        
        # Filtrar por fecha (manejar tanto fechas con y sin timezone)
        adopciones_recientes = []
        for a in adopciones_completadas:
            if a.fecha_adopcion:
                # Si la fecha no tiene timezone, asumimos UTC
                fecha_adopcion = a.fecha_adopcion
                if fecha_adopcion.tzinfo is None:
                    fecha_adopcion = fecha_adopcion.replace(tzinfo=timezone.utc)
                
                if fecha_adopcion >= fecha_limite:
                    adopciones_recientes.append(a)
        
        # Agrupar por mes
        contador_por_mes = Counter()
        especies_por_mes = {}
        
        for adopcion in adopciones_recientes:
            # Formato: "2024-01" 
            periodo = adopcion.fecha_adopcion.strftime("%Y-%m")
            contador_por_mes[periodo] += 1
            
            # Inicializar lista de especies si no existe
            if periodo not in especies_por_mes:
                especies_por_mes[periodo] = []
            
            # Obtener la especie real del animal adoptado
            if adopcion.id_publicacion:
                try:
                    # 1. Obtener la publicación
                    publicacion = await self.publicacion_repo.obtener_publicacion_por_id(adopcion.id_publicacion)
                    
                    if publicacion and publicacion.id_animal:
                        # 2. Obtener el animal
                        animal = await self.animal_repo.obtener_animal_por_id(publicacion.id_animal)
                        
                        if animal and animal.especie:
                            # 3. Agregar la especie
                            especies_por_mes[periodo].append(animal.especie)
                except Exception:
                    # Si hay error, continuar
                    continue
        
        # Convertir a formato de salida ordenado por fecha
        resultado = []
        for periodo in sorted(contador_por_mes.keys()):
            # Contar especies en este período
            especies_contador = Counter(especies_por_mes.get(periodo, []))
            total_periodo = contador_por_mes[periodo]
            
            especies_adoptadas = [
                {
                    "categoria": especie,
                    "cantidad": cantidad,
                    "porcentaje": round((cantidad / total_periodo * 100), 2) if total_periodo > 0 else 0
                }
                for especie, cantidad in especies_contador.most_common()
            ]
            
            resultado.append({
                "periodo": periodo,
                "total_adopciones": total_periodo,
                "especies_adoptadas": especies_adoptadas
            })
        
        return resultado
    
    async def obtener_estadisticas_generales(self) -> Dict[str, any]:
        """
        Obtiene estadísticas generales de adopciones.
        
        Returns:
            Diccionario con métricas generales
        """
        # Obtener todas las adopciones
        adopciones = await self.repository.listar_adopciones()
        
        # Filtrar por estado (excluir rechazadas/canceladas)
        estados_excluidos = ['rechazada', 'rechazado', 'cancelada', 'cancelado']
        adopciones_completadas = [a for a in adopciones if a.estado and a.estado.lower() not in estados_excluidos]
        
        # Fecha actual con timezone
        ahora = datetime.now(timezone.utc)
        primer_dia_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        primer_dia_anio = ahora.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Contar adopciones del mes actual
        adopciones_mes = []
        for a in adopciones_completadas:
            if a.fecha_adopcion:
                fecha = a.fecha_adopcion
                if fecha.tzinfo is None:
                    fecha = fecha.replace(tzinfo=timezone.utc)
                if fecha >= primer_dia_mes:
                    adopciones_mes.append(a)
        
        # Contar adopciones del año actual
        adopciones_anio = []
        for a in adopciones_completadas:
            if a.fecha_adopcion:
                fecha = a.fecha_adopcion
                if fecha.tzinfo is None:
                    fecha = fecha.replace(tzinfo=timezone.utc)
                if fecha >= primer_dia_anio:
                    adopciones_anio.append(a)
        
        return {
            "total_adopciones": len(adopciones_completadas),
            "adopciones_mes_actual": len(adopciones_mes),
            "adopciones_anio_actual": len(adopciones_anio),
            "promedio_dias_adopcion": None,  # Requiere fecha de ingreso del animal
            "especies_mas_adoptadas": await self.obtener_especies_mas_adoptadas(),
            "refugios_mas_adopciones": [],  # Se implementará en Query 3
            "tendencia_mensual": await self.obtener_adopciones_por_mes(12)
        }
