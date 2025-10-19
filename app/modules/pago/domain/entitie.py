from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional
from typing import List


@dataclass
class Pago:
    id_pago: UUID
    monto: float
    metodo_pago: str
    estado_pago: Optional[str]
    stripe_payment_intent_id: Optional[str]
    stripe_charge_id: Optional[str]
    fecha_pago_completado: Optional[datetime]
    fecha_pago: Optional[datetime]
    error_pago: Optional[str]
    create_at: datetime
    id_donacion: Optional[UUID]

@dataclass
class NewPago:
    monto: float
    metodo_pago: str
    id_donacion: Optional[UUID] = None

@dataclass
class UpdatePago:
    estado_pago: Optional[str] = None
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    fecha_pago_completado: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None
    error_pago: Optional[str] = None

