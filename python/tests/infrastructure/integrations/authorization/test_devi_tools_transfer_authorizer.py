from decimal import Decimal
from uuid import uuid4

import httpx

from payment_transfer.domain.transfers.transfer import Transfer
from payment_transfer.infrastructure.integrations.authorization.devi_tools_transfer_authorizer import (
    DeviToolsTransferAuthorizer,
)


def create_transfer() -> Transfer:
    return Transfer(
        payer_id=uuid4(),
        payee_id=uuid4(),
        amount=Decimal("100.00"),
    )


def test_should_authorize_transfer_when_service_allows_it():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == (
            "https://util.devi.tools/api/v2/authorize"
        )

        return httpx.Response(
            200,
            json={
                "status": "success",
                "data": {
                    "authorization": True,
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    authorizer = DeviToolsTransferAuthorizer(client)

    assert authorizer.authorize(create_transfer())


def test_should_reject_transfer_when_service_denies_it():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "status": "success",
                "data": {
                    "authorization": False,
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    authorizer = DeviToolsTransferAuthorizer(client)

    assert not authorizer.authorize(create_transfer())

def test_should_raise_when_authorization_service_fails():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)

    authorizer = DeviToolsTransferAuthorizer(client)

    try:
        authorizer.authorize(create_transfer())
    except httpx.HTTPStatusError:
        pass
    else:
        raise AssertionError("Expected HTTPStatusError.")
