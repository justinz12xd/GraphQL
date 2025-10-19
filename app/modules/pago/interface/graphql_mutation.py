import strawberry
from typing import Optional
from uuid import UUID
from app.modules.pago.interface.graphql_type import (
    PagoType, InitPaymentInput, InitPaymentResponse, 
    CreatePagoInput, UpdatePagoInput, ConfirmPaymentInput
)
from app.modules.pago.application.pago_service  import PagoApplicationService
from app.modules.pago.domain.entitie import NewPago, UpdatePago

@strawberry.type
class PagoMutation:
    """Mutations relacionadas con pagos y Stripe"""

    @strawberry.mutation
    async def inicializar_pago(self, input: InitPaymentInput) -> InitPaymentResponse:
        """Inicializar un pago con Stripe - Crear PaymentIntent"""
        service = PagoApplicationService()
        
        response = await service.init_payment(
            amount=input.amount,
            currency=input.currency,
            description=input.description,
            id_donacion=input.id_donacion
        )
        
        return InitPaymentResponse(
            client_secret=response["client_secret"],
            payment_intent_id=response["payment_intent_id"],
            id_pago=UUID(response["id_pago"])
        )

    @strawberry.mutation
    async def confirmar_pago(self, input: ConfirmPaymentInput) -> PagoType:
        """Confirmar un pago después del procesamiento de Stripe"""
        service = PagoApplicationService()
        
        pago = await service.confirm_payment(
            payment_intent_id=input.payment_intent_id,
            payment_status=input.payment_status,
            charge_id=input.charge_id,
            error_message=input.error_message
        )
        
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

    @strawberry.mutation
    async def cancelar_pago(self, id_pago: strawberry.ID) -> PagoType:
        """Cancelar un pago pendiente"""
        service = PagoApplicationService()
        
        pago = await service.cancel_payment(UUID(id_pago))
        
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

    @strawberry.mutation
    async def reembolsar_pago(self, id_pago: strawberry.ID, amount: Optional[float] = None, reason: Optional[str] = None) -> PagoType:
        """Procesar un reembolso de pago"""
        service = PagoApplicationService()
        
        pago = await service.refund_payment(
            id_pago=UUID(id_pago),
            amount=amount,
            reason=reason
        )
        
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

    @strawberry.mutation
    async def crear_pago(self, input: CreatePagoInput) -> PagoType:
        """Crear un pago básico (sin Stripe)"""
        service = PagoApplicationService()
        
        nuevo_pago = NewPago(
            monto=input.monto,
            metodo_pago=input.metodo_pago,
            id_donacion=input.id_donacion
        )
        
        pago = await service.create_pago(nuevo_pago)
        
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

    @strawberry.mutation
    async def actualizar_pago(self, id_pago: strawberry.ID, input: UpdatePagoInput) -> PagoType:
        """Actualizar un pago existente"""
        service = PagoApplicationService()
        
        pago_actualizado = UpdatePago(
            estado_pago=input.estado_pago,
            stripe_payment_intent_id=input.stripe_payment_intent_id,
            stripe_charge_id=input.stripe_charge_id,
            fecha_pago_completado=input.fecha_pago_completado,
            fecha_pago=input.fecha_pago,
            error_pago=input.error_pago
        )
        
        pago = await service.update_pago(UUID(id_pago), pago_actualizado)
        
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