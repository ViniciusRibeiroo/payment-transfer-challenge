from decimal import Decimal
from uuid import uuid4

import pytest

from payment_transfer.domain.transfers.transfer import Transfer


def test_should_create_transfer():
    payer_id = uuid4()
    payee_id = uuid4()

    transfer = Transfer(
        payer_id=payer_id,
        payee_id=payee_id,
        amount=Decimal("100.00"),
    )

    assert transfer.payer_id == payer_id
    assert transfer.payee_id == payee_id
    assert transfer.amount == Decimal("100.00")


def test_should_generate_uuid_transfer_id():
    transfer = Transfer(
        payer_id=uuid4(),
        payee_id=uuid4(),
        amount=Decimal("100.00"),
    )

    assert transfer.id is not None


def test_should_preserve_existing_transfer_id():
    transfer_id = uuid4()

    transfer = Transfer(
        payer_id=uuid4(),
        payee_id=uuid4(),
        amount=Decimal("100.00"),
        transfer_id=transfer_id,
    )

    assert transfer.id == transfer_id


def test_should_reject_transfer_to_same_account():
    account_id = uuid4()

    with pytest.raises(
        ValueError,
        match="Payer and payee must be different.",
    ):
        Transfer(
            payer_id=account_id,
            payee_id=account_id,
            amount=Decimal("100.00"),
        )


def test_should_reject_zero_transfer():
    with pytest.raises(
        ValueError,
        match="Transfer amount must be greater than zero.",
    ):
        Transfer(
            payer_id=uuid4(),
            payee_id=uuid4(),
            amount=Decimal("0.00"),
        )


def test_should_reject_negative_transfer():
    with pytest.raises(
        ValueError,
        match="Transfer amount must be greater than zero.",
    ):
        Transfer(
            payer_id=uuid4(),
            payee_id=uuid4(),
            amount=Decimal("-10.00"),
        )
