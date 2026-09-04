from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from payment_transfer.domain.accounts.account import Account
from payment_transfer.infrastructure.database.account_mapper import (
    to_domain,
    to_model,
)
from payment_transfer.infrastructure.database.models import AccountModel


class SqlAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, account_id: UUID) -> Account | None:
        model = self._session.get(AccountModel, account_id)

        if model is None:
            return None

        return to_domain(model)

    def get_by_document(self, document: str) -> Account | None:
        statement = select(AccountModel).where(
            AccountModel.document == document
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_by_email(self, email: str) -> Account | None:
        statement = select(AccountModel).where(
            AccountModel.email == email
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def save(self, account: Account) -> None:
        model = to_model(account)

        self._session.add(model)
