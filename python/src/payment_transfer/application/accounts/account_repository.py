from typing import Protocol
from uuid import UUID

from payment_transfer.domain.accounts.account import Account


class AccountRepository(Protocol):
    def get_by_id(self, account_id: UUID) -> Account | None:
        ...

    def get_by_document(self, document: str) -> Account | None:
        ...

    def get_by_email(self, email: str) -> Account | None:
        ...

    def save(self, account: Account) -> None:
        ...
