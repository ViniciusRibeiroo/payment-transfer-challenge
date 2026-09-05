from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class TransferRequest(BaseModel):
    payer_id: UUID
    payee_id: UUID
    amount: Decimal = Field(gt=0)
