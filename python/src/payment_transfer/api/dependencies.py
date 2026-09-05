import httpx
from fastapi import Depends
from sqlalchemy.orm import Session

from payment_transfer.application.accounts.account_repository import (
    AccountRepository,
)
from payment_transfer.application.transfers.transfer_authorizer import (
    TransferAuthorizer,
)
from payment_transfer.application.transfers.transfer_money import TransferMoney
from payment_transfer.infrastructure.database.account_repository import (
    SqlAlchemyAccountRepository,
)
from payment_transfer.infrastructure.database.session import SessionLocal
from payment_transfer.infrastructure.integrations.authorization.devi_tools_transfer_authorizer import (
    DeviToolsTransferAuthorizer,
)
from payment_transfer.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_http_client():
    client = httpx.Client()

    try:
        yield client
    finally:
        client.close()


def get_account_repository(
    session: Session = Depends(get_session),
) -> AccountRepository:
    return SqlAlchemyAccountRepository(session)


def get_transfer_authorizer(
    client: httpx.Client = Depends(get_http_client),
) -> TransferAuthorizer:
    return DeviToolsTransferAuthorizer(client)


def get_transfer_money(
    account_repository: AccountRepository = Depends(get_account_repository),
    transfer_authorizer: TransferAuthorizer = Depends(get_transfer_authorizer),
) -> TransferMoney:
    return TransferMoney(
        account_repository=account_repository,
        transfer_authorizer=transfer_authorizer,
    )

def get_transfer_money(
    account_repository: AccountRepository = Depends(get_account_repository),
    transfer_authorizer: TransferAuthorizer = Depends(get_transfer_authorizer),
    session: Session = Depends(get_session),
) -> TransferMoney:
    return TransferMoney(
        account_repository=account_repository,
        transfer_authorizer=transfer_authorizer,
        unit_of_work=SqlAlchemyUnitOfWork(session),
    )
