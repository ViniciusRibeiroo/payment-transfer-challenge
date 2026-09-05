from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TransferResponse(BaseModel):
    id: UUID
    payer_id: UUID
    payee_id: UUID
    amount: Decimal
