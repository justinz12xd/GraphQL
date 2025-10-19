import strawberry
from typing import List, Optional
from uuid import UUID
from app.modules.pago.interface.graphql_type import PagoType, InitPaymentInput, InitPaymentResponse
from app.modules.pago.application.pago_service import PagoApplicationService

@strawberry.type
class PagoQuery:
    """Queries relacionadas con pagos"""

    @strawberry.field
    async def obtener_pago(self, id_pago: strawberry.ID) -> Optional[PagoType]:
        """Obtener un pago por su ID"""
        service = PagoApplicationService()
        pago = await service.obtener_pago(UUID(id_pago))

        if pago is None:
            return None
            
        return PagoType(
            id_pago=pago.id_pago,
            monto=pago.monto,
            metodo_pago=pago.metodo_pago,
            estado_pago=pago.estado_pago,
            stripe_payment_intent_id=pago.stripe_payment_intent_id,
            stripe_charge_id=pago.stripe_charge_id,
            fecha_pago_completado=pago.fecha_pago_completado,
            fecha_pago=pago.fecha_pago,
            error_pago=pago.error_pago,
            create_at=pago.create_at,
            id_donacion=pago.id_donacion
        )

    @strawberry.field
    async def listar_pagos(self, limit: int = 50, offset: int = 0) -> List[PagoType]:
        """Listar todos los pagos con paginación"""
        service = PagoApplicationService()
        pagos = await service.listar_pagos(limit=limit, offset=offset)

        return [
            PagoType(
                id_pago=pago.id_pago,
                monto=pago.monto,
                metodo_pago=pago.metodo_pago,
                estado_pago=pago.estado_pago,
                stripe_payment_intent_id=pago.stripe_payment_intent_id,
                stripe_charge_id=pago.stripe_charge_id,
                fecha_pago_completado=pago.fecha_pago_completado,
                fecha_pago=pago.fecha_pago,
                error_pago=pago.error_pago,
                create_at=pago.create_at,
                id_donacion=pago.id_donacion
            )
            for pago in pagos
        ]

    @strawberry.field
    async def pagos_por_donacion(self, id_donacion: strawberry.ID) -> List[PagoType]:
        """Obtener todos los pagos de una donación específica"""
        service = PagoApplicationService()
        pagos = await service.obtener_pagos_por_donacion(UUID(id_donacion))

        return [
            PagoType(
                id_pago=pago.id_pago,
                monto=pago.monto,
                metodo_pago=pago.metodo_pago,
                estado_pago=pago.estado_pago,
                stripe_payment_intent_id=pago.stripe_payment_intent_id,
                stripe_charge_id=pago.stripe_charge_id,
                fecha_pago_completado=pago.fecha_pago_completado,
                fecha_pago=pago.fecha_pago,
                error_pago=pago.error_pago,
                create_at=pago.create_at,
                id_donacion=pago.id_donacion
            )
            for pago in pagos
        ]