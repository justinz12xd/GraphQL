# 📋 Queries GraphQL Especiales Disponibles

Este documento lista las **queries especiales** (filtros, relaciones y paginación) disponibles en el GraphQL API.

> ℹ️ **Nota**: Las queries básicas de "listar todos" y "obtener por ID" están disponibles en todos los módulos pero no se documentan aquí.

---

## 🐾 Módulo: Animales (9 queries especiales)

### 1. Buscar animales por nombre 🆕
**Descripción**: Busca animales por nombre (búsqueda parcial, case-insensitive)

```graphql
query BuscarAnimales($nombre: String!) {
  buscarAnimales(nombre: $nombre) {
    idAnimal
    nombre
    especie
    edad
    fotos
    estadoAdopcion
    descripcion
  }
}
```

**Variables**:
```json
{
  "nombre": "Max"
}
```

**Ejemplos de búsqueda**:
- `"Max"` → encuentra "Max", "Maximus", "Maxwell"
- `"luna"` → encuentra "Luna", "Lunita" (case-insensitive)
- `"to"` → encuentra "Toto", "Tony", "Tobby"

### 2. Filtrar animales por rango de edad 🆕
**Descripción**: Filtra animales por edad mínima y/o máxima (ambos parámetros opcionales)

```graphql
query AnimalesPorEdad($edadMin: Int, $edadMax: Int) {
  animalesPorEdad(edadMin: $edadMin, edadMax: $edadMax) {
    idAnimal
    nombre
    especie
    edad
    fotos
    estadoAdopcion
  }
}
```

**Variables - Ejemplos de uso**:

Cachorros (0-1 años):
```json
{
  "edadMin": 0,
  "edadMax": 1
}
```

Adultos jóvenes (1-3 años):
```json
{
  "edadMin": 1,
  "edadMax": 3
}
```

Adultos (3-7 años):
```json
{
  "edadMin": 3,
  "edadMax": 7
}
```

Senior (7+ años):
```json
{
  "edadMin": 7
}
```

Menores de 5 años:
```json
{
  "edadMax": 5
}
```

**Nota**: Los animales sin edad (`null`) no aparecen en los resultados filtrados.

### 3. Filtros combinados (Query más potente) 🆕🔥
**Descripción**: Combina múltiples filtros simultáneamente. Todos los parámetros son opcionales.

```graphql
query AnimalesFiltrados(
  $nombre: String
  $idEspecie: ID
  $idRefugio: ID
  $estadoAdopcion: String
  $edadMin: Int
  $edadMax: Int
) {
  animalesFiltrados(
    nombre: $nombre
    idEspecie: $idEspecie
    idRefugio: $idRefugio
    estadoAdopcion: $estadoAdopcion
    edadMin: $edadMin
    edadMax: $edadMax
  ) {
    idAnimal
    nombre
    especie
    edad
    fotos
    estadoAdopcion
    descripcion
    idRefugio
  }
}
```

**Variables - Ejemplos de uso**:

Perros cachorros disponibles:
```json
{
  "idEspecie": "uuid-de-perro",
  "edadMin": 0,
  "edadMax": 1,
  "estadoAdopcion": "disponible"
}
```

Gatos en un refugio específico:
```json
{
  "idEspecie": "uuid-de-gato",
  "idRefugio": "uuid-del-refugio"
}
```

Buscar "Max" solo disponibles:
```json
{
  "nombre": "Max",
  "estadoAdopcion": "disponible"
}
```

Adultos de cualquier especie en un refugio:
```json
{
  "idRefugio": "uuid-del-refugio",
  "edadMin": 3,
  "edadMax": 7
}
```

**Ventajas**:
- ✅ Combina todos los filtros disponibles
- ✅ Todos los parámetros opcionales
- ✅ Ideal para buscadores avanzados
- ✅ Una sola llamada al servidor

### 4. Paginación con filtros 🆕📄
**Descripción**: Obtiene animales de forma paginada con todos los filtros disponibles. Incluye metadata de paginación.

```graphql
query AnimalesPaginados(
  $limit: Int = 20
  $offset: Int = 0
  $nombre: String
  $idEspecie: ID
  $idRefugio: ID
  $estadoAdopcion: String
  $edadMin: Int
  $edadMax: Int
) {
  animalesPaginados(
    limit: $limit
    offset: $offset
    nombre: $nombre
    idEspecie: $idEspecie
    idRefugio: $idRefugio
    estadoAdopcion: $estadoAdopcion
    edadMin: $edadMin
    edadMax: $edadMax
  ) {
    animales {
      idAnimal
      nombre
      especie
      edad
      fotos
      estadoAdopcion
    }
    totalCount
    hasMore
    totalPages
    currentPage
    limit
    offset
  }
}
```

**Variables - Ejemplos de uso**:

Primera página (20 resultados):
```json
{
  "limit": 20,
  "offset": 0
}
```

Segunda página:
```json
{
  "limit": 20,
  "offset": 20
}
```

Tercera página:
```json
{
  "limit": 20,
  "offset": 40
}
```

Con filtros (perros disponibles, paginados):
```json
{
  "limit": 10,
  "offset": 0,
  "idEspecie": "uuid-perro",
  "estadoAdopcion": "disponible"
}
```

**Metadata retornada**:
- `totalCount`: Total de resultados (sin paginar)
- `hasMore`: ¿Hay más páginas disponibles?
- `totalPages`: Número total de páginas
- `currentPage`: Página actual (comienza en 1)
- `limit`: Cantidad de resultados por página
- `offset`: Desplazamiento actual

**Ventajas**:
- ✅ Carga resultados en bloques (mejor performance)
- ✅ Scroll infinito o paginación clásica
- ✅ Combina con todos los filtros
- ✅ Metadata completa para UI de paginación

### 5. Ordenamiento 🆕🔀
**Descripción**: Obtiene animales ordenados por diferentes campos (nombre, edad, fecha de creación).

```graphql
query AnimalesOrdenados($orderBy: String = "nombre", $order: String = "asc") {
  animalesOrdenados(orderBy: $orderBy, order: $order) {
    idAnimal
    nombre
    edad
    fechaCreacion
    especie
  }
}
```

**Variables - Ejemplos de uso**:

Ordenar por nombre A-Z:
```json
{
  "orderBy": "nombre",
  "order": "asc"
}
```

Ordenar por nombre Z-A:
```json
{
  "orderBy": "nombre",
  "order": "desc"
}
```

Ordenar por edad (más jóvenes primero):
```json
{
  "orderBy": "edad",
  "order": "asc"
}
```

Ordenar por edad (más viejos primero):
```json
{
  "orderBy": "edad",
  "order": "desc"
}
```

Ordenar por fecha de creación (más recientes primero):
```json
{
  "orderBy": "fecha_creacion",
  "order": "desc"
}
```

**Campos disponibles para orderBy**:
- `"nombre"` - Nombre del animal (alfabético, case-insensitive)
- `"edad"` - Edad del animal (numérico, null al final)
- `"fecha_creacion"` - Fecha de registro (más recientes primero con desc)

**Ventajas**:
- ✅ Ordenamiento flexible por 3 campos diferentes
- ✅ Control ascendente/descendente
- ✅ Animales sin datos (null) van al final
- ✅ Compatible con todos los animales

### 6. Obtener animales por estado de adopción
**Descripción**: Filtra animales según su estado de adopción (disponible, adoptado, en proceso, etc.)

```graphql
query GetAnimalesPorEstado {
  animales(estadoAdopcion: "disponible") {
    idAnimal
    nombre
    especie
    edad
    fotos
    estadoAdopcion
  }
}
```

**Estados posibles**: `"disponible"`, `"adoptado"`, `"en_proceso"`, `"reservado"`

### 7. Obtener animales por especie
**Descripción**: Filtra todos los animales de una especie específica

```graphql
query GetAnimalesPorEspecie($especieId: ID!) {
  animalesPorEspecie(idEspecie: $especieId) {
    idAnimal
    nombre
    edad
    fotos
    estadoAdopcion
  }
}
```

**Variables**:
```json
{
  "especieId": "uuid-de-la-especie"
}
```

### 8. Obtener animales por refugio
**Descripción**: Obtiene todos los animales alojados en un refugio específico

```graphql
query GetAnimalesPorRefugio($refugioId: ID!) {
  animalesPorRefugio(idRefugio: $refugioId) {
    idAnimal
    nombre
    especie
    edad
    estadoAdopcion
  }
}
```

**Variables**:
```json
{
  "refugioId": "uuid-del-refugio"
}
```

### 9. Obtener solo animales disponibles
**Descripción**: Atajo para obtener solo animales con estado "disponible"

```graphql
query GetAnimalesDisponibles {
  animalesDisponibles {
    idAnimal
    nombre
    especie
    edad
    fotos
    descripcion
    idRefugio
  }
}
```

---

## � Módulo: Causas Urgentes (2 queries especiales)

### 1. Obtener causas urgentes por refugio
**Descripción**: Todas las causas urgentes asociadas a un refugio

```graphql
query GetCausasUrgentesPorRefugio($refugioId: ID!) {
  causasUrgentesPorRefugio(idRefugio: $refugioId) {
    idCausaUrgente
    titulo
    descripcion
    meta
    fechaLimite
    idAnimal
    fotos
  }
}
```

**Variables**:
```json
{
  "refugioId": "uuid-del-refugio"
}
```

### 2. Obtener causas urgentes por animal
**Descripción**: Causas urgentes específicas de un animal (ej: operación, vacunas)

```graphql
query GetCausasUrgentesPorAnimal($animalId: ID!) {
  causasUrgentesPorAnimal(idAnimal: $animalId) {
    idCausaUrgente
    titulo
    descripcion
    meta
    fechaLimite
    idRefugio
    fotos
  }
}
```

**Variables**:
```json
{
  "animalId": "uuid-del-animal"
}
```

---

## 🎯 Módulo: Campañas (1 query con paginación)

### Listar campañas con paginación
**Descripción**: Obtiene campañas de forma paginada para evitar cargar todas a la vez

```graphql
query GetCampaniasPaginadas($limit: Int, $offset: Int) {
  listarCampanias(limit: $limit, offset: $offset) {
    idCampania
    idTipoCampania
    titulo
    descripcion
    fechaInicio
    fechaFin
    lugar
    organizador
    estado
  }
}
```

**Variables** (valores por defecto: limit=50, offset=0):
```json
{
  "limit": 10,
  "offset": 0
}
```

**Ejemplo de paginación**:
- Página 1: `limit: 10, offset: 0`
- Página 2: `limit: 10, offset: 10`
- Página 3: `limit: 10, offset: 20`

---

## 💳 Módulo: Pagos (2 queries especiales)

### 1. Listar pagos con paginación
**Descripción**: Lista todos los pagos de forma paginada

```graphql
query GetPagosPaginados($limit: Int, $offset: Int) {
  listarPagos(limit: $limit, offset: $offset) {
    idPago
    monto
    metodoPago
    estadoPago
    fechaPago
    idDonacion
  }
}
```

**Variables** (valores por defecto: limit=50, offset=0):
```json
{
  "limit": 20,
  "offset": 0
}
```

### 2. Obtener pagos por donación
**Descripción**: Historial de todos los pagos relacionados a una donación específica

```graphql
query GetPagosPorDonacion($donacionId: ID!) {
  pagosPorDonacion(idDonacion: $donacionId) {
    idPago
    monto
    metodoPago
    estadoPago
    fechaPago
    stripePaymentIntentId
    fechaPagoCompletado
  }
}
```

**Variables**:
```json
{
  "donacionId": "uuid-de-la-donacion"
}
```

---

## � Queries Combinadas (Casos de Uso Reales)

### 1. Dashboard de Animal Completo
**Caso de uso**: Página de detalle de un animal con causas urgentes relacionadas

```graphql
query GetAnimalCompleto($animalId: ID!) {
  animal(idAnimal: $animalId) {
    idAnimal
    nombre
    especie
    edad
    estado
    descripcion
    fotos
    estadoAdopcion
    idRefugio
  }
  
  causasUrgentesPorAnimal(idAnimal: $animalId) {
    idCausaUrgente
    titulo
    descripcion
    meta
    fechaLimite
    fotos
  }
}
```

**Variables**:
```json
{
  "animalId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### 2. Dashboard de Refugio Completo
**Caso de uso**: Vista general de un refugio con sus animales y causas urgentes

```graphql
query GetRefugioCompleto($refugioId: ID!) {
  refugio(idRefugio: $refugioId) {
    idRefugio
    nombre
    direccion
    telefono
    capacidad
    estado
    fechaCreacion
  }
  
  animalesPorRefugio(idRefugio: $refugioId) {
    idAnimal
    nombre
    especie
    estadoAdopcion
  }
  
  causasUrgentesPorRefugio(idRefugio: $refugioId) {
    idCausaUrgente
    titulo
    meta
    fechaLimite
  }
}
```

**Variables**:
```json
{
  "refugioId": "uuid-del-refugio"
}
```

### 3. Catálogo de Animales con Filtros
**Caso de uso**: Página principal con animales disponibles de una especie específica

```graphql
query GetCatalogoAnimales($especieId: ID!) {
  animalesPorEspecie(idEspecie: $especieId) {
    idAnimal
    nombre
    edad
    fotos
    estadoAdopcion
    descripcion
  }
  
  especies {
    id
    nombre
  }
}
```

**Variables**:
```json
{
  "especieId": "uuid-de-especie-perro"
}
```

---

## � Resumen de Queries Especiales

| Módulo | Query | Tipo | Parámetros |
|--------|-------|------|------------|
| **Animal** | `buscarAnimales` 🆕 | Búsqueda | `nombre: String!` |
| **Animal** | `animalesPorEdad` 🆕 | Filtro | `edadMin: Int, edadMax: Int` (opcionales) |
| **Animal** | `animalesFiltrados` 🆕🔥 | Filtro Combinado | `nombre, idEspecie, idRefugio, estadoAdopcion, edadMin, edadMax` (todos opcionales) |
| **Animal** | `animalesPaginados` 🆕📄 | Paginación + Filtros | `limit, offset, nombre, idEspecie, idRefugio, estadoAdopcion, edadMin, edadMax` (con metadata) |
| **Animal** | `animalesOrdenados` 🆕🔀 | Ordenamiento | `orderBy: String, order: String` (nombre/edad/fecha_creacion + asc/desc) |
| **Animal** | `animales(estadoAdopcion)` | Filtro | `String` opcional |
| **Animal** | `animalesPorEspecie` | Filtro | `idEspecie: ID!` |
| **Animal** | `animalesPorRefugio` | Filtro | `idRefugio: ID!` |
| **Animal** | `animalesDisponibles` | Filtro | ninguno |
| **Causa Urgente** | `causasUrgentesPorRefugio` | Relación | `idRefugio: ID!` |
| **Causa Urgente** | `causasUrgentesPorAnimal` | Relación | `idAnimal: ID!` |
| **Campaña** | `listarCampanias` | Paginación | `limit, offset` |
| **Pago** | `listarPagos` | Paginación | `limit, offset` |
| **Pago** | `pagosPorDonacion` | Relación | `idDonacion: ID!` |

**Total**: **14 queries especiales** + 26 queries básicas (listar/por ID) = **40 queries disponibles** 🎉

---

## 📊 Módulo: Estadísticas y Reportes (4 queries de agregación)

### 1. Especies más adoptadas
**Descripción**: Ranking de especies por número de adopciones exitosas

```graphql
query EspeciesMasAdoptadas($limite: Int = 10) {
  especiesMasAdoptadas(limite: $limite) {
    especie
    totalAdopciones
  }
}
```

**Variables**:
```json
{
  "limite": 5
}
```

### 2. Adopciones por mes
**Descripción**: Tendencia mensual de adopciones con desglose por especie

```graphql
query AdopcionesPorMes($meses: Int = 12) {
  adopcionesPorMes(meses: $meses) {
    periodo
    totalAdopciones
    desglosePorEspecie {
      especie
      cantidad
    }
  }
}
```

**Variables**:
```json
{
  "meses": 6
}
```

### 3. Participación de voluntarios por tipo de campaña
**Descripción**: Voluntarios agrupados por tipo de campaña con estado activo/inactivo

```graphql
query ParticipacionVoluntarios {
  participacionVoluntariosPorTipoCampania {
    tipoCampania
    totalVoluntarios
    voluntariosActivos
    voluntariosInactivos
  }
}
```

### 4. Actividad mensual del sistema
**Descripción**: Resumen mensual de adopciones, publicaciones y donaciones

```graphql
query ActividadMensual($meses: Int = 12) {
  actividadMensual(meses: $meses) {
    periodo
    totalAdopciones
    totalPublicaciones
    totalDonaciones
    montoTotalDonado
  }
}
```

**Variables**:
```json
{
  "meses": 6
}
```

---

