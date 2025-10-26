# 📄 Módulo de Reportes PDF

## 🏗️ Arquitectura

Este módulo sigue una **arquitectura en capas** con separación de responsabilidades:

```
reports/
├── config/          # Configuración y settings
├── schemas/         # DTOs y modelos de datos
├── clients/         # Clientes externos (GraphQL)
├── generators/      # Generadores de reportes (PDF, Excel, etc.)
├── services/        # Lógica de negocio
└── routes/          # Endpoints FastAPI
```

### 📦 Principios aplicados:

✅ **Single Responsibility**: Cada clase tiene una única responsabilidad  
✅ **Dependency Injection**: Servicios inyectados en constructores  
✅ **Open/Closed**: Extensible mediante herencia (BaseReportGenerator)  
✅ **Interface Segregation**: Interfaces pequeñas y específicas  
✅ **Separation of Concerns**: Capas bien definidas  

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar solo las dependencias de reportes
pip install reportlab gql[all] aiohttp pydantic-settings
```

## 🧪 Pruebas Rápidas

### 1. Endpoint de prueba (sin datos reales):
```
http://localhost:8000/api/reports/test/pdf
```

### 2. Health check:
```
http://localhost:8000/api/reports/health
```

### 3. Documentación interactiva:
```
http://localhost:8000/docs
```

## 📝 Endpoints Disponibles

### Reportes de Animales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/reports/test/pdf` | GET | PDF de prueba (sin datos reales) |
| `/api/reports/animales/por-especie/pdf` | GET | Animales por especie |
| `/api/reports/animales/por-refugio/pdf` | GET | Animales por refugio |
| `/api/reports/animales/general/pdf` | GET | Reporte general |
| `/api/reports/animales/filtrados/pdf` | GET | Animales con filtros combinados |
| `/api/reports/campanias/pdf` | GET | Campañas activas |

## 🎯 Uso desde el Frontend

### React/Next.js

```typescript
// utils/pdfReports.ts
export const descargarReportePDF = async (
  endpoint: string,
  params?: Record<string, string>,
  filename?: string
) => {
  const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`);
  
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.append(key, value);
    });
  }

  const response = await fetch(url.toString());
  
  if (!response.ok) {
    throw new Error('Error al generar el reporte');
  }

  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = filename || 'reporte.pdf';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(downloadUrl);
};

// Uso
await descargarReportePDF(
  '/api/reports/animales/por-especie/pdf',
  { id_especie: 'uuid-here' },
  'animales.pdf'
);
```

### Componente de ejemplo

```tsx
'use client';

import { useState } from 'react';

export default function BotonDescargarReporte({ especieId }) {
  const [loading, setLoading] = useState(false);

  const handleDescargar = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/reports/animales/por-especie/pdf?id_especie=${especieId}`
      );
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'reporte.pdf';
      a.click();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleDescargar} disabled={loading}>
      {loading ? 'Generando...' : 'Descargar PDF'}
    </button>
  );
}
```

## ⚙️ Configuración

### Variables de entorno

```bash
# .env
REPORT_GRAPHQL_URL=http://localhost:8000/graphql
REPORT_PDF_PAGE_SIZE=A4
REPORT_PDF_AUTHOR=Sistema de Refugio Animal
REPORT_PDF_PRIMARY_COLOR=#3498DB
REPORT_PDF_SECONDARY_COLOR=#2C3E50
```

### Personalizar en código

```python
# app/reports/config/settings.py
settings.pdf_primary_color = "#FF5733"
settings.pdf_page_size = "letter"
```

## 🔧 Extensibilidad

### Agregar un nuevo tipo de reporte

1. **Agregar método en GraphQLClient:**
```python
# app/reports/clients/graphql_client.py
async def obtener_adopciones(self):
    query = """
    query {
        listarAdopciones {
            idAdopcion
            fechaAdopcion
            # ...
        }
    }
    """
    result = await self.execute_query(query)
    return result.get("listarAdopciones", [])
```

2. **Agregar generador en PDFGenerator:**
```python
# app/reports/generators/pdf_generator.py
def _generate_adopciones(self, adopciones):
    # Lógica de generación...
    pass
```

3. **Agregar método en ReportService:**
```python
# app/reports/services/report_service.py
async def generar_reporte_adopciones(self):
    adopciones = await self.graphql_client.obtener_adopciones()
    pdf_buffer = self.pdf_generator.generate(
        data=adopciones,
        report_type="adopciones"
    )
    return pdf_buffer, "adopciones.pdf"
```

4. **Agregar endpoint:**
```python
# app/reports/routes/report_routes.py
@router.get("/adopciones/pdf")
async def generar_pdf_adopciones():
    pdf_buffer, filename = await report_service.generar_reporte_adopciones()
    return StreamingResponse(pdf_buffer, ...)
```

## 🐛 Debugging

### Habilitar logs

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Ver logs de reportes

```python
logger = logging.getLogger("app.reports")
logger.setLevel(logging.DEBUG)
```

## 📊 Estructura de un PDF generado

1. **Encabezado:**
   - Título del reporte
   - Fecha y hora de generación

2. **Estadísticas:**
   - Totales
   - Distribuciones
   - Porcentajes

3. **Tabla de datos:**
   - Encabezado con color
   - Filas alternas
   - Datos formateados

## 🎨 Personalización de Estilos

Los PDFs usan los siguientes estilos:

- **Primary Color**: Encabezados de tablas
- **Secondary Color**: Textos principales
- **Background Color**: Filas alternas

Personalízalos en `app/reports/config/settings.py`

## ✅ Testing

### Probar sin frontend

```bash
# Endpoint de prueba
curl http://localhost:8000/api/reports/test/pdf --output test.pdf

# Reporte general
curl http://localhost:8000/api/reports/animales/general/pdf --output animales.pdf
```

### Probar en el navegador

```
http://localhost:8000/api/reports/test/pdf
```

## 🚦 Estados de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | PDF generado exitosamente |
| 404 | No se encontraron datos |
| 500 | Error interno del servidor |

## 📚 Dependencias

- **reportlab**: Generación de PDFs
- **gql**: Cliente GraphQL
- **aiohttp**: HTTP asíncrono
- **pydantic-settings**: Configuración tipada
