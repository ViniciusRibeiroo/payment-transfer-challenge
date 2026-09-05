from decimal import Decimal
from uuid import UUID

from payment_transfer.application.accounts.account_repository import (
    AccountRepository,
)
from payment_transfer.domain.accounts.account_type import AccountType
from payment_transfer.domain.transfers.transfer import Transfer


class TransferMoney:
    def __init__(
        self,
        account_repository: AccountRepository,
    ) -> None:
        self._account_repository = account_repository

    def execute(
        self,
        payer_id: UUID,
        payee_id: UUID,
        amount: Decimal,
    ) -> Transfer:
        payer = self._account_repository.get_by_id(payer_id)

        if payer is None:
            raise ValueError("Payer not found.")

        payee = self._account_repository.get_by_id(payee_id)

        if payee is None:
            raise ValueError("Payee not found.")

        if payer.account_type != AccountType.USER:
            raise ValueError("Payer is not allowed to transfer money.")

        transfer = Transfer(
            payer_id=payer_id,
            payee_id=payee_id,
            amount=amount,
        )

        payer.debit(amount)
        payee.credit(amount)

        self._account_repository.save(payer)
        self._account_repository.save(payee)

        return transfer
