from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from payment_transfer.api.dependencies import get_transfer_money
from payment_transfer.domain.transfers.transfer import Transfer
from payment_transfer.main import app


class FakeTransferMoney:
    def execute(self, payer_id, payee_id, amount):
        return Transfer(
            payer_id=payer_id,
            payee_id=payee_id,
            amount=amount,
        )


def test_should_create_transfer():
    payer_id = uuid4()
    payee_id = uuid4()

    app.dependency_overrides[get_transfer_money] = (
        lambda: FakeTransferMoney()
    )

    client = TestClient(app)

    response = client.post(
        "/transfers",
        json={
            "payer_id": str(payer_id),
            "payee_id": str(payee_id),
            "amount": "100.00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["payer_id"] == str(payer_id)
    assert data["payee_id"] == str(payee_id)
    assert data["amount"] == "100.00"

    app.dependency_overrides.clear()


def test_should_reject_invalid_transfer_amount():
    app.dependency_overrides[get_transfer_money] = (
        lambda: FakeTransferMoney()
    )

    client = TestClient(app)

    response = client.post(
        "/transfers",
        json={
            "payer_id": str(uuid4()),
            "payee_id": str(uuid4()),
            "amount": "0.00",
        },
    )

    assert response.status_code == 422

    app.dependency_overrides.clear()
