import strawberry
from typing import Optional
from uuid import UUID
from datetime import datetime

@strawberry.type
class PagoType:
    """Tipo GraphQL para representar un pago"""
    id_pago: UUID
    monto: float
    metodo_pago: str
    estado_pago: Optional[str] = None
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    fecha_pago_completado: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None
    error_pago: Optional[str] = None
    create_at: datetime
    id_donacion: Optional[UUID] = None

@strawberry.input
class InitPaymentInput:
    """Input para inicializar un pago con Stripe"""
    amount: float
    currency: str = "usd"
    description: Optional[str] = None
    id_donacion: Optional[UUID] = None

@strawberry.type
class InitPaymentResponse:
    """Respuesta de inicialización de pago"""
    client_secret: str
    payment_intent_id: str
    id_pago: UUID

@strawberry.input
class CreatePagoInput:
    """Input para crear un nuevo pago"""
    monto: float
    metodo_pago: str
    id_donacion: Optional[UUID] = None

@strawberry.input
class UpdatePagoInput:
    """Input para actualizar un pago"""
    estado_pago: Optional[str] = None
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    fecha_pago_completado: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None
    error_pago: Optional[str] = None

@strawberry.input
class ConfirmPaymentInput:
    """Input para confirmar un pago de Stripe"""
    payment_intent_id: str
    payment_status: str
    charge_id: Optional[str] = None
    error_message: Optional[str] = None