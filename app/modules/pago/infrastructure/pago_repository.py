import httpx
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.config.settings import settings
from app.modules.pago.domain.entitie import Pago, NewPago, UpdatePago

class PagoRepository:
    """Repositorio para gestionar pagos mediante REST API con integración Stripe"""
    
    def __init__(self):
        self.base_url = settings.REST_API_URL
        self.timeout = 30

    async def _get_client(self) -> httpx.AsyncClient:
        """Crea un cliente HTTP asíncrono"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
    
    def _parse_pago(self, data: dict) -> Pago:
        """Convierte la respuesta del API REST en una entidad Pago"""
        return Pago(
            id_pago=UUID(data["id_pago"]) if isinstance(data["id_pago"], str) else data["id_pago"],
            monto=float(data["monto"]),
            metodo_pago=data["metodo_pago"],
            estado_pago=data.get("estado_pago"),
            stripe_payment_intent_id=data.get("stripe_payment_intent_id"),
            stripe_charge_id=data.get("stripe_charge_id"),
            fecha_pago_completado=self._parse_datetime(data.get("fecha_pago_completado")),
            fecha_pago=self._parse_datetime(data.get("fecha_pago")),
            error_pago=data.get("error_pago"),
            create_at=self._parse_datetime(data.get("created_at")) or datetime.now(),
            id_donacion=UUID(data["id_donacion"]) if data.get("id_donacion") and isinstance(data["id_donacion"], str) else data.get("id_donacion")
        )

    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Convierte string ISO a datetime"""
        if not date_str:
            return None
        try:
            # Maneja diferentes formatos de fecha
            if date_str.endswith('Z'):
                return datetime.fromisoformat(date_str[:-1] + '+00:00')
            return datetime.fromisoformat(date_str)
        except ValueError:
            return None

    async def listar_pagos(self, limit: int = 50, offset: int = 0) -> List[Pago]:
        """Obtener todos los pagos - Fallback temporal hasta que se implemente GET /pagos"""
        # TEMPORAL: Como no existe GET /pagos en el backend, retornamos lista vacía
        # TODO: Implementar GET /pagos en el backend de Rust con paginación
        
        # Para desarrollo, retornamos una lista vacía por ahora
        # Una vez que se implemente la ruta en Rust, descomentar el código siguiente:
        
        # async with await self._get_client() as client:
        #     params = {"limit": limit, "offset": offset}
        #     response = await client.get("/pagos", params=params)
        #     response.raise_for_status()
        #     pagos_data = response.json()
        #     return [self._parse_pago(data) for data in pagos_data]
        
        return []

    async def obtener_pago_por_id(self, id_pago: UUID) -> Optional[Pago]:
        """GET /pagos/{id} - Obtener un pago por ID"""
        async with await self._get_client() as client:
            try:
                response = await client.get(f"/pagos/{str(id_pago)}")
                response.raise_for_status()
                data = response.json()
                return self._parse_pago(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def obtener_pagos_por_donacion(self, id_donacion: UUID) -> List[Pago]:
        """Obtener todos los pagos de una donación - Fallback temporal"""
        # TEMPORAL: Como no existe GET /pagos/donacion/{id} en el backend, retornamos lista vacía
        # TODO: Implementar GET /pagos/donacion/{id} en el backend de Rust
        
        # Para desarrollo, retornamos una lista vacía por ahora
        # Una vez que se implemente la ruta en Rust, descomentar el código siguiente:
        
        # async with await self._get_client() as client:
        #     response = await client.get(f"/pagos/donacion/{str(id_donacion)}")
        #     response.raise_for_status()
        #     pagos_data = response.json()
        #     return [self._parse_pago(data) for data in pagos_data]
        
        return []

    async def obtener_estadisticas_pagos(self, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> Dict[str, Any]:
        """GET /pagos/stats - Obtener estadísticas de pagos"""
        async with await self._get_client() as client:
            params = {}
            if fecha_inicio:
                params["fecha_inicio"] = fecha_inicio.isoformat()
            if fecha_fin:
                params["fecha_fin"] = fecha_fin.isoformat()

            response = await client.get("/pagos/stats", params=params)
            response.raise_for_status()
            return response.json()

    async def obtener_pagos_por_estado(self, estado: str, limit: int = 50, offset: int = 0) -> List[Pago]:
        """GET /pagos?estado={estado} - Obtener pagos por estado"""
        async with await self._get_client() as client:
            params = {
                "estado": estado,
                "limit": limit,
                "offset": offset
            }
            response = await client.get("/pagos", params=params)
            response.raise_for_status()
            pagos_data = response.json()
            return [self._parse_pago(data) for data in pagos_data]

    async def obtener_pagos_por_metodo(self, metodo_pago: str, limit: int = 50, offset: int = 0) -> List[Pago]:
        """GET /pagos?metodo={metodo} - Obtener pagos por método de pago"""
        async with await self._get_client() as client:
            params = {
                "metodo_pago": metodo_pago,
                "limit": limit,
                "offset": offset
            }
            response = await client.get("/pagos", params=params)
            response.raise_for_status()
            pagos_data = response.json()
            return [self._parse_pago(data) for data in pagos_data]