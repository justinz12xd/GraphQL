# 📋 Queries GraphQL Especiales Disponibles

Este documento lista las **queries especiales** (filtros, relaciones y paginación) disponibles en el GraphQL API.

> ℹ️ **Nota**: Las queries básicas de "listar todos" y "obtener por ID" están disponibles en todos los módulos pero no se documentan aquí.

---

## 🐾 Módulo: Animales (6 queries especiales)

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

### 3. Obtener animales por estado de adopción
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

### 4. Obtener animales por especie
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

### 5. Obtener animales por refugio
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

### 6. Obtener solo animales disponibles
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
| **Animal** | `animales(estadoAdopcion)` | Filtro | `String` opcional |
| **Animal** | `animalesPorEspecie` | Filtro | `idEspecie: ID!` |
| **Animal** | `animalesPorRefugio` | Filtro | `idRefugio: ID!` |
| **Animal** | `animalesDisponibles` | Filtro | ninguno |
| **Causa Urgente** | `causasUrgentesPorRefugio` | Relación | `idRefugio: ID!` |
| **Causa Urgente** | `causasUrgentesPorAnimal` | Relación | `idAnimal: ID!` |
| **Campaña** | `listarCampanias` | Paginación | `limit, offset` |
| **Pago** | `listarPagos` | Paginación | `limit, offset` |
| **Pago** | `pagosPorDonacion` | Relación | `idDonacion: ID!` |

**Total**: **11 queries especiales** + 26 queries básicas (listar/por ID) = **37 queries disponibles**

--
