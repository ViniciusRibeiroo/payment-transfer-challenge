from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from payment_transfer.domain.accounts.account import Account
from payment_transfer.domain.accounts.account_type import AccountType


def create_account(**overrides) -> Account:
    data = {
        "full_name": "John Doe",
        "document": "12345678900",
        "email": "john@example.com",
        "password_hash": "$argon2id$example",
        "account_type": AccountType.USER,
    }

    data.update(overrides)

    return Account(**data)


def test_should_create_user_account():
    account = create_account()

    assert account.full_name == "John Doe"
    assert account.account_type == AccountType.USER
    assert account.balance == Decimal("0.00")


def test_should_create_merchant_account():
    account = create_account(
        account_type=AccountType.MERCHANT,
    )

    assert account.account_type == AccountType.MERCHANT


def test_should_generate_uuid_account_id():
    account = create_account()

    assert isinstance(account.id, UUID)


def test_should_preserve_existing_account_id():
    account_id = uuid4()

    account = create_account(account_id=account_id)

    assert account.id == account_id


def test_should_reject_empty_name():
    with pytest.raises(
        ValueError,
        match="Full name cannot be empty.",
    ):
        create_account(full_name="")


def test_should_reject_empty_document():
    with pytest.raises(
        ValueError,
        match="Document cannot be empty.",
    ):
        create_account(document="")


def test_should_reject_empty_email():
    with pytest.raises(
        ValueError,
        match="Email cannot be empty.",
    ):
        create_account(email="")


def test_should_reject_empty_password_hash():
    with pytest.raises(
        ValueError,
        match="Password hash cannot be empty.",
    ):
        create_account(password_hash="")


def test_should_reject_negative_balance():
    with pytest.raises(
        ValueError,
        match="Balance cannot be negative.",
    ):
        create_account(
            balance=Decimal("-0.01"),
        )

def test_should_debit_account_balance():
    account = create_account(balance=Decimal("100.00"))

    account.debit(Decimal("30.00"))

    assert account.balance == Decimal("70.00")


def test_should_reject_debit_when_balance_is_insufficient():
    account = create_account(balance=Decimal("50.00"))

    with pytest.raises(ValueError, match="Insufficient balance."):
        account.debit(Decimal("100.00"))


def test_should_reject_zero_debit():
    account = create_account(balance=Decimal("100.00"))

    with pytest.raises(ValueError, match="Debit amount must be greater than zero."):
        account.debit(Decimal("0.00"))


def test_should_reject_negative_debit():
    account = create_account(balance=Decimal("100.00"))

    with pytest.raises(ValueError, match="Debit amount must be greater than zero."):
        account.debit(Decimal("-10.00"))


def test_should_credit_account_balance():
    account = create_account(balance=Decimal("100.00"))

    account.credit(Decimal("30.00"))

    assert account.balance == Decimal("130.00")


def test_should_reject_zero_credit():
    account = create_account(balance=Decimal("100.00"))

    with pytest.raises(ValueError, match="Credit amount must be greater than zero."):
        account.credit(Decimal("0.00"))


def test_should_reject_negative_credit():
    account = create_account(balance=Decimal("100.00"))

    with pytest.raises(ValueError, match="Credit amount must be greater than zero."):
        account.credit(Decimal("-10.00"))
