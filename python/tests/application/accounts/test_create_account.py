from decimal import Decimal

from payment_transfer.application.accounts.create_account import (
    CreateAccount,
)
from payment_transfer.domain.accounts.account_type import AccountType


class FakeAccountRepository:
    def __init__(self) -> None:
        self.accounts = []

    def get_by_document(self, document):
        return next(
            (
                account
                for account in self.accounts
                if account.document == document
            ),
            None,
        )

    def get_by_email(self, email):
        return next(
            (
                account
                for account in self.accounts
                if account.email == email
            ),
            None,
        )

    def save(self, account):
        self.accounts.append(account)


class FakePasswordHasher:
    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == f"hashed:{password}"


def create_use_case():
    repository = FakeAccountRepository()
    hasher = FakePasswordHasher()

    return CreateAccount(repository, hasher), repository


def test_should_create_account_with_hashed_password():
    use_case, repository = create_use_case()

    account = use_case.execute(
        full_name="John Doe",
        document="12345678900",
        email="john@example.com",
        password="MySecurePassword123!",
        account_type=AccountType.USER,
    )

    assert account.password_hash == "hashed:MySecurePassword123!"
    assert account.password_hash != "MySecurePassword123!"
    assert repository.accounts == [account]


def test_should_create_account_with_zero_balance_by_default():
    use_case, _ = create_use_case()

    account = use_case.execute(
        full_name="John Doe",
        document="12345678900",
        email="john@example.com",
        password="MySecurePassword123!",
        account_type=AccountType.USER,
    )

    assert account.balance == Decimal("0.00")


def test_should_reject_duplicate_document():
    use_case, repository = create_use_case()

    existing_account = use_case.execute(
        full_name="John Doe",
        document="12345678900",
        email="john@example.com",
        password="MySecurePassword123!",
        account_type=AccountType.USER,
    )

    try:
        use_case.execute(
            full_name="Jane Doe",
            document=existing_account.document,
            email="jane@example.com",
            password="AnotherPassword123!",
            account_type=AccountType.USER,
        )

        assert False
    except ValueError as exception:
        assert str(exception) == "Document already registered."


def test_should_reject_duplicate_email():
    use_case, _ = create_use_case()

    use_case.execute(
        full_name="John Doe",
        document="12345678900",
        email="john@example.com",
        password="MySecurePassword123!",
        account_type=AccountType.USER,
    )

    try:
        use_case.execute(
            full_name="Jane Doe",
            document="98765432100",
            email="john@example.com",
            password="AnotherPassword123!",
            account_type=AccountType.USER,
        )

        assert False
    except ValueError as exception:
        assert str(exception) == "Email already registered."
