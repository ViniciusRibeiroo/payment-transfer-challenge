from decimal import Decimal

from payment_transfer.application.accounts.account_repository import (
    AccountRepository,
)
from payment_transfer.application.security.password_hasher import PasswordHasher
from payment_transfer.domain.accounts.account import Account
from payment_transfer.domain.accounts.account_type import AccountType


class CreateAccount:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._account_repository = account_repository
        self._password_hasher = password_hasher

    def execute(
        self,
        full_name: str,
        document: str,
        email: str,
        password: str,
        account_type: AccountType,
        balance: Decimal = Decimal("0.00"),
    ) -> Account:
        if self._account_repository.get_by_document(document) is not None:
            raise ValueError("Document already registered.")

        if self._account_repository.get_by_email(email) is not None:
            raise ValueError("Email already registered.")

        password_hash = self._password_hasher.hash(password)

        account = Account(
            full_name=full_name,
            document=document,
            email=email,
            password_hash=password_hash,
            account_type=account_type,
            balance=balance,
        )

        self._account_repository.save(account)

        return account
