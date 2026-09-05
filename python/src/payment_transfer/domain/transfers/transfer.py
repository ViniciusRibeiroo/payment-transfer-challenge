from decimal import Decimal
from uuid import UUID, uuid4


class Transfer:
    def __init__(
        self,
        payer_id: UUID,
        payee_id: UUID,
        amount: Decimal,
        transfer_id: UUID | None = None,
    ) -> None:
        self.id = transfer_id or uuid4()
        self.payer_id = payer_id
        self.payee_id = payee_id
        self.amount = amount
        self._validate()

    def _validate(self) -> None:
        if self.payer_id == self.payee_id:
            raise ValueError("Payer and payee must be different.")

        if self.amount <= Decimal("0.00"):
            raise ValueError("Transfer amount must be greater than zero.")
