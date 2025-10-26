"""
Servicio de agregación para estadísticas de voluntarios.
Implementa lógica de negocio para queries analíticas con agregaciones.
"""

from typing import List, Dict
from collections import Counter
from app.modules.voluntario.infrastructure.voluntario_repository import VoluntarioRepository
from app.modules.campania.infrastructure.campania_respository import CampaniaRepository
from app.modules.tipo_campania.infrastructure.tipo_campania_repository import TipoCampaniaRepository


class VoluntarioAggregationService:
    """Servicio para consultas de agregación y estadísticas de voluntarios"""
    
    def __init__(self, repository: VoluntarioRepository):
        self.repository = repository
        self.campania_repo = CampaniaRepository()
        self.tipo_campania_repo = TipoCampaniaRepository()
    
    async def obtener_participacion_por_tipo_campania(self) -> List[Dict[str, any]]:
        """
        Calcula la participación de voluntarios agrupada por tipo de campaña.
        
        Returns:
            Lista de diccionarios con estadísticas por tipo de campaña
        """
        # Obtener todos los voluntarios
        voluntarios = await self.repository.listar_voluntarios()
        
        if not voluntarios:
            return []
        
        # Agrupar voluntarios por tipo de campaña
        voluntarios_por_tipo = {}
        total_voluntarios = 0
        
        for voluntario in voluntarios:
            if voluntario.id_campania:
                try:
                    # 1. Obtener la campaña
                    campania = await self.campania_repo.obtener_campania_por_id(voluntario.id_campania)
                    
                    if campania and campania.id_tipo_campania:
                        # 2. Obtener el tipo de campaña
                        tipo_campania = await self.tipo_campania_repo.obtener_tipo_campania_por_id(campania.id_tipo_campania)
                        
                        if tipo_campania and tipo_campania.nombre:
                            nombre_tipo = tipo_campania.nombre
                            
                            # Inicializar contadores si no existen
                            if nombre_tipo not in voluntarios_por_tipo:
                                voluntarios_por_tipo[nombre_tipo] = {
                                    "total": 0,
                                    "activos": 0,
                                    "inactivos": 0
                                }
                            
                            # Contar voluntario
                            voluntarios_por_tipo[nombre_tipo]["total"] += 1
                            total_voluntarios += 1
                            
                            # Contar por estado
                            if voluntario.estado and voluntario.estado.lower() in ['activo', 'active']:
                                voluntarios_por_tipo[nombre_tipo]["activos"] += 1
                            else:
                                voluntarios_por_tipo[nombre_tipo]["inactivos"] += 1
                                
                except Exception:
                    # Si hay error, continuar con el siguiente
                    continue
        
        if total_voluntarios == 0:
            return []
        
        # Convertir a formato de salida
        resultado = []
        for tipo_campania, stats in sorted(voluntarios_por_tipo.items(), key=lambda x: x[1]["total"], reverse=True):
            porcentaje = (stats["total"] / total_voluntarios * 100) if total_voluntarios > 0 else 0
            resultado.append({
                "tipo_campania": tipo_campania,
                "total_voluntarios": stats["total"],
                "porcentaje_participacion": round(porcentaje, 2),
                "voluntarios_activos": stats["activos"],
                "voluntarios_inactivos": stats["inactivos"]
            })
        
        return resultado
