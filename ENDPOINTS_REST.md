# API Endpoints - Love4Pets REST API

## 🌐 Información del Servidor
- **Base URL**: `http://localhost:8080`
- **Puerto**: `8080`
- **Protocolo**: HTTP/REST

> **Nota**: Todas las rutas deben ser precedidas por la base URL. Por ejemplo: `http://localhost:8080/animals`

---

## 🐾 Animales
- **GET** `/animals` - Obtener todos los animales
- **POST** `/animals` - Crear un nuevo animal
- **GET** `/animals/{id}` - Obtener un animal por ID
- **PUT** `/animals/{id}` - Actualizar un animal
- **DELETE** `/animals/{id}` - Eliminar un animal

## 🦴 Especies
- **GET** `/especies` - Obtener todas las especies
- **POST** `/especies` - Crear una nueva especie
- **GET** `/especies/{id}` - Obtener una especie por ID
- **PUT** `/especies/{id}` - Actualizar una especie
- **DELETE** `/especies/{id}` - Eliminar una especie

## 👨‍💼 Supervisores
- **GET** `/supervisores` - Obtener todos los supervisores
- **POST** `/supervisores` - Crear un nuevo supervisor
- **GET** `/supervisores/{id}` - Obtener un supervisor por ID
- **PUT** `/supervisores/{id}` - Actualizar un supervisor
- **DELETE** `/supervisores/{id}` - Eliminar un supervisor

## 📢 Campañas
- **GET** `/campanias` - Obtener todas las campañas
- **POST** `/campanias` - Crear una nueva campaña
- **GET** `/campanias/{id}` - Obtener una campaña por ID
- **PUT** `/campanias/{id}` - Actualizar una campaña
- **DELETE** `/campanias/{id}` - Eliminar una campaña

## 🚨 Causas Urgentes
- **GET** `/causas_urgentes` - Obtener todas las causas urgentes
- **POST** `/causas_urgentes` - Crear una nueva causa urgente
- **GET** `/causas_urgentes/{id}` - Obtener una causa urgente por ID
- **PUT** `/causas_urgentes/{id}` - Actualizar una causa urgente
- **DELETE** `/causas_urgentes/{id}` - Eliminar una causa urgente

## 👥 Usuarios
- **GET** `/usuarios` - Obtener todos los usuarios
- **POST** `/usuarios` - Crear un nuevo usuario
- **GET** `/usuarios/{id}` - Obtener un usuario por ID
- **PUT** `/usuarios/{id}` - Actualizar un usuario
- **DELETE** `/usuarios/{id}` - Eliminar un usuario

## 📋 Tipo de Campañas
- **GET** `/tipo_campanias` - Obtener todos los tipos de campañas
- **POST** `/tipo_campanias` - Crear un nuevo tipo de campaña
- **GET** `/tipo_campanias/{id}` - Obtener un tipo de campaña por ID
- **PUT** `/tipo_campanias/{id}` - Actualizar un tipo de campaña
- **DELETE** `/tipo_campanias/{id}` - Eliminar un tipo de campaña

## 🙋 Voluntarios
- **GET** `/voluntarios` - Obtener todos los voluntarios
- **POST** `/voluntarios` - Crear un nuevo voluntario
- **GET** `/voluntarios/{id}` - Obtener un voluntario por ID
- **PUT** `/voluntarios/{id}` - Actualizar un voluntario
- **DELETE** `/voluntarios/{id}` - Eliminar un voluntario

## 📝 Publicaciones
- **GET** `/publicaciones` - Obtener todas las publicaciones
- **POST** `/publicaciones` - Crear una nueva publicación
- **GET** `/publicaciones/{id}` - Obtener una publicación por ID
- **PUT** `/publicaciones/{id}` - Actualizar una publicación
- **DELETE** `/publicaciones/{id}` - Eliminar una publicación

## 🏠 Adopciones
- **GET** `/adopciones` - Obtener todas las adopciones
- **POST** `/adopciones` - Crear una nueva adopción
- **GET** `/adopciones/{id}` - Obtener una adopción por ID
- **PUT** `/adopciones/{id}` - Actualizar una adopción
- **DELETE** `/adopciones/{id}` - Eliminar una adopción

## 🏡 Refugios
- **GET** `/refugios` - Obtener todos los refugios
- **POST** `/refugios` - Crear un nuevo refugio
- **GET** `/refugios/{id}` - Obtener un refugio por ID
- **PUT** `/refugios/{id}` - Actualizar un refugio
- **DELETE** `/refugios/{id}` - Eliminar un refugio

## 📊 Seguimientos
- **GET** `/seguimientos` - Obtener todos los seguimientos
- **POST** `/seguimientos` - Crear un nuevo seguimiento
- **GET** `/seguimientos/{id}` - Obtener un seguimiento por ID
- **PUT** `/seguimientos/{id}` - Actualizar un seguimiento
- **DELETE** `/seguimientos/{id}` - Eliminar un seguimiento

## 💰 Donaciones
- **GET** `/donaciones` - Obtener todas las donaciones
- **POST** `/donaciones` - Crear una nueva donación
- **GET** `/donaciones/{id}` - Obtener una donación por ID
- **PUT** `/donaciones/{id}` - Actualizar una donación
- **DELETE** `/donaciones/{id}` - Eliminar una donación

## 💳 Pagos
- **POST** `/pagos/init` - Inicializar un pago
- **POST** `/pagos` - Crear un nuevo pago
- **GET** `/pagos/{id}` - Obtener un pago por ID
- **PUT** `/pagos/{id}` - Actualizar un pago
- **DELETE** `/pagos/{id}` - Eliminar un pago

## 📦 Storage
- **POST** `/storage/upload` - Subir un archivo
- **GET** `/storage/list` - Listar archivos
- **POST** `/storage/buckets` - Crear un bucket
- **DELETE** `/storage/delete` - Eliminar un archivo
- **GET** `/storage/url` - Obtener URL pública de un archivo

## 📚 Documentación
- **GET** `/swagger-ui` - Interfaz de Swagger UI
- **GET** `/api-doc/openapi.json` - Especificación OpenAPI


```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│    USUARIO      │         │   PUBLICACION   │         │    ADOPCION     │
├─────────────────┤         ├─────────────────┤         ├─────────────────┤
│ id_usuario (PK) │◄───────┤ id_usuario (FK) │────────►│ id_publicacion  │
│ nombre          │         │ id_publicacion  │         │   (FK)          │
│ email (UQ)      │         │   (PK)          │         │ id_adopcion(PK) │
│ contrasenia     │         │ titulo          │         │ fecha_adopcion  │
│ telefono        │         │ descripcion     │         │ estado          │
│ direccion       │         │ fecha_subida    │         │ id_usuario (FK) │
│ fecha_registro  │         │ estado          │         └─────────────────┘
└─────────────────┘         │ id_animal (FK)  │
        │                   └─────────────────┘
        │                           │
        │                           │
        ▼                           ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   VOLUNTARIO    │         │     ANIMAL      │         │     ESPECIE     │
├─────────────────┤         ├─────────────────┤         ├─────────────────┤
│id_voluntario(PK)│         │ id_animal (PK)  │◄───────┤ id_especie (PK) │
│ rol             │         │ nombre          │         │ nombre (UQ)     │
│ estado          │         │ edad            │         └─────────────────┘
│ id_usuario (FK) │         │ estado          │
│ id_campania(FK) │         │ descripcion     │
└─────────────────┘         │ fotos           │
        │                   │ estado_adopcion │         ┌─────────────────┐
        │                   │ id_especie (FK) │         │    REFUGIO      │
        ▼                   │ id_refugio (FK) │◄───────┤ id_refugio (PK) │
┌─────────────────┐         └─────────────────┘         │ nombre          │
│    CAMPAÑA      │                 │                   │ direccion       │
├─────────────────┤                 │                   │ telefono        │
│ id_campania(PK) │                 │                   │ descripcion     │
│ titulo          │                 ▼                   └─────────────────┘
│ descripcion     │         ┌─────────────────┐                 │
│ fecha_inicio    │         │  SEGUIMIENTO    │                 │
│ fecha_fin       │         ├─────────────────┤                 │
│ lugar           │         │id_seguimiento   │                 ▼
│ organizador     │         │   (PK)          │         ┌─────────────────┐
│ estado          │         │ titulo          │         │   SUPERVISOR    │
│id_tipo_campania │         │ observaciones   │         ├─────────────────┤
│   (FK)          │         │ fecha_seguim.   │◄───────┤id_supervisor(PK)│
└─────────────────┘         │ id_animal (FK)  │         │ nombre          │
        │                   │ id_supervisor   │         │ total_animales  │
        │                   │   (FK)          │         │ id_refugio (FK) │
        ▼                   └─────────────────┘         │ id_animal (FK)  │
┌─────────────────┐                                     └─────────────────┘
│ TIPO_CAMPAÑA    │
├─────────────────┤         ┌─────────────────┐
│id_tipo_campania │         │ CAUSA_URGENTE   │
│   (PK)          │         ├─────────────────┤
│ nombre          │         │id_causa_urgente │
│ descripcion     │         │   (PK)          │
└─────────────────┘         │ titulo          │
                            │ descripcion     │
                            │ meta            │
┌─────────────────┐         │ fecha_limite    │
│    DONACION     │         │ id_refugio (FK) │
├─────────────────┤         │ id_animal (FK)  │
│ id_donacion(PK) │────────►│ fotos           │
│ monto           │         └─────────────────┘
│ fecha           │
│ id_usuario (FK) │
│id_causa_urgente │
│   (FK)          │
│ estado_donacion │
└─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│      PAGO       │
├─────────────────┤
│ id_pago (PK)    │
│ id_donacion(FK) │
│ monto           │
│ metodo_pago     │
│ estado_pago     │
│stripe_payment_  │
│  intent_id      │
│stripe_charge_id │
│fecha_pago_      │
│  completado     │
│ error_pago      │
│ created_at      │
└─────────────────┘
```
