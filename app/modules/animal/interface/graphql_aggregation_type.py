"""
Tipos de agregación para estadísticas de animales.
"""

import strawberry
from typing import List, Optional


@strawberry.type(description="Conteo agrupado de elementos")
class ConteoType:
    """Representa un conteo agrupado genérico."""
    
    categoria: str = strawberry.field(description="Nombre de la categoría")
    cantidad: int = strawberry.field(description="Cantidad de elementos en esta categoría")
    porcentaje: float = strawberry.field(description="Porcentaje del total (%)")


@strawberry.type(description="Estadísticas agregadas de animales")
class EstadisticasAnimalesType:
    """Estadísticas generales y agregadas de todos los animales."""
    
    total_animales: int = strawberry.field(description="Total de animales registrados")
    total_disponibles: int = strawberry.field(description="Animales disponibles para adopción")
    total_adoptados: int = strawberry.field(description="Animales adoptados")
    total_en_proceso: int = strawberry.field(description="Animales en proceso de adopción")
    
    # Agregaciones por especie
    animales_por_especie: List[ConteoType] = strawberry.field(
        description="Distribución de animales por especie"
    )
    
    # Agregaciones por estado
    animales_por_estado: List[ConteoType] = strawberry.field(
        description="Distribución de animales por estado de adopción"
    )
    
    # Métricas numéricas
    edad_promedio: Optional[float] = strawberry.field(
        description="Edad promedio de los animales (en años)"
    )
    edad_minima: Optional[int] = strawberry.field(description="Edad del animal más joven")
    edad_maxima: Optional[int] = strawberry.field(description="Edad del animal más viejo")
