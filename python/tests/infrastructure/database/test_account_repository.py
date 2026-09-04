from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from payment_transfer.domain.accounts.account import Account
from payment_transfer.domain.accounts.account_type import AccountType
from payment_transfer.infrastructure.database.account_repository import (
    SqlAlchemyAccountRepository,
)
from payment_transfer.infrastructure.database.models import Base


def create_account() -> Account:
    return Account(
        full_name="John Doe",
        document="12345678900",
        email="john@example.com",
        password_hash="$argon2id$example",
        account_type=AccountType.USER,
        balance=Decimal("100.00"),
    )


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    return Session(engine)


def test_should_save_and_retrieve_account_by_id():
    with create_session() as session:
        repository = SqlAlchemyAccountRepository(session)
        account = create_account()

        repository.save(account)
        session.commit()

        result = repository.get_by_id(account.id)

        assert result is not None
        assert result.id == account.id
        assert result.full_name == account.full_name
        assert result.document == account.document
        assert result.email == account.email
        assert result.password_hash == account.password_hash
        assert result.account_type == account.account_type
        assert result.balance == account.balance


def test_should_find_account_by_document():
    with create_session() as session:
        repository = SqlAlchemyAccountRepository(session)
        account = create_account()

        repository.save(account)
        session.commit()

        result = repository.get_by_document(account.document)

        assert result is not None
        assert result.id == account.id


def test_should_find_account_by_email():
    with create_session() as session:
        repository = SqlAlchemyAccountRepository(session)
        account = create_account()

        repository.save(account)
        session.commit()

        result = repository.get_by_email(account.email)

        assert result is not None
        assert result.id == account.id


def test_should_return_none_when_account_does_not_exist():
    with create_session() as session:
        repository = SqlAlchemyAccountRepository(session)

        result = repository.get_by_document("99999999999")

        assert result is None
