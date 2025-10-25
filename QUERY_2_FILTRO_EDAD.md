# 🎂 Query #2: Filtro por Rango de Edad

## ✅ Implementación Completada

**Fecha**: 2025-10-25  
**Commit**: Query #2 - Filtro de animales por rango de edad

---

## 📝 Cambios Realizados

### 1. Service Layer (`animal_service.py`)
Agregado método:
```python
async def obtener_animales_por_rango_edad(
    self, 
    edad_min: Optional[int] = None, 
    edad_max: Optional[int] = None
) -> List[Animal]:
    """Filtrar animales por rango de edad (ambos parámetros opcionales)"""
    todos_animales = await self.repo.listar_animales()
    
    resultado = []
    for animal in todos_animales:
        # Si no tiene edad, no incluir en resultados filtrados
        if animal.edad is None:
            continue
        
        # Verificar edad mínima
        if edad_min is not None and animal.edad < edad_min:
            continue
        
        # Verificar edad máxima
        if edad_max is not None and animal.edad > edad_max:
            continue
        
        resultado.append(animal)
    
    return resultado
```

### 2. GraphQL Query Layer (`graphql_query.py`)
Agregado endpoint:
```python
@strawberry.field
async def animales_por_edad(
    self, 
    edad_min: Optional[int] = None, 
    edad_max: Optional[int] = None
) -> List[AnimalType]:
    """Filtrar animales por rango de edad (ambos parámetros opcionales)"""
```

### 3. Documentación (`GRAPHQL_QUERIES.md`)
- Actualizado contador de queries: 6 queries en módulo Animal
- Agregada documentación de `animalesPorEdad`
- Total queries: 37 (11 especiales + 26 básicas)

---

## 🧪 Cómo Probar

### Opción 1: Cachorros (0-1 años)
```graphql
query CachorrosDisponibles {
  animalesPorEdad(edadMin: 0, edadMax: 1) {
    idAnimal
    nombre
    edad
    especie
    fotos
    estadoAdopcion
  }
}
```

### Opción 2: Adultos Jóvenes (1-3 años)
```graphql
query AdultosJovenes {
  animalesPorEdad(edadMin: 1, edadMax: 3) {
    idAnimal
    nombre
    edad
    especie
  }
}
```

### Opción 3: Senior (7+ años)
```graphql
query AnimalesSenior {
  animalesPorEdad(edadMin: 7) {
    idAnimal
    nombre
    edad
    especie
  }
}
```

### Opción 4: Con Variables (Recomendado)
**Query:**
```graphql
query AnimalesPorEdad($min: Int, $max: Int) {
  animalesPorEdad(edadMin: $min, edadMax: $max) {
    idAnimal
    nombre
    edad
    especie
    estadoAdopcion
  }
}
```

**Variables:**
```json
{
  "min": 0,
  "max": 3
}
```

### Opción 5: Solo edad máxima
```graphql
query MenoresDe5 {
  animalesPorEdad(edadMax: 5) {
    idAnimal
    nombre
    edad
  }
}
```

---

## 🎯 Casos de Uso Frontend

### Filtro Dropdown por Categoría de Edad
```tsx
export function FiltroEdad() {
  const categorias = [
    { label: "Cachorros (0-1 años)", min: 0, max: 1 },
    { label: "Jóvenes (1-3 años)", min: 1, max: 3 },
    { label: "Adultos (3-7 años)", min: 3, max: 7 },
    { label: "Senior (7+ años)", min: 7, max: null },
  ];

  const [filtro, setFiltro] = useState(null);

  const { data } = useGraphQL({
    query: `
      query AnimalesPorEdad($min: Int, $max: Int) {
        animalesPorEdad(edadMin: $min, edadMax: $max) {
          idAnimal
          nombre
          edad
          especie
          fotos
        }
      }
    `,
    variables: filtro,
  });

  return (
    <select onChange={(e) => {
      const cat = categorias[e.target.value];
      setFiltro({ min: cat.min, max: cat.max });
    }}>
      <option value="">Todas las edades</option>
      {categorias.map((cat, i) => (
        <option key={i} value={i}>{cat.label}</option>
      ))}
    </select>
  );
}
```

### Slider de Rango de Edad
```tsx
export function RangoEdadSlider() {
  const [edadMin, setEdadMin] = useState(0);
  const [edadMax, setEdadMax] = useState(15);

  const { data } = useGraphQL({
    query: `
      query AnimalesPorEdad($min: Int, $max: Int) {
        animalesPorEdad(edadMin: $min, edadMax: $max) {
          idAnimal
          nombre
          edad
        }
      }
    `,
    variables: { min: edadMin, max: edadMax },
  });

  return (
    <div>
      <label>Edad: {edadMin} - {edadMax} años</label>
      <input 
        type="range" 
        min="0" 
        max="15" 
        value={edadMin}
        onChange={(e) => setEdadMin(Number(e.target.value))}
      />
      <input 
        type="range" 
        min="0" 
        max="15" 
        value={edadMax}
        onChange={(e) => setEdadMax(Number(e.target.value))}
      />
    </div>
  );
}
```

---

## ✨ Características

✅ **Parámetros opcionales**: Puedes usar solo `edadMin`, solo `edadMax`, o ambos  
✅ **Filtrado seguro**: Excluye animales sin edad (`null`)  
✅ **Rangos inclusivos**: `edadMin: 1, edadMax: 3` incluye 1, 2 y 3 años  
✅ **Flexible**: Combina con otros filtros (especie, refugio, etc.)

---

## 📊 Ejemplos de Rangos Comunes

| Categoría | `edadMin` | `edadMax` | Descripción |
|-----------|-----------|-----------|-------------|
| Cachorros | 0 | 1 | Animales de 0-1 años |
| Jóvenes | 1 | 3 | Animales de 1-3 años |
| Adultos | 3 | 7 | Animales de 3-7 años |
| Senior | 7 | - | Animales de 7+ años |
| Todos < 5 años | - | 5 | Menores de 5 años |
| Todos > 2 años | 2 | - | Mayores de 2 años |

---

## 🔍 Combinación con Otras Queries

### Ejemplo: Cachorros Disponibles de Especie Perro
```graphql
query CachorrosPerrosDisponibles($especieId: ID!) {
  # Primero obtén cachorros
  cachorros: animalesPorEdad(edadMin: 0, edadMax: 1) {
    idAnimal
    nombre
    edad
    estadoAdopcion
    idEspecie
  }
  
  # Luego puedes filtrar en cliente por especie y estado
}
```

**Nota**: Para combinar múltiples filtros simultáneamente, usa la Query #3 (Filtros Combinados) que implementaremos después.

---

## 📊 Estado de Implementación

| Query | Estado |
|-------|--------|
| ✅ Buscar por nombre | COMPLETADO |
| ✅ Filtro por edad | COMPLETADO |
| ⏳ Filtros combinados | Pendiente |
| ⏳ Paginación | Pendiente |
| ⏳ Ordenamiento | Pendiente |

---

## 🚀 Siguiente Paso

**Query #3**: Filtros combinados (nombre + edad + especie + refugio + estado + paginación)

Ejecuta el commit y avísame para implementar la siguiente query.

---

> 💡 **Tip de UX**: Muestra la cantidad de resultados en tiempo real:
> ```tsx
> <p>Encontrados: {data?.animalesPorEdad.length || 0} animales</p>
> ```
