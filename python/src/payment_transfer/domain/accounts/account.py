from decimal import Decimal
from uuid import UUID, uuid4

from payment_transfer.domain.accounts.account_type import AccountType


class Account:
    def __init__(
        self,
        full_name: str,
        document: str,
        email: str,
        password_hash: str,
        account_type: AccountType,
        balance: Decimal = Decimal("0.00"),
        account_id: UUID | None = None,
    ) -> None:
        self.id = account_id or uuid4()
        self.full_name = full_name
        self.document = document
        self.email = email
        self.password_hash = password_hash
        self.account_type = account_type
        self.balance = balance

        self._validate()

    def _validate(self) -> None:
        if not self.full_name.strip():
            raise ValueError("Full name cannot be empty.")

        if not self.document.strip():
            raise ValueError("Document cannot be empty.")

        if not self.email.strip():
            raise ValueError("Email cannot be empty.")

        if not self.password_hash.strip():
            raise ValueError("Password hash cannot be empty.")

        if self.balance < Decimal("0.00"):
            raise ValueError("Balance cannot be negative.")

    def debit(self, amount: Decimal) -> None:
        if amount <= Decimal("0.00"):
            raise ValueError("Debit amount must be greater than zero.")

        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self.balance -= amount

    def credit(self, amount: Decimal) -> None:
        if amount <= Decimal("0.00"):
            raise ValueError("Credit amount must be greater than zero.")

        self.balance += amount
