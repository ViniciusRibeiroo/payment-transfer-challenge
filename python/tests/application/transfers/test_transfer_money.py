from decimal import Decimal
from uuid import uuid4

import pytest

from payment_transfer.application.transfers.transfer_money import TransferMoney
from payment_transfer.domain.accounts.account import Account
from payment_transfer.domain.accounts.account_type import AccountType

class FakeTransferAuthorizer:
    def __init__(self, authorized: bool = True) -> None:
        self.authorized = authorized

    def authorize(self, transfer) -> bool:
        return self.authorized

class FakeAccountRepository:
    def __init__(self, accounts: list[Account] | None = None) -> None:
        self.accounts = accounts or []

    def get_by_id(self, account_id):
        return next(
            (account for account in self.accounts if account.id == account_id),
            None,
        )

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
            (account for account in self.accounts if account.email == email),
            None,
        )

    def save(self, account):
        existing = self.get_by_id(account.id)

        if existing is None:
            self.accounts.append(account)

def create_account(
    account_type: AccountType = AccountType.USER,
    balance: Decimal = Decimal("100.00"),
) -> Account:
    return Account(
        full_name="John Doe",
        document=str(uuid4()),
        email=f"{uuid4()}@example.com",
        password_hash="$argon2id$example",
        account_type=account_type,
        balance=balance,
    )


def test_should_transfer_money_between_accounts():
    payer = create_account(balance=Decimal("100.00"))
    payee = create_account(balance=Decimal("50.00"))

    repository = FakeAccountRepository([payer, payee])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    transfer = use_case.execute(
        payer_id=payer.id,
        payee_id=payee.id,
        amount=Decimal("30.00"),
    )

    assert transfer.payer_id == payer.id
    assert transfer.payee_id == payee.id
    assert transfer.amount == Decimal("30.00")

    assert payer.balance == Decimal("70.00")
    assert payee.balance == Decimal("80.00")


def test_should_reject_transfer_when_payer_does_not_exist():
    payee = create_account()

    repository = FakeAccountRepository([payee])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(ValueError, match="Payer not found."):
        use_case.execute(
            payer_id=uuid4(),
            payee_id=payee.id,
            amount=Decimal("30.00"),
        )


def test_should_reject_transfer_when_payee_does_not_exist():
    payer = create_account()

    repository = FakeAccountRepository([payer])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(ValueError, match="Payee not found."):
        use_case.execute(
            payer_id=payer.id,
            payee_id=uuid4(),
            amount=Decimal("30.00"),
        )


def test_should_reject_transfer_from_merchant():
    payer = create_account(
        account_type=AccountType.MERCHANT,
        balance=Decimal("100.00"),
    )
    payee = create_account()

    repository = FakeAccountRepository([payer, payee])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(
        ValueError,
        match="Payer is not allowed to transfer money.",
    ):
        use_case.execute(
            payer_id=payer.id,
            payee_id=payee.id,
            amount=Decimal("30.00"),
        )


def test_should_reject_transfer_with_insufficient_balance():
    payer = create_account(balance=Decimal("20.00"))
    payee = create_account()

    repository = FakeAccountRepository([payer, payee])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(ValueError, match="Insufficient balance."):
        use_case.execute(
            payer_id=payer.id,
            payee_id=payee.id,
            amount=Decimal("30.00"),
        )

    assert payer.balance == Decimal("20.00")
    assert payee.balance == Decimal("100.00")


def test_should_reject_transfer_to_same_account():
    payer = create_account()

    repository = FakeAccountRepository([payer])
    authorizer = FakeTransferAuthorizer()

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(
        ValueError,
        match="Payer and payee must be different.",
    ):
        use_case.execute(
            payer_id=payer.id,
            payee_id=payer.id,
            amount=Decimal("30.00"),
        )

def test_should_reject_transfer_when_not_authorized():
    payer = create_account(balance=Decimal("100.00"))
    payee = create_account(balance=Decimal("50.00"))

    repository = FakeAccountRepository([payer, payee])
    authorizer = FakeTransferAuthorizer(authorized=False)

    use_case = TransferMoney(
        repository,
        authorizer,
    )

    with pytest.raises(
        ValueError,
        match="Transfer was not authorized.",
    ):
        use_case.execute(
            payer_id=payer.id,
            payee_id=payee.id,
            amount=Decimal("30.00"),
        )

    assert payer.balance == Decimal("100.00")
    assert payee.balance == Decimal("50.00")
